import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

# Analyze class distribution
def print_class_distribution(y):
    print("\nClass Distribution (AQI classes):")
    print(y.value_counts(normalize=True).rename(lambda x: f"Class {x}"))

# Check for duplicates
def check_duplicates(df):
    duplicates = df.duplicated().sum()
    print(f"\nNumber of duplicate rows: {duplicates}")

# Feature correlation heatmap
def plot_correlation_matrix(df):
    print("\nGenerating correlation heatmap...")
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title("Feature Correlation Matrix")
    plt.tight_layout()
    plt.show()

# Evaluate model accuracy with different train-test splits
def evaluate_splits(X, y, splits):
    for test_size in splits:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        train_pct = int((1 - test_size) * 100)
        test_pct = int(test_size * 100)
        print(f"\nTrain-Test Split: {train_pct}-{test_pct} -> Accuracy: {acc:.4f}")
        print(classification_report(y_test, predictions))

# Run cross-validation
def cross_validation(X, y, cv_folds=5):
    print(f"\nRunning {cv_folds}-Fold Cross-Validation...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    scores = cross_val_score(model, X, y, cv=cv_folds)
    print("Cross-validation scores:", scores)
    print(f"Mean CV Accuracy: {scores.mean():.4f}")

# Main routine
def main():
    data = load_data("C:/Users/hemud/Videos/python class/Comparison-of-ML-models-for-predicting-AQI-latest_v1.2/Air Quality Index/AIQ/New_AQI/Air-Quality-Index/Air-Quality-Index/backend/API_dataset_allcities.csv")

    # Check duplicates
    check_duplicates(data)

    # Plot correlation matrix
    plot_correlation_matrix(data)

    # Extract features and target
    feature_cols = [
        'components.co', 'components.no', 'components.no2', 'components.o3',
        'components.so2', 'components.pm2_5', 'components.pm10', 'components.nh3'
    ]
    target_col = 'main.aqi'

    X = data[feature_cols]
    y = data[target_col]

    # Check class distribution
    print_class_distribution(y)

    # Evaluate train-test splits
    evaluate_splits(X, y, splits=[0.3, 0.2, 0.1])

    # Run cross-validation
    cross_validation(X, y)

if __name__ == "__main__":
    main()
