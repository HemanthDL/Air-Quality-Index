# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# # from dotenv import load_dotenv
# import os

# # load_dotenv()

# # all_cities_dataset_path = os.environ.get("ALL_CITIES_DATASET_PATH")
# all_cities_dataset_path = "API_dataset_allcities.csv"

# def load_data(filename):
#     data = pd.read_csv(filename)
#     X = data[['components.co', 'components.no', 'components.no2', 'components.o3',
#               'components.so2', 'components.pm2_5', 'components.pm10', 'components.nh3']]
#     y = data['main.aqi']
#     return X, y

# def evaluate_model(X, y, test_size):
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=test_size, random_state=42, stratify=y
#     )
#     model = RandomForestClassifier(n_estimators=100, random_state=42)
#     model.fit(X_train, y_train)
#     predictions = model.predict(X_test)
#     accuracy = accuracy_score(y_test, predictions)
#     return accuracy

# if __name__ == "__main__":
#     X, y = load_data(all_cities_dataset_path)
    
#     # Train - Test split 
#     splits = [0.3, 0.2, 0.1]  

#     for test_size in splits:
#         accuracy = evaluate_model(X, y, test_size)
#         train_percent = int((1 - test_size) * 100)
#         test_percent = int(test_size * 100)
#         print(f"Train-Test Split: {train_percent}-{test_percent} -> Accuracy: {accuracy:.4f}")




import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

# Train and evaluate model with chronological train-test split
def evaluate_chronological_split(X, y, splits):
    for test_size in splits:
        # Calculate the split index based on the time order
        split_index = int(len(X) * (1 - test_size))
        
        # Chronologically split the dataset
        X_train, X_test = X[:split_index], X[split_index:]
        y_train, y_test = y[:split_index], y[split_index:]

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        predictions = model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        train_pct = int((1 - test_size) * 100)
        test_pct = int(test_size * 100)
        print(f"\nTrain-Test Split: {train_pct}-{test_pct} -> Accuracy: {acc:.4f}")
        print(classification_report(y_test, predictions))

# Main function
def main():
    # Load the dataset
    data = load_data("API_dataset_allcities.csv")
    
    # Extract features and target
    feature_cols = [
        'components.co', 'components.no', 'components.no2', 'components.o3',
        'components.so2', 'components.pm2_5', 'components.pm10', 'components.nh3'
    ]
    target_col = 'main.aqi'

    X = data[feature_cols]
    y = data[target_col]

    # Chronologically evaluate train-test splits
    evaluate_chronological_split(X, y, splits=[0.3, 0.2, 0.1])

if __name__ == "__main__":
    main()
