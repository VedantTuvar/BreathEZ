import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from prophet.diagnostics import cross_validation, performance_metrics
from scipy.stats import zscore
import json
from prophet.serialize import model_to_json

# --- Configuration ---
FILE_PATH = "C:\\Users\\91940\\Downloads\\City500hour\\City500hour\\Final PA\\Ground NO2\\bergenno2.csv"
DATE_COLUMN = 'Date'
TARGET_COLUMN = 'Daily AQI Value'
FORECAST_HORIZON = 7  # in days

# --- Step 1: Load and Prepare Data ---
try:
    df = pd.read_csv(FILE_PATH, parse_dates=[DATE_COLUMN])
    df.set_index(DATE_COLUMN, inplace=True)
    df.index = pd.to_datetime(df.index, format='%d-%m-%Y', errors='coerce')
    df.sort_index(inplace=True)

    df_prophet = df.reset_index().rename(columns={DATE_COLUMN: 'ds', TARGET_COLUMN: 'y'})
    df_prophet = df_prophet[['ds', 'y']]

    print("\nData loaded successfully:")
    print(df_prophet.head())

except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit()

# --- Step 2: Outlier Handling ---
print("\n--- Step 2: Outlier Handling ---")
df_prophet['z_score_y'] = np.abs(zscore(df_prophet['y'], nan_policy='omit'))
outlier_threshold = 3
outliers = df_prophet[df_prophet['z_score_y'] > outlier_threshold]

if not outliers.empty:
    print(f"Detected {len(outliers)} outliers (Z > {outlier_threshold}). Replacing with median.")
    median_y = df_prophet[df_prophet['z_score_y'] <= outlier_threshold]['y'].median()
    df_prophet.loc[df_prophet['z_score_y'] > outlier_threshold, 'y'] = median_y
else:
    print("No significant outliers detected.")

df_prophet.drop('z_score_y', axis=1, inplace=True)

# --- Step 3: Feature Engineering ---
print("\n--- Step 3: Feature Engineering ---")
df_prophet['y_lag_2'] = df_prophet['y'].shift(2)
df_prophet['rolling_mean_3'] = df_prophet['y'].rolling(window=3).mean()
df_prophet['rolling_std_3'] = df_prophet['y'].rolling(window=3).std()

df_prophet.dropna(inplace=True)
print(df_prophet.head())

# --- Step 4: Prophet Model Training ---
print("\n--- Step 4: Prophet Model Training ---")
train_size = int(len(df_prophet) * 0.8)
train_df = df_prophet.iloc[:train_size]
test_df = df_prophet.iloc[train_size:]

model = Prophet(
    growth='linear',
    seasonality_mode='multiplicative',
    changepoint_prior_scale=0.1,
    seasonality_prior_scale=10.0,
    holidays_prior_scale=10.0,
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)

# Fit only on date & AQI (no regressors)
model.fit(train_df)
print("✅ Prophet model trained successfully.")

# --- Step 5: Model Evaluation ---
print("\n--- Step 5: Cross-Validation ---")
try:
    df_cv = cross_validation(
        model, initial=f'{FORECAST_HORIZON*2} days',
        period=f'{FORECAST_HORIZON} days', horizon=f'{FORECAST_HORIZON} days'
    )
    df_p = performance_metrics(df_cv)
    print("\nCross-validation performance:")
    print(df_p.head())
except Exception as e:
    print(f"⚠️ Cross-validation skipped due to error: {e}")

# --- Step 6: Forecast on Test Set ---
print("\n--- Step 6: Forecasting ---")
future = model.make_future_dataframe(periods=len(test_df), freq='D', include_history=False)
forecast = model.predict(future)

y_true = test_df['y'].values
y_pred = forecast['yhat'].values

mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))

print(f"\n📈 MAE: {mae:.2f}")
print(f"📉 RMSE: {rmse:.2f}")

# --- Step 7: Visualization ---
fig = model.plot(forecast)
plt.title("PM2.5 AQI Forecast")
plt.show()

fig2 = model.plot_components(forecast)
plt.title("Forecast Components")
plt.show()

# --- Step 8: Save Model ---
with open('BergenNo2_model.json', 'w') as fout:
    json.dump(model_to_json(model), fout)
print("💾 Model saved to 'BronxNo2_model.json'")
