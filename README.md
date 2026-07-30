# EV Charging Station Health Monitoring

## Overview

EV Charging Station Health Monitoring is a FastAPI-based backend application that monitors the health of electric vehicle charging stations using telemetry data and machine learning. The system stores charging station information, telemetry records, maintenance history, and predicts whether a charging station is healthy or likely to fail.

---

## Features

- User Management
- Charging Station Management
- Telemetry Data Management
- Maintenance Record Management
- Machine Learning Failure Prediction
- RESTful APIs
- Swagger API Documentation
- SQLite Database

---

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Scikit-learn
- Pandas
- Joblib
- Uvicorn

---

## Project Structure

```
backend/
│
├── api/
│   ├── main.py
│   ├── routes/
│
├── database/
│   ├── database.py
│   ├── models.py
│
├── schemas/
│
├── ml/
│   ├── train_model.py
│   ├── predict.py
│   ├── model.pkl
│
├── seed_data.py
│
requirements.txt
README.md
```

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd EV_Charging_Station_Health_Monitoring
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
uvicorn backend.api.main:app --reload
```

---

## API Documentation

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Available APIs

### Users

- POST /users
- GET /users/all

### Charging Stations

- POST /charging-stations
- GET /charging-stations/all

### Telemetry

- POST /telemetry
- GET /telemetry/all

### Maintenance

- POST /maintenance
- GET /maintenance/all

### Prediction

- POST /predict

---

## Machine Learning Model

The application uses a Random Forest Classifier trained on:

- Temperature
- Humidity
- Power Consumption

The model predicts:

- Charging Station Healthy
- Failure Expected

---

## Sample Prediction Request

```json
{
    "temperature": 28,
    "humidity": 40,
    "power_consumption": 12
}
```

### Sample Response

```json
{
    "prediction": "Charging Station Healthy"
}
```

---

## Future Enhancements

- Real-time IoT sensor integration
- Email alerts for failures
- Dashboard and analytics
- Cloud deployment
- Historical performance visualization

---

## Author

**KADALI PRASAMHITA**
