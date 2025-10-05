from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from LoadModel import run_forecast
from datetime import datetime
import os

app = FastAPI(title="Air Quality Forecast API")

# ---------------- Forecast API ----------------
@app.get("/api/forecast")
def get_forecast(
    city: str = Query(..., description="City name, e.g., Bergen"),
    forecast_days: int = Query(2, ge=1, le=7, description="Number of forecast days (1–7)"),
    start_date: str = Query(datetime.today().strftime("%Y-%m-%d"), description="Start date in YYYY-MM-DD")
):
    """
    Returns air quality forecast for a given city and number of days.
    """
    try:
        df = run_forecast(city.lower(), start_date, forecast_days)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# ---------------- Figures API ----------------
@app.get("/api/figures")
def get_figure(city: str, pollutant: str):
    figure_path = f"Figures/{city}{pollutant}/Trends.png"
    if os.path.exists(figure_path):
        return FileResponse(figure_path)
    return {"error": "Figure not found"}

# ---------------- Model Info API ----------------
@app.get("/api/modelinfo")
def get_model_info():
    return {"models": os.listdir("Models")}

# ---------------- Upload CSV ----------------
from fastapi import UploadFile, File

@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    contents = await file.read()
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
    return {"message": f"File '{file.filename}' uploaded successfully"}
