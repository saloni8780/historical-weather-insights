# app.py

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("🌤️ Weather Data Dashboard")

# Sidebar input
st.sidebar.header("Input Parameters")
latitude = st.sidebar.number_input("Latitude", value=40.71)
longitude = st.sidebar.number_input("Longitude", value=-74.01)
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Metrics selection
metrics = st.sidebar.multiselect(
    "Select daily metrics",
    ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    default=["temperature_2m_max", "temperature_2m_min"]
)

# Fetch button
if st.sidebar.button("Fetch Weather Data"):
    with st.spinner("Fetching data from Open-Meteo..."):
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "daily": ",".join(metrics),
            "timezone": "auto"
        }
        response = requests.get(url, params=params)

        if response.status_code != 200:
            st.error("Failed to fetch data.")
        else:
            data = response.json()
            df = pd.DataFrame(data['daily'])
            df['time'] = pd.to_datetime(df['time'])

            # Rename columns for plotting
            rename_map = {
                'temperature_2m_max': 'temp_max',
                'temperature_2m_min': 'temp_min',
                'precipitation_sum': 'precipitation'
            }
            df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

            st.success("✅ Data fetched successfully!")

            # Show data
            st.subheader("Raw Weather Data")
            st.dataframe(df)

            # Save CSV (optional)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "weather_data.csv", "text/csv")

            # Visualizations
            st.subheader("📈 Visualizations")

            if "temp_max" in df.columns and "temp_min" in df.columns:
                df['month'] = df['time'].dt.to_period('M')
                monthly_avg = df.groupby('month')[['temp_max', 'temp_min']].mean().reset_index()
                monthly_avg['month'] = monthly_avg['month'].astype(str)

                st.subheader("📅 Monthly Average Temperature")
                st.line_chart(monthly_avg.set_index('month'))

            if 'precipitation' in df.columns:
    
                df['month_year'] = df['time'].dt.to_period('M').astype(str)
                monthly_precip = df.groupby('month_year')['precipitation'].sum().reset_index()
                st.subheader("🌧️ Total Monthly Precipitation")
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.bar(monthly_precip['month_year'], monthly_precip['precipitation'], color='skyblue')
                ax.set_xlabel('Month-Year')
                ax.set_ylabel('Total Precipitation (mm)')
                ax.set_title('Monthly Precipitation Over Time')
                plt.xticks(rotation=45)
                st.pyplot(fig)


            