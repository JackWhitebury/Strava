import requests
import openpyxl
import pandas as pd
from datetime import datetime

# Read Strava access token from a file
with open("strava_access_token.txt", "r") as token_file:
    strava_access_token = token_file.read().strip()

# Set up parameters for Strava API request
year = 2023
activities_url = "https://www.strava.com/api/v3/athlete/activities"
params = {
    'access_token': strava_access_token,
    'after': int(datetime(year, 1, 1).timestamp()),
    'before': int(datetime(year + 1, 1, 1).timestamp()),
    'per_page': 200,
}

# Placeholder for all activities
all_activities = []

# Fetch activities until no more pages
while True:
    # Make the Strava API request for activities
    response = requests.get(activities_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Convert the response to JSON format
        activities_data = response.json()

        # Break if there are no more activities
        if not activities_data:
            break

        # Filter activities marked as "commute"
        commute_activities = [activity for activity in activities_data if activity.get('commute')]

        # Append current page of activities to the list
        all_activities.extend(commute_activities)

        # Move to the next page by incrementing the 'page' parameter
        params['page'] = params.get('page', 1) + 1
    else:
        print(f"Error: {response.status_code}, {response.text}")
        break

# Create a DataFrame using pandas
df = pd.json_normalize(all_activities)

# Extract relevant columns
selected_columns = ['name', 'type', 'distance', 'moving_time', 'start_date', 'average_speed', 'total_elevation_gain']
df = df[selected_columns]

# Convert the 'start_date' column to datetime format and make it timezone unaware
df['start_date'] = pd.to_datetime(df['start_date']).dt.tz_localize(None)

# Add a new column for "Carbon CO2 kg Saved" and round to 2 decimal places
df['Carbon CO2 kg Saved'] = round((df['distance'] / 1000) * 0.21755, 2)

# Save the DataFrame to an Excel file
excel_file_path = f"strava_commute_activities_{year}.xlsx"
df.to_excel(excel_file_path, index=False, engine='openpyxl')

# Calculate and print the total savings
total_savings = df['Carbon CO2 kg Saved'].sum()
print(f"Total Carbon CO2 kg Saved: {total_savings} kg")

# Add a cell for "Total savings for the year" in Column I
with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    total_savings_sheet = pd.DataFrame({'Total savings for the year': [total_savings]})
    total_savings_sheet.to_excel(writer, sheet_name='Sheet1', startcol=8, index=False)


print(f"Commute activities for {year} saved to {excel_file_path}")
