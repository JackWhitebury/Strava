import requests
import pandas as pd
from datetime import datetime

# Set your Strava access token here
strava_access_token = "*****"

# Set up parameters for Strava API request
year = 2023
activities_url = "https://www.strava.com/api/v3/athlete/activities"
params = {
    'access_token': strava_access_token,
    'after': int(datetime(year, 1, 1).timestamp()),
    'before': int(datetime(year + 1, 1, 1).timestamp()),
    'per_page': 200,
}

# Make the Strava API request for activities
response = requests.get(activities_url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Convert the response to JSON format
    activities_data = response.json()

    # Filter activities marked as "commute"
    commute_activities = [activity for activity in activities_data if activity.get('commute')]

    # Create a DataFrame using pandas
    df = pd.json_normalize(commute_activities)

    # Extract relevant columns
    selected_columns = ['name', 'type', 'distance', 'moving_time', 'start_date', 'average_speed', 'total_elevation_gain']
    df = df[selected_columns]

    # Convert the 'start_date' column to datetime format and make it timezone unaware
    df['start_date'] = pd.to_datetime(df['start_date']).dt.tz_localize(None)

    # Save the DataFrame to an Excel file
    excel_file_path = f"strava_commute_activities_{year}.xlsx"
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

    print(f"Commute activities for {year} saved to {excel_file_path}")
else:
    print(f"Error: {response.status_code}, {response.text}")
