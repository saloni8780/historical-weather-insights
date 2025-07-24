import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Function to get the coordinates for a city using OpenCage Geocoding API
def get_coordinates(city_name):
    api_key = 'YOUR_OPENCAGE_API_KEY'  # Replace with your OpenCage API key
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    if data['results']:
        lat = data['results'][0]['geometry']['lat']
        lng = data['results'][0]['geometry']['lng']
        return lat, lng
    else:
        raise ValueError(f"Could not find coordinates for {city_name}")

# Prompt for the city and get its coordinates
city_name = input("Enter the city name: ")
latitude, longitude = get_coordinates(city_name)
print(f"Coordinates for {city_name} are: Latitude = {latitude}, Longitude = {longitude}")

# Get start and end dates for weather data
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

# Prompt user to select which metrics to fetch
print("Available daily metrics: temperature_2m_max, temperature_2m_min, precipitation_sum")
daily_metrics = input("Enter comma-separated metrics to fetch: ")

# API URL and parameters for weather data
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": start_date,
    "end_date": end_date,
    "daily": daily_metrics,
    "timezone": "auto"
}

# Fetch data from Open-Meteo API
response = requests.get(url, params=params)

# Handle potential errors in the response
if response.status_code != 200:
    print("Error fetching data:", response.status_code, response.text)
    exit()

data = response.json()

# Check the columns in the returned data
df = pd.DataFrame(data['daily'])
print("Columns in the fetched data:", df.columns)

# Process the time column and fill missing values
df['time'] = pd.to_datetime(df['time'])
df.fillna(method='ffill', inplace=True)

# Rename columns dynamically
rename_map = {
    'temperature_2m_max': 'temp_max',
    'temperature_2m_min': 'temp_min',
    'precipitation_sum': 'precipitation'
}
df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

# Save the data to CSV and SQLite database
df.to_csv("weather_data.csv", index=False)
conn = sqlite3.connect("weather.db")
df.to_sql("daily_weather", conn, if_exists="replace", index=False)
conn.close()

# Display results
print("\nETL pipeline completed successfully. Output saved to 'weather_data.csv' and 'weather.db'.")

# Plot available metrics
plt.figure(figsize=(12, 6))
if 'temp_max' in df.columns:
    plt.plot(df['time'], df['temp_max'], label='Max Temperature', color='red')
if 'temp_min' in df.columns:
    plt.plot(df['time'], df['temp_min'], label='Min Temperature', color='blue')
if 'precipitation' in df.columns:
    plt.bar(df['time'], df['precipitation'], label='Precipitation', color='green')

plt.title(f'Weather Data for {city_name}')
plt.xlabel('Date')
plt.ylabel('Values')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Optional: Monthly Precipitation Visualization (if precipitation data is available)
if 'precipitation' in df.columns:
    df['month'] = df['time'].dt.month
    monthly_precip = df.groupby('month')['precipitation'].sum()

    plt.figure(figsize=(10, 6))
    monthly_precip.plot(kind='bar', color='purple')
    plt.title(f'Total Precipitation per Month for {city_name}')
    plt.xlabel('Month')
    plt.ylabel('Total Precipitation (mm)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
