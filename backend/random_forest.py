import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump


# Loading the data 
def load_data(filename):
    data = pd.read_csv(filename)
    X = data[['components.co', 'components.no', 'components.no2', 'components.o3', 'components.so2', 'components.pm2_5', 'components.pm10', 'components.nh3']]
    y = data['main.aqi']
    return X, y


# Training using random forest algorithm
def train_model(X, y):
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42,n_jobs=1)
    rf_model.fit(X, y)
    return rf_model


#saving the trained data as pkl file
def save_model(model, filename):
    dump(model, filename)

X_train, y_train = load_data('API_dataset_allcities.csv')

rf_model = train_model(X_train, y_train)

save_model(rf_model, 'random_forest_algo_model.pkl')

print("Model trained and saved!")
