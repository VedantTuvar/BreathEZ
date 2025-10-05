# BreathEZ

## 1. Project Summary

**BreathEZ** is a user-centric web application designed to forecast local air quality and proactively alert users to potential health risks stemming from air pollution exposure. By seamlessly integrating **NASA's Tropospheric Emissions: Monitoring of Pollution (TEMPO)** satellite data with diverse ground-based measurements and weather information, the app provides a comprehensive, near real-time, and localized view of air quality across North America. Our goal is to translate complex Earth science data into easily digestible, actionable information to improve public health outcomes and environmental awareness.

---

## 2. Core Objectives


1.  **Data Fusion and Integration:** Build a robust backend to ingest and synthesize near real-time data from TEMPO, ground stations (Pandora, OpenAQ), and meteorological services.
2.  **Localized Air Quality Forecasting:** Develop a machine learning (ML) model that generates hyperlocal air quality predictions (24-48 hours) by combining multi-source data.
3.  **Proactive Alert System:** Implement timely, customizable notifications when air quality is forecasted to reach unhealthy levels based on the Air Quality Index (AQI).

---

## 3. Key Capabilities

### 🗺️ Data Integration and Validatio
* **Real-Time Validation:** Feature to compare TEMPO satellite column densities against co-located ground-based measurements (e.g., Pandora) for data quality assessment.

### 📈 Forecasting and Alerts
* **Hyperlocal Forecast Grid:** High-resolution map visualizing air quality forecasts down to specific neighborhoods.
* **Customizable Health Alerts:** User-defined alert thresholds based on sensitive groups and preferred pollutants.
* **Historical Trends:** Interactive charts for viewing seasonal and annual air quality trends.

---

## 4. Technology Stack and Architecture

| Component | Technology/Tool | Purpose |
| :--- | :--- | :--- |
| **Frontend** | `HTML, CSS and JS` | Modern, responsive web interface; user-centric design. |
| **Backend/API** | `Python (FastAPI)` | High-speed data processing and API serving. |

---

## 5. Data and Resources Used

| Data Source | Data Type | Access Note |
| :--- | :--- | :--- |
| **TEMPO Mission** | Near Real-Time L2 Products | NASA TEMPO Data Access. |
| **OpenAQ** | Global Ground-Based PM and Gas Measurements | OpenAQ API. |

---

## 6. Licensing

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

***BreathEZ***
