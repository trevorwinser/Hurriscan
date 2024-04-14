# HurriScan ![HurriScane Logo](/server/static/images/new-logo.png) - [Presentation Video](https://www.youtube.com/watch?v=DuKt8fv_xJ4)
## Project Description
HurriScan is an advanced hurricane tracking and scanning system designed to offer unparalleled
insights into hurricane activities in the Pacific Ocean. The platform utilizes wind and temperature
data from a network of strategically positioned buoys throughout the equatorial Pacific,
providing hurricane tracking, detailed forecasts, and potential impact assessments.

HurriScan aims to cater to a diverse range of users, including meteorologists, climate
researchers, companies engaged in shipping goods across the Pacific, and media outlets alerting
coastal cities. The platform accomplishes this by delivering an interactive oceanographic data
map, machine-learning-powered predictions, helpful data visualizations, and timely alerts. These
features empower users to stay safe and well-informed about natural events and changes
occurring throughout the Pacific.

## Dataset
We will be using the **El Niño** dataset collected with the Tropical Atmosphere Ocean (TAO) array which was developed by the international Tropical Ocean Global Atmosphere (TOGA) program.
The data set contains oceanographic and surface meteorological readings taken from a series of buoys positioned throughout the equatorial Pacific.

Link to the dataset: https://archive.ics.uci.edu/dataset/122/el+nino
DOI Link: https://doi.org/10.24432/C5WG62
This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license.

## User Dashboard
Leaflet Heat Map: https://www.patrick-wied.at/static/heatmapjs/plugin-leaflet-layer.htmlwied.at/static/heatmapjs/plugin-leaflet-layer.html

## Non-Functional Requirements
- Login and register page ensure valid credentials
- User dashboard displays geographical and chart information
- Alert preferences allow personalized notification configuration
- Predictions page has a responsive layout with clear indications of what the user can interact with.
- Admin dashboard displays only the user information to admins

## Functional Requirements
- User credentials verified via the SQLite database for the login and register pages
- Hurricane data from SQLite database loaded onto maps and graphs/
- User information loaded onto admin dashboard and handling of alert creation

## Step by Step Setup
- Python 3.x
- pip (Python package installer)
- Git Repo cloned onto your machine trevorwinser/Infinite-Loopers (github.com)
Setting Up the Virtual Environment
To set up a virtual environment enter the following in the Vscode CLI:
1. Navigate to the project directory: cd server
2. Create a virtual environment named `venv` python -m venv venv
3. Activate the virtual environment: 
On Windows:
.\venv\Scripts\activate
On macOS and Linux:
source venv/bin/activate
Installing Dependencies
After activating the virtual environment, install the project dependencies by entering the following command in the CLI:
pip install -r ../requirements.txt
This command reads the `requirements.txt` file from the project directory and installs all the necessary packages.
Setting Up the Database
1. Ensure SQLite is installed on your machine (comes pre-installed with Python).
2. Navigate to the project root directory and run the following command:
python sqlite_setup.py
Running the Flask Application
1. Ensure your virtual environment is activated.
2. Set the environment variable for the Flask application:
- On Windows:
set FLASK_APP=app.py
- On macOS and Linux:
export FLASK_APP=app.py
3. Run the Flask development server:
flask run
4. Open a web browser and navigate to http://127.0.0.1:5000/ to view the application.
