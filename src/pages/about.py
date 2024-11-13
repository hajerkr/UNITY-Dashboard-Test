from dash import html

# Define the layout for the About page
layout = html.Div([
    html.H2("About This App"),
    html.P([
        "This dashboard is designed to visualize MRI data across numerous sites,", html.Br(), 
        "providing insights into derived volume estimates and QA MRI data analysis. ", html.Br(),
        "The goal is to assist researchers and clinicians in identifying potential issues with the data and to provide a ", html.Br(),
        "comprehensive overview of the data quality across different sites."
    ]),
    
    html.H3("Contributors"),
    html.P("""
        The app was developed as part of the UNITY network to visualise QA data
    """),
    html.H3("Contact Us"),
    html.P("""
        If you have any questions or feedback, please contact niall.bourke@kcl.ac.uk
    """)
])

