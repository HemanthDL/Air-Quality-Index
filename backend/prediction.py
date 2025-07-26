from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import requests
from joblib import load
import os
from dotenv import load_dotenv

load_dotenv()

pkl_local_path = os.environ.get("PKL_LOCAL_PATH")
open_weather_map_api = os.environ.get("OPEN_WEATHER_API_URL")

# Load the pre-trained model
def load_model(model_path):
    return load(model_path)


# Function to fetch real-time air pollution data using OpenWeatherMap API
def fetch_real_time_data(api_key, lat, lon):
    url = open_weather_map_api
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'list' in data and len(data['list']) > 0:
        air_quality_data = data['list'][0]['components']
        return air_quality_data
    else:
        raise ValueError("No data available for the specified location")


rf_model = load_model(pkl_local_path)
# rf_model = load_model('random_forest_algo_model.pkl')


app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/*": {"origins": "*"}})


city_coordinates = {
    "Hassan": {"lat": 13.0033, "lon": 76.1004},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mysuru": {"lat": 12.2958, "lon": 76.6394},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Pune": {"lat": 18.5204, "lon": 73.8567},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462},
    "Indore": {"lat": 22.7196, "lon": 75.8577},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558},
    "Surat": {"lat": 21.1702, "lon": 72.8311},
    "Vadodara": {"lat": 22.3072, "lon": 73.1812},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126},
    "Patna": {"lat": 25.5941, "lon": 85.1376},
    "Ranchi": {"lat": 23.3441, "lon": 85.3096},
    "Madurai": {"lat": 9.9250, "lon": 78.1193},
    "Agra": {"lat": 27.1767, "lon": 78.0081},
    "Varanasi": {"lat": 25.3176, "lon": 82.9739},
    "Ludhiana": {"lat": 30.9008, "lon": 75.8573},
    "Amritsar": {"lat": 31.5497, "lon": 74.3436},
    "Faridabad": {"lat": 28.4089, "lon": 77.3178}
}

@app.route('/cities',methods=['GET'])
def get_cities():
    # cities = city_coordinates.keys()
    # return jsonify({
    #     cities : cities
    # })
    return jsonify({"cities": list(city_coordinates.keys())})


# Route to get AQI prediction and composition for a selected city
@app.route('/predict', methods=['POST'])
def predict_aqi():
    data = request.get_json()
    city = data.get('city')

    if city not in city_coordinates:
        return jsonify({"error": "City not found"}), 404
    
    lat, lon = city_coordinates[city]['lat'], city_coordinates[city]['lon']

    try:
        api_key = os.environ.get("OPEN_WEATHER_API_KEY")
        print("API key",api_key)
        real_time_data = fetch_real_time_data(api_key, lat, lon)
        
        # Prepare the data for prediction
        real_time_df = pd.DataFrame([real_time_data])
        real_time_df = real_time_df.rename(columns={
            'co': 'components.co',
            'no': 'components.no',
            'no2': 'components.no2',
            'o3': 'components.o3',
            'so2': 'components.so2',
            'pm2_5': 'components.pm2_5',
            'pm10': 'components.pm10',
            'nh3': 'components.nh3'
        })
        real_time_df = real_time_df[['components.co', 'components.no', 'components.no2', 'components.o3','components.so2', 'components.pm2_5', 'components.pm10', 'components.nh3']]
        
        # Predict AQI Class using the loaded RandomForestClassifier
        prediction_rf = rf_model.predict(real_time_df)
        
        # Prepare air quality composition details
        composition_data = {
            'co': real_time_data.get('co'),
            'no': real_time_data.get('no'),
            'no2': real_time_data.get('no2'),
            'o3': real_time_data.get('o3'),
            'so2': real_time_data.get('so2'),
            'pm2_5': real_time_data.get('pm2_5'),
            'pm10': real_time_data.get('pm10'),
            'nh3': real_time_data.get('nh3')
        }
        
        # Return the AQI prediction and composition as JSON
        return jsonify({
            'aqi': int(prediction_rf[0]), 
            'composition': composition_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
