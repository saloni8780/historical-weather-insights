import streamlit as st
import matplotlib.pyplot as plt
from weather_pipeline import get_coordinates, fetch_weather_data

st.title("🌤️ Weather Data Dashboard")
st.sidebar.header("Input Parameters")

city_name = st.sidebar.text_input("City Name")

if city_name:
    try:
        api_key = st.secrets["OPENCAGE_API_KEY"]
        latitude, longitude = get_coordinates(city_name, api_key)
    except Exception as e:
        st.error(str(e))
        st.stop()
else:
    latitude = st.sidebar.number_input("Latitude", value=40.71)
    longitude = st.sidebar.number_input("Longitude", value=-74.01)

start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

metrics = st.sidebar.multiselect(
    "Select daily metrics",
    ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    default=["temperature_2m_max", "temperature_2m_min"]
)

if st.sidebar.button("Fetch Weather Data"):
    if not metrics:
        st.warning("Please select at least one metric.")
        st.stop()

    with st.spinner("Fetching data from Open-Meteo..."):
        try:
            df = fetch_weather_data(latitude, longitude, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), metrics)
        except Exception as e:
            st.error(str(e))
            st.stop()

        st.success("✅ Data fetched successfully!")
        st.subheader("📋 Raw Weather Data")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "weather_data.csv", "text/csv")

        st.subheader("📈 Visualizations")

        if "temp_max" in df.columns and "temp_min" in df.columns:
            df['month'] = df['time'].dt.to_period('M')
            monthly_avg = df.groupby('month')[['temp_max', 'temp_min']].mean().reset_index()
            monthly_avg['month'] = monthly_avg['month'].astype(str)
            st.line_chart(monthly_avg.set_index('month'))

        if 'precipitation' in df.columns:
            df['month_year'] = df['time'].dt.to_period('M').astype(str)
            monthly_precip = df.groupby('month_year')['precipitation'].sum().reset_index()
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(monthly_precip['month_year'], monthly_precip['precipitation'], color='skyblue')
            ax.set_xlabel('Month-Year')
            ax.set_ylabel('Total Precipitation (mm)')
            ax.set_title('Monthly Precipitation Over Time')
            plt.xticks(rotation=45)
            st.pyplot(fig)
