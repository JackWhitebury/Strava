import json
import requests


def get_strava_config():
    with open(STRAVA_CONFIG_FILE, 'r') as file:
        config = json.loads(file.read().strip())
    return config

def update_strava_config(config):
    with open(STRAVA_CONFIG_FILE, 'w') as file:
        file.write(json.dumps(config, indent=4, sort_keys=True))


STRAVA_CONFIG_FILE = 'config/strava-config.json'
strava_config = get_strava_config()


if __name__ == '__main__':
    # Set up parameters for Strava API request
    api_url = 'https://www.strava.com/oauth/token'
    params = {
        'client_id': strava_config['client_id'],
        'client_secret': strava_config['client_secret'],
        'refresh_token': strava_config['refresh_token'],
        'grant_type': 'refresh_token'
    }

    # Fetch the refresh token
    try:
        response = requests.post(api_url, params=params)

        if response.status_code == 200:
            api_response = response.json()

            print(f"old access_token: {strava_config['access_token']}")
            print(f"old refresh_token: {strava_config['refresh_token']}")

            strava_config['access_token'] = api_response['access_token']
            strava_config['refresh_token'] = api_response['refresh_token']
            update_strava_config(strava_config)

            print(f"new access_token: {strava_config['access_token']}")
            print(f"new refresh_token: {strava_config['refresh_token']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print("Exception when calling AthletesApi->getStats: %s\n" % e)
