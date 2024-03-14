import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Assume phantom_qa_data is the DataFrame you're working with

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',  # Basic Dash CSS
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css'  # Font Awesome for icons
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Assuming phantom_qa_data is available here and it's similar to the previously generated DataFrame
phantom_qa_data = pd.read_csv('data/phantom_qa_data.csv')

sites = phantom_qa_data['Site'].unique()
metrics = ['Scanner Frequency', 'Temperature', 'SNR', 'T1w', 'T2w', 'FSIP']  # Assuming these are the metrics

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # Sidebar
    html.Div([
        # Sidebar content including links with icons
        # Similar to the previous example
    ], style={
        'padding': '20px',
        'width': '20%',
        'background-color': '#001f3f',  # Navy color
        'position': 'fixed',
        'height': '100%',
        'overflow': 'auto'
    }),

    # Main Content Area
    html.Div(id='page-content', style={'margin-left': '25%', 'padding': '20px'})
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/qa':
        return html.Div([
            html.H3('QA Analysis'),
            dcc.Dropdown(id='site-dropdown', options=[{'label': site, 'value': site} for site in sites], value=sites[0]),
            dcc.Dropdown(id='metric-dropdown', options=[{'label': metric, 'value': metric} for metric in metrics], value=metrics[0]),
            dcc.Graph(id='time-series-chart'),
            dcc.Graph(id='boxplot-chart')
        ])
    # Handle other pages similarly
    else:
        return html.H3('Some other page')

@app.callback(
    [Output('time-series-chart', 'figure'),
     Output('boxplot-chart', 'figure')],
    [Input('site-dropdown', 'value'),
     Input('metric-dropdown', 'value')])
def update_charts(selected_site, selected_metric):
    filtered_data = phantom_qa_data[phantom_qa_data['Site'] == selected_site]
    time_series_fig = px.line(filtered_data, x='Timestamp', y=selected_metric, title=f'{selected_metric} Over Time for {selected_site}')
    boxplot_fig = px.box(phantom_qa_data, x='Site', y=selected_metric, title=f'{selected_metric} Distribution by Site')

    return time_series_fig, boxplot_fig

if __name__ == '__main__':
    app.run_server(debug=True)
