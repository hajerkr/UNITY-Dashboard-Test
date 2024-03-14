from dash import html

# Define the layout for the About page
layout = html.Div([
    html.H2("About This App"),
    html.P("""
        This dashboard is designed to visualize MRI data across numerous sites, 
        providing insights into derived volume estimates and QA MRI data analysis. 
        The goal is to assist researchers
        and clinicians in identifying potential issues with the data and to provide a 
        comprehensive overview of the data quality across different sites.
           """
    ),
    html.H3("Contributors"),
    html.P("""
        This app was developed by Niall Bourke from Metacognition. 
        The app was developed as part of the UNITY project for MRI analysis at King's College London, funded by the Bill and Malinda Gates Foundation.
    """),
    html.H3("Contact Us"),
    html.P("""
        If you have any questions or feedback, please contact [niall.bourke@kcl.ac.uk].
    """)
])

