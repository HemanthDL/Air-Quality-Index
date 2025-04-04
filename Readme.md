# Air Quality Index (AQI) Prediction

## 📌 Project Overview
This project aims to predict the Air Quality Index (AQI) for selected cities in India. The system leverages real-time air pollution data from OpenWeatherMap API and uses a **Random Forest Classifier** to predict AQI based on trained air quality datasets.

## 🏗️ Technology Stack
- **Backend:** Flask, Flask-CORS, Pandas, Requests
- **Frontend:** React, Axios, Framer Motion (for animations)
- **Machine Learning Model:** Random Forest Algorithm (trained on over a lakh data points)

## 🎯 Features
- Predict AQI for major Indian cities.
- Fetch real-time air quality data from OpenWeatherMap API.
- Display AQI along with the concentration of pollutants (CO, NO, NO₂, O₃, SO₂, PM2.5, PM10, NH₃).
- Interactive and dynamic frontend using React.

## 📊 Model Performance
- **Algorithm Used:** Random Forest Classifier
- **Dataset Size:** 100,000+ records
- **Accuracy:** *92%* (Specify the actual accuracy here)

## 🔧 Installation & Setup
### 1️⃣ Backend Setup

- To run random_forest.py

```sh
pip install pandas scikit-learn joblib
python random_forest.py
```

- To run prediction.py
```sh
pip install flask flask_cors requests pandas joblib

python prediction.py
```

### 2️⃣ Frontend Setup
```sh
cd frontend
npm install
npm run dev
```

## 🚀 API Endpoints
| Method | Endpoint     | Description |
|--------|-------------|-------------|
| GET    | /cities     | Returns the list of available cities |
| POST   | /predict    | Predicts AQI for the selected city |



---

