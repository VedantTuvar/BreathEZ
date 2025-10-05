'''import pandas as pd
from prophet.serialize import model_from_json
import json
from datetime import datetime
import os

# ------------------ Configuration ------------------
COUNTY_MODELS = {
    "bergen": {
        "no2": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Models\\NO2\\bergenno2_model.json",
        "o3": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Models\\O3\\BergenO3_model.json",
        "pm25": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Models\\PM2.5\\bergenPM2.5_model.json"
    },
    "morris": {
        "no2": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground NO2\\morrisno2.csv",
        "o3": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground O3\\morriso3.csv",
        "pm25": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground PM2.5\\PM2.0 morris.csv"
    },
    "bronx": {
        "no2": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground NO2\\bronxno2.csv",
        "o3": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground O3\\bronx03.csv",
        "pm25": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground PM2.5\\PM2.0 bronex.csv"
    }
}

# Example coordinates — update with real ones if needed
COUNTY_COORDS = {
    "bergen": (40.958, -74.075),
    "morris": (40.860, -74.545),
    "bronx": (40.8448, -73.8648)
}

# AQI category thresholds
def get_aqi_alert(aqi_value):
    if aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Moderate"
    elif aqi_value <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi_value <= 200:
        return "Unhealthy"
    else:
        return "Very Unhealthy or Hazardous"


# Dummy future weather regressors (replace later with real data)
def get_future_regressors(start_date, periods):
    future_dates = pd.date_range(start=start_date, periods=periods, freq='D')
    df = pd.DataFrame({
        "ds": future_dates,
        "Temperature": [20.0] * periods,
        "Humidity": [65.0] * periods
    })
    return df


# Load a Prophet model
def load_model(model_path):
    if not os.path.exists(model_path):
        print(f"⚠️ Model file not found: {model_path}")
        return None
    with open(model_path, "r") as f:
        return model_from_json(json.load(f))


# Main forecast function
def forecast_for_county(county_name, forecast_days):
    print(f"\n📍 Forecasting for {county_name.title()} County")

    lat, lon = COUNTY_COORDS[county_name]

    # Prepare regressors (same for all pollutant models)
    start_date = datetime.today().date()
    future_df = get_future_regressors(start_date, forecast_days)

    results = []

    # Predict each pollutant
    for pollutant, model_path in COUNTY_MODELS[county_name].items():
        model = load_model(model_path)
        if model is None:
            continue
        forecast = model.predict(future_df)
        results.append((pollutant, forecast[['ds', 'yhat']]))

    # Merge predictions
    merged = pd.DataFrame({"ds": future_df["ds"]})
    for pollutant, pred_df in results:
        merged = merged.merge(pred_df, on="ds", suffixes=("", f"_{pollutant}"))
        merged.rename(columns={"yhat": pollutant.upper()}, inplace=True)

    # Compute a rough AQI (if not provided)
    merged["AQI"] = merged[["NO2", "O3", "PM25"]].mean(axis=1)
    merged["Alert"] = merged["AQI"].apply(get_aqi_alert)
    merged["Temperature"] = future_df["Temperature"]
    merged["Humidity"] = future_df["Humidity"]

    # Print results
    print("\n--- Forecast Results ---")
    for _, row in merged.iterrows():
        print(f"\nDate: {row['ds'].date()}")
        print(f"County: {county_name.title()}")
        print(f"Lat: {lat}, Lon: {lon}")
        print(f"NO₂: {row['NO2']:.2f}")
        print(f"O₃: {row['O3']:.2f}")
        print(f"PM₂.₅: {row['PM25']:.2f}")
        print(f"Overall AQI: {row['AQI']:.2f}")
        print(f"AQI Alert: {row['Alert']}")
        print(f"Temperature: {row['Temperature']}°C")
        print(f"Humidity: {row['Humidity']}%")

    return merged


# ------------------ MAIN ------------------
if __name__ == "__main__":
    print("Available counties: Bergen, Morris, Bronx")
    while True:
        county = input("Enter county name: ").strip().lower()
        if county in COUNTY_MODELS:
            break
        else:
            print("Invalid county. Please choose from Bergen, Morris, Bronx.")

    while True:
        try:
            forecast_days = int(input("Enter forecast days (1–7): "))
            if 1 <= forecast_days <= 7:
                break
            else:
                print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    forecast_df = forecast_for_county(county, forecast_days)

    # Optionally save output
    out_path = f"forecast_{county}.csv"
    forecast_df.to_csv(out_path, index=False)
    print(f"\n✅ Forecast saved to {out_path}")

'''

import pandas as pd
from prophet.serialize import model_from_json
import json
from datetime import datetime, timedelta
import os

# ------------------ Configuration ------------------
COUNTY_MODELS = {
    "bergen": {
        "no2": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Models\\NO2\\BergenNo2_model.json" ,
        "o3": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Models\\O3\\BergenO3_model.json",
        "pm25": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Models\\PM2.5\\bergenPM2.5_model.json"
    },
    "morris": {
        "no2": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground NO2\\morrisno2.csv",
        "o3": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground O3\\morriso3.csv",
        "pm25": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground PM2.5\\PM2.0 morris.csv"
    }, 
    "bronx": {
        "no2": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground NO2\\bronxno2.csv",
        "o3": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground O3\\bronx03.csv",
        "pm25": "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground PM2.5\\PM2.0 bronex.csv"
    }
}

# Example coordinates — update if needed
COUNTY_COORDS = {
    "bergen": (40.958, -74.075),
    "morris": (40.860, -74.545),
    "bronx": (40.8448, -73.8648)
}

# AQI alert levels
def get_aqi_alert(aqi_value):
    if aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Moderate"
    elif aqi_value <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi_value <= 200:
        return "Unhealthy"
    else:
        return "Very Unhealthy or Hazardous"

# Future date generator
def get_future_dates(start_date, periods):
    return pd.DataFrame({"ds": pd.date_range(start=start_date, periods=periods, freq='D')})

# Load a Prophet model
def load_model(model_path):
    if not os.path.exists(model_path):
        print(f"⚠️ Model file not found: {model_path}")
        return None
    with open(model_path, "r") as f:
        return model_from_json(json.load(f))

# Forecast for one county
def forecast_for_county(county_name, start_date, forecast_days):
    print(f"\n📍 Forecasting for {county_name.title()} County")

    lat, lon = COUNTY_COORDS[county_name]
    future_df = get_future_dates(start_date, forecast_days)
    results = []

    # Predict each pollutant
    for pollutant, model_path in COUNTY_MODELS[county_name].items():
        model = load_model(model_path)
        if model is None:
            continue
        forecast = model.predict(future_df)
        results.append((pollutant, forecast[['ds', 'yhat']]))

    # Merge predictions
    merged = pd.DataFrame({"ds": future_df["ds"]})
    for pollutant, pred_df in results:
        merged = merged.merge(pred_df, on="ds", suffixes=("", f"_{pollutant}"))
        merged.rename(columns={"yhat": pollutant.upper()}, inplace=True)

    # Compute overall AQI and alert
    merged["AQI"] = merged[["NO2", "O3", "PM25"]].mean(axis=1)
    merged["Alert"] = merged["AQI"].apply(get_aqi_alert)

    # Print results
    print("\n--- Forecast Results ---")
    for _, row in merged.iterrows():
        print(f"\nDate: {row['ds'].date()}")
        print(f"County: {county_name.title()}")
        print(f"Lat: {lat}, Lon: {lon}")
        print(f"NO₂: {row['NO2']:.2f}")
        print(f"O₃: {row['O3']:.2f}")
        print(f"PM₂.₅: {row['PM25']:.2f}")
        print(f"Overall AQI: {row['AQI']:.2f}")
        print(f"AQI Alert: {row['Alert']}")

    return merged

# ------------------ MAIN ------------------
if __name__ == "__main__":
    print("Available counties: Bergen, Morris, Bronx")

    # Get county
    while True:
        county = input("Enter county name: ").strip().lower()
        if county in COUNTY_MODELS:
            break
        print("Invalid county. Please choose from Bergen, Morris, Bronx.")

    # Get start date
    while True:
        start_date_str = input("Enter start date for forecast (YYYY-MM-DD): ")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")

    # Get forecast days
    while True:
        try:
            forecast_days = int(input("Enter number of forecast days (1–7): "))
            if 1 <= forecast_days <= 7:
                break
            else:
                print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Run forecast
    forecast_df = forecast_for_county(county, start_date, forecast_days)

    # Save to CSV
    out_path = f"forecast_{county}_{start_date}.csv"
    forecast_df.to_csv(out_path, index=False)
    print(f"\n✅ Forecast saved to {out_path}")

def run_forecast(county: str, start_date: str, forecast_days: int):
    """
    Wrapper for FastAPI.
    county: "bergen", "morris", or "bronx"
    start_date: string YYYY-MM-DD
    forecast_days: int (1–7)
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    df = forecast_for_county(county.lower(), start_date, forecast_days)
    return df