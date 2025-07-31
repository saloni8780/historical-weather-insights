import requests
import pandas as pd

def get_coordinates(city_name, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("OpenCage API error")
    data = response.json()
    if data['results']:
        lat = data['results'][0]['geometry']['lat']
        lng = data['results'][0]['geometry']['lng']
        return lat, lng
    else:
        raise ValueError(f"Could not find coordinates for '{city_name}'")

def fetch_weather_data(latitude, longitude, start_date, end_date, metrics):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(metrics),
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Weather API error")

    data = response.json()
    df = pd.DataFrame(data["daily"])
    df['time'] = pd.to_datetime(df['time'])

    rename_map = {
        'temperature_2m_max': 'temp_max',
        'temperature_2m_min': 'temp_min',
        'precipitation_sum': 'precipitation'
    }
    df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

    return df
