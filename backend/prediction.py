from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import requests
import pickle

# Load the pre-trained model using pickle
def load_model(model_path='random_forest_model.pkl'):
    with open(model_path, 'rb') as model_file:
        return pickle.load(model_file)

rf_model = load_model('random_forest_model.pkl')

# Function to fetch real-time air pollution data using OpenWeatherMap API
def fetch_real_time_data(api_key, lat, lon):
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
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

# Initialize Flask app
app = Flask(__name__)

CORS(app)


# Define city to coordinates mapping (You can expand this mapping for more cities)
city_coordinates = {
    'Bengaluru': {'lat': 12.9716, 'lon': 77.5946},
    'Hassan': {'lat': 13.0033, 'lon': 76.1004},
    'Mysuru': {'lat': 12.2958, 'lon': 76.6394},
    'Mangaluru': {'lat': 12.9141, 'lon': 74.8560},
    'Kolar': {'lat': 13.1291, 'lon': 78.1285}
}

# Route to get AQI prediction and composition for a selected city
@app.route('/predict', methods=['POST'])
def predict_aqi():
    # Get city name from the request
    data = request.get_json()
    city = data.get('city')

    if city not in city_coordinates:
        return jsonify({"error": "City not found"}), 404
    
    lat, lon = city_coordinates[city]['lat'], city_coordinates[city]['lon']

    # Fetch the real-time air quality data for the city
    try:
        api_key = '770f56fec010799b22416015a76a31c5'  # Replace with your OpenWeatherMap API key
        real_time_data = fetch_real_time_data(api_key, lat, lon)
        
        # Prepare the data for prediction
        real_time_df = pd.DataFrame([real_time_data])
        real_time_df = real_time_df[['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']]
        
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
