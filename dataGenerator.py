import pandas as pd
import numpy as np

# Setting random seed for reproducibility
np.random.seed(42)

# Step 1: Generate Synthetic Phantom QA Data
# Simulating some basic data for 5 sites over a year
sites = ['Site_' + str(i) for i in range(1, 6)]
timestamps_qa = pd.date_range(start='2023-01-01', end='2023-12-31', freq='W')
scanner_frequency = np.random.uniform(1.5, 3.0, size=len(timestamps_qa) * len(sites))
temperature = np.random.uniform(18, 22, size=len(timestamps_qa) * len(sites))
snr = np.random.uniform(20, 40, size=len(timestamps_qa) * len(sites))
t1w = np.random.uniform(0.5, 2.0, size=len(timestamps_qa) * len(sites))
t2w = np.random.uniform(40, 80, size=len(timestamps_qa) * len(sites))
fsip = np.random.uniform(0.8, 1.0, size=len(timestamps_qa) * len(sites))

phantom_qa_data = pd.DataFrame({
    'Site': np.tile(sites, len(timestamps_qa)),
    'Timestamp': np.repeat(timestamps_qa, len(sites)),
    'Scanner Frequency': scanner_frequency,
    'Temperature': temperature,
    'SNR': snr,
    'T1w': t1w,
    'T2w': t2w,
    'FSIP': fsip
})

# Step 2: Generate Synthetic Participant Results Data
n_participants = 200
participant_ids = ['P' + str(i).zfill(3) for i in range(n_participants)]
session_ids = ['S1', 'S2']  # Assuming each participant has two sessions
ages = np.random.randint(20, 81, size=n_participants)
sex = np.random.choice(['Male', 'Female'], size=n_participants)
groups = np.random.choice(['Control', 'Experimental'], size=n_participants)
sites_participants = np.random.choice(sites, size=n_participants)
timestamp_participants = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
timestamp_participants = np.random.choice(timestamp_participants, size=n_participants)
ticv = ages * np.random.uniform(1400, 1500, size=n_participants) / 30
wm_vol = ages * np.random.uniform(400, 450, size=n_participants) / 30
gm_vol = ages * np.random.uniform(600, 650, size=n_participants) / 30
csf_vol = ages * np.random.uniform(100, 150, size=n_participants) / 30
gsed = np.random.uniform(0.8, 1.2, size=n_participants)

# Adjust for age pattern and sex differences
for i in range(n_participants):
    if ages[i] > 30 and ages[i] <= 65:
        factor = np.random.uniform(0.95, 1.05)
        ticv[i] *= factor
        wm_vol[i] *= factor
        gm_vol[i] *= factor
        csf_vol[i] *= factor
    elif ages[i] > 65:
        factor = np.random.uniform(0.9, 0.95)
        ticv[i] *= factor
        wm_vol[i] *= factor
        gm_vol[i] *= factor
        csf_vol[i] *= factor
    if sex[i] == 'Female':
        ticv[i] *= 0.97
        wm_vol[i] *= 0.97
        gm_vol[i] *= 0.97
        csf_vol[i] *= 0.97

participant_results_data = pd.DataFrame({
    'Subject ID': np.repeat(participant_ids, 2),
    'Session ID': np.tile(session_ids, n_participants),
    'Timestamp': np.tile(timestamp_participants, 2),
    'Age': np.repeat(ages, 2),
    'Sex': np.repeat(sex, 2),
    'Group': np.repeat(groups, 2),
    'Site': np.repeat(sites_participants, 2),
    'TICV': np.tile(ticv, 2),
    'wm_vol': np.tile(wm_vol, 2),
    'gm_vol': np.tile(gm_vol, 2),
    'csf_vol': np.tile(csf_vol, 2),
    'GSED': np.tile(gsed, 2)
})

phantom_qa_data.head(), participant_results_data.head()

phantom_qa_data.to_csv('data/phantom_qa_data.csv', index=False)
participant_results_data.to_csv('data/participant_results_data.csv', index=False)
