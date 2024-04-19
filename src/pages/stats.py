# pages/stats.py
import dash
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from scipy.stats import pearsonr
import numpy as np
from dash import html, dcc, dash_table
import statsmodels.api as sm
import os
import flask 
from io import StringIO


# Load the synthetic data
def load_data():
    return pd.read_csv("data/participant_results_data.csv")

df = load_data()
unique_sites = df['site'].unique()

from dash import dcc, html

def site_filter_sidebar(unique_sites):
    """Returns a sidebar component for site filtering specific to the data analysis page."""
    return html.Div([
        html.H4("Site Filter", style={'color': 'white', 'marginTop': '20px'}),
        dcc.Dropdown(
            id='selected-site',
            options=[{'label': "All", 'value': "All"}] + [{'label': site, 'value': site} for site in unique_sites],
            value="All",
            style={'color': 'black'}
        )
    ], style={'padding': '20px', 'background-color': '#001f3f'})


# Create the layout for the stats page
layout = html.Div([
    html.H3("Study Descriptive Statistics"),
    # html.Br(),
    # html.Label("Please select a site to filter the data:"),
    # dcc.Dropdown(
    #     id='selected-site', 
    #     options=[{"label": "All", "value": "All"}] + [{"label": site, "value": site} for site in unique_sites], 
    #     value="All"),
    html.Label("Please choose a variable to display descriptive statistics:"),
    dcc.Dropdown(
        id='variable-dropdown',
        options=[{'label': var, 'value': var} for var in df.columns if var not in ['subjectID', 'sessionID', 'site', 'sex', 'group', 'Timestamp']],
        value='age'  # Default selection
    ),
    html.Br(),
    html.P(id='dropdown-output'),    
    html.Div(id='stats-output'),  # Placeholder for stats
    html.A('Download CSV', id='download-link', href=''),
    
])

# Callbacks registered in app.py that takes the app as an argument.
def register_callbacks(app):
    @app.callback(
        Output('stats-output', 'children'),
        Output('dropdown-output', 'children'),
        [Input('selected-site', 'value'), 
         Input('variable-dropdown', 'value')]
    )

    def update_output(selected_site, selected_variable):

        # Filter data based on selection
        filtered_data = df[df['site'] == selected_site] if selected_site != 'All' else df
        
        # Calculate descriptive statistics
        stats = filtered_data[selected_variable].describe().reset_index()
        stats.columns = ['Statistic', 'Value']
        # print(stats)
        # Generate table and download link components
        stats_table = dash_table.DataTable(
            data=stats.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in stats.columns],
            style_cell={'textAlign': 'left'},
        )

        # Generate descriptive text
        descriptive_text = html.P(f"Descriptive statistics for the selected variable: {selected_variable} (site: {selected_site})")

        return stats_table, descriptive_text
   
 
    def generate_csv(selected_site, selected_variable):
        filtered_data = df[df['site'] == selected_site] if selected_site != 'All' else df
        stats = filtered_data[selected_variable].describe().reset_index()
        stats.columns = ['Statistic', 'Value']

        output_df = pd.DataFrame(stats)
        csv_filename = 'my_data.csv'
        csv_file_path = os.path.join('/assets/', csv_filename)

        output_df.to_csv(csv_file_path, index=False)
        return html.A('Download Descriptive Statistics', href=f'/{csv_filename}', download=csv_filename)