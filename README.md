# 🌦️ Weather Insights Dashboard

**Get historical weather trends for any city — fast, visual, and interactive.**

---

## 🔍 What is this?

A simple Streamlit web app that shows **past weather data** (like temperature and rainfall) for **any city in the world**.

Great for:

* 🌱 Farmers checking past rainfall
* 🧳 Travelers planning trips
* 🏗️ Engineers analyzing weather for projects
* 🧑‍🏫 Students learning data visualization

---

## 🎯 What it does

* Enter a **city name** (e.g., Mumbai)
* Pick a **date range**
* Choose weather data like:

  * Max Temperature
  * Min Temperature
  * Rainfall (precipitation)
* Get clear charts showing:

  * 📈 Temperature over time
  * 🌧️ Rainfall per month

---

## 🧩 How to Use

### 1. Clone the project

```bash
git clone https://github.com/saloni8780/historical-weather-insights.git
cd historical-weather-insights
```

### 2. Install Python packages

```bash
pip install -r requirements.txt
```

### 3. Add your API key

Create this file: `.streamlit/secrets.toml`

```toml
[general]
OPENCAGE_API_KEY = "your_opencage_api_key"
```

> ✅ This file is hidden from GitHub automatically!

### 4. Run the app

```bash
streamlit run weather_dashboard.py
```

Then open `http://localhost:8501` in your browser!

---

## 📦 Tech Used

* **Streamlit** – to build the web app
* **OpenCage API** – to get city coordinates
* **Open-Meteo API** – to fetch historical weather
* **Pandas + Matplotlib** – to process & plot data

---

## 💡 Why two files?

* `weather_pipeline.py` – handles the data logic (API + processing)
* `weather_dashboard.py` – handles the UI (Streamlit layout + input)

This makes it easy to reuse the pipeline elsewhere!
