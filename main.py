import json
import os
import re

import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from glob import glob
import pydicom
import zipfile
import argparse



parser = argparse.ArgumentParser(description='Update the CSV file with the latest data from the Flywheel UNITY QA project.')
parser.add_argument('--apikey','-apikey',type=str,nargs='?',help='FW CLI API key')

args = parser.parse_args()
api_key = args.apikey

fw = flywheel.Client(api_key=api_key)
display(f"User: {fw.get_current_user().firstname} {fw.get_current_user().lastname}")

fw_project = fw.projects.find_first('label=UNITY-QA')
project = project.reload()
display(f"Project: {project.label}")

subjects = fw_project.subjects()
print(f"This project has {len(subjects)} subjects.")

for subject in subjects:
    all_rows = []
    subject = subject.reload()
    print(subject.label)
    for session in subject.sessions():
        session = session.reload()
        acqs = [acq for acq in session.acquisitions() if "FISP" in acq.label or ("T2" in acq.label and "AXI" in acq.label)]
        print(session.label)
        temp_d = None
        for acquisition in acqs:
            print(acquisition.label)
            acquisition = acquisition.reload()
        
            json_f = [f for f in acquisition.files if f.name.endswith(".json")]
            if json_f:
                json_f = json_f[0]
                acquisition.download_file(json_f.name, json_f.name)
                with open(os.path.join(json_f.name),'r') as jf:
                    sw = json.load(jf)["SoftwareVersions"]
                    print("SW: ", sw)
                
            if "FISP" in acquisition.label:
                
                fisp_f = [f for f in acquisition.files if f.name.endswith(".dcm") or f.name.endswith(".dicom") or f.name.endswith(".zip")][0]
                
                acquisition.download_file(fisp_f.name, os.path.join(os.getcwd(), 'tmp',fisp_f.name))
                
                if fisp_f.name.endswith('zip'):
                    zip_path =  os.path.join(os.getcwd(), 'tmp',fisp_f.name)
                    extract_dir = os.path.join(os.getcwd(), 'tmp')
                    
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
        
                        for root, _, files in os.walk(extract_dir):
                            for file in files:
                                if file.lower().endswith(".dcm"):
                                    dcm_path = os.path.join(os.getcwd(), 'tmp', root, file)
                                    ds = pydicom.dcmread(dcm_path)
                                    temperature = ds.get("PatientComments", None)
                                    temp_d = re.findall(r'\d+', temperature)  
                                    
                                    #print("Temperature: ", temp_d)
                                    
                
                else:
                    ds = pydicom.dcmread(os.path.join(os.getcwd(), 'tmp', fisp_f.name))
                    temperature = ds.get("PatientComments", None)
                    temp_d = re.findall(r'\d+', temperature)                 
                    #print("Temperature: ", temp_d)
                                    


            
        asys = session.analyses
        filtered_analyses = [a for a in asys if "ghoststats" in a.label]
        for asys in filtered_analyses:
            files = asys.files
            for seg in ['T1', 'T2']:
                d = {'Site':subject.label, 'Session':session.label, 'PSNR':None}
                
                
                csv_files = [f for f in files if "PSNR" in f.name and f.name.endswith(".csv") and seg in f.name ]
                if csv_files:
                    try:
                        file = csv_files[0]
                        path = os.path.join(os.getcwd(),  'src','data', 'tmp', f'{subject.label}_{session.label}_{file.name}')
                        asys.download_file(file.name, path)
                        
                        df = pd.read_csv(path)
                        
                        d['PSNR'] = df.iloc[0].PSNR
                        d['MSE'] = df.iloc[0].MSE
                        d['NMI'] = df.iloc[0].NMI
                        d['SSIM'] = df.iloc[0].SSIM

                       
                        d['SoftwareVersion'] = sw
                        d['Temperature'] = temp_d

                        all_rows.append(d)
                        df = pd.DataFrame(all_rows)
                        

                    except Exception as e:
                        print("Exception caught ", e)
                        continue     
                
    if all_rows:
        df = pd.DataFrame.from_dict(all_rows)
        df = df.drop(df[df['PSNR'] == np.inf].index).reset_index()
        df['Temperature'] = df['Temperature'].apply(lambda v: v[0] if v else None)
        df[['Site','Session','MSE', 'PSNR', 'NMI', 'SSIM','SoftwareVersion','Temperature']].to_csv(os.path.join(os.getcwd(),  'src','data', f'PSNR_{subject.label}.csv'),index=False)
        


# List to hold each DataFrame
dfs = []
directory = os.path.join(os.getcwd(), 'src','data')
# Loop through each file in the directory
for filename in os.listdir(directory) :
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        dfs.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)

display(combined_df)
combined_df.to_csv(os.path.join(os.getcwd(),  'src','data', "all_phantoms.csv"),index=False)