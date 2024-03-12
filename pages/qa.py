from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Example DataFrame for demonstration purposes
qa_data = pd.read_csv('data/phantom_qa_data.csv')
sites = qa_data['Site'].unique()
metrics = ['Scanner Frequency', 'Temperature', 'SNR', 'T1w', 'T2w', 'FSIP']  # Assuming these are the metrics

# QA Page layout
layout = html.Div([
    html.H3('QA Analysis'),
    dcc.Dropdown(id='qa-site-dropdown', options=[{'label': site, 'value': site} for site in qa_data['Site'].unique()], value='Site 1'),
    dcc.Dropdown(id='metric-dropdown', options=[{'label': metric, 'value': metric} for metric in metrics], value=metrics[0]),
    dcc.Graph(id='qa-time-series-graph'),
    dcc.Graph(id='qa-boxplot-graph')

])

# Callback registration function
def register_callbacks(app):
    @app.callback(
        [Output('qa-time-series-graph', 'figure'),  # First graph output
         Output('qa-boxplot-graph', 'figure')],    # Second graph output
        [Input('qa-site-dropdown', 'value'),       # First input
         Input('metric-dropdown', 'value')]        # Second input
    )
    def update_charts(selected_site, selected_metric):
        # Filter data for the selected site
        filtered_data = qa_data[qa_data['Site'] == selected_site]

        # Generate time series figure
        time_series_fig = px.line(filtered_data, x='Timestamp', y=selected_metric,
                                  title=f'{selected_metric} Over Time for {selected_site}')
        
        # Generate boxplot figure
        boxplot_fig = px.box(qa_data, x='Site', y=selected_metric,
                             title=f'{selected_metric} Distribution by Site')

        return time_series_fig, boxplot_fig