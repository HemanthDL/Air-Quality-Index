import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

def load_data(filename):
    data = pd.read_csv(filename)
    X = data[['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']]
    y = data['aqi']
    return X, y

def train_model(X, y):
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X, y)
    return rf_model

def save_model(model, filename):
    with open(filename, 'wb') as model_file:
        pickle.dump(model, model_file)

X_train, y_train = load_data('KACities.csv')

rf_model = train_model(X_train, y_train)

save_model(rf_model, 'random_forest_model.pkl')

print("Model trained and saved!")
