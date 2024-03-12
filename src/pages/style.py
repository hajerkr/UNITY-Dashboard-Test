from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Sample data and figure
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length')

app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div([
        dcc.Graph(figure=fig, style={'padding': '10px'}),
        dcc.Dropdown(
            options=[{'label': i, 'value': i} for i in df['species'].unique()],
            value=df['species'].unique()[0],
            style={'width': '50%', 'padding': '10px'}
        ),
    ], style={
        'border': '2px solid #007BFF',
        'borderRadius': '15px',
        'padding': '20px',
        'margin': '10px',
        'boxShadow': '2px 2px 2px lightgrey'
    })
])

if __name__ == '__main__':
    app.run_server(debug=True)
