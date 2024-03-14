# UNITY MRI Dashbaord Application Overview

This repository contains a Dash application designed for data analysis and visualization. Leveraging Dash and Dash Bootstrap Components, it offers a user-friendly web interface with multiple pages including an Overview, Data Analysis, Data Visualization, QA, and an About section. 

## Features
Modular Page Layout: Includes separate pages for different functionalities (QA, Data Visualization, Data Analysis, and an About section) to keep the content organized.
Navigation Sidebar: A responsive sidebar with Font Awesome icons for intuitive navigation across different sections of the application.
Dynamic Content Loading: Utilizes Dash's callback mechanism to dynamically load content based on user navigation.
External Stylesheets: Incorporates Dash CSS and Font Awesome for styling and icons.
Deployment Ready: Includes a server variable to facilitate easy deployment on platforms like Heroku.

## Usage
Navigate through the application using the sidebar links. Each section provides distinct functionalities:

Overview: A homepage with introductory information.
Data Analysis: Tools and interfaces for analyzing data.
Data Visualization: Visual tools for data representation.
QA: A section dedicated to questions and answers.
About: Information about the application and its developers.

## Development
Developed in vscode with Github integration
To run the application locally, clone the repository and install the required packages using pip:
```bash
pip install -r requirements.txt
```
Run the application using the following command:
```bash
python app.py
```
The application will be accessible at http://localhost:8050/ by default.

## Structure
The application is organized into the following directories:

assets: Contains external stylesheets and other static files.
pages: Contains separate Python modules for different pages of the application.
tests: Contains test cases for the application.
app.py: The main application file that defines the layout and callbacks for the Dash application.

**To add or modify tests:**
Create a new Python module under the tests directory.
Define your test cases within this module.
Import your module in app.py and add a new test suite if necessary.


**To add or modify pages:**
Create a new Python module under the pages directory.
Define your page layout and callbacks within this module.
Import your module in app.py and add a new navigation link in the sidebar if necessary.
Register any callbacks defined in your module at the bottom of app.py.

## Deployment
The application is deployment-ready and can be easily deployed on platforms like Heroku or render. The server variable in Procfile is configured to facilitate deployment on render. To deploy the application on render, follow these steps:

Create a new web service on render and connect it to your GitHub repository.
Configure the web service with the following settings:
Build Command: pip install -r requirements.txt
Push any updates to your repository.
To trigger a new build and deployment click Manual Deploy > Deploy latest commit.
The application will be accessible at the URL provided by render after the deployment is complete
**Note:** The free version spins down after inactivity so may take up to a minute to load up again.


For Heroku, you can follow the official guide to deploy a Dash application on Heroku.


## Contributing
Contributions to this project are welcome. Please ensure to follow the existing coding style and add or update tests as necessary. For substantial changes, please open an issue first to discuss what you would like to change.

### License
MIT