from dash import html

# Define the layout for the About page
layout = html.Div([
    html.H1("Welcome to the UNITY MRI Dashboard"),
    html.P("""
        This dashboard is designed to visualize MRI data across numerous sites, 
        providing insights into derived volume estimates and QA MRI data analysis. 
        The goal is to assist researchers
        and clinicians in identifying potential issues with the data and to provide a 
        comprehensive overview of the data quality across different sites.
           """
    ),

    html.H3("Disclaimer"),
    html.P("""
        Loaded data is synthetic and does not represent real scanner data.
        No warranty is provided for the accuracy of the results.
        The data is generated for educational purposes only.
    """)
])

