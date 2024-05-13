import pandas as pd
import matplotlib.pyplot as plt
from flask import send_from_directory
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(csv_file_path):
    try:
        data = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return None
    except Exception as e:
        print("Error loading CSV file:", e)
        return None

    print("Data loaded successfully. Shape:", data.shape)

    data.columns = data.columns.str.strip()
    
    required_columns = ['market', 'category', 'price', 'usdprice']
    missing_columns = set(required_columns) - set(data.columns)
    if missing_columns:
        print("Error: Missing columns in DataFrame:", missing_columns)
        return None
    
    # Convert 'price' and 'usdprice' columns to numeric values, coerce errors to NaN
    data['price'] = pd.to_numeric(data['price'], errors='coerce')
    data['usdprice'] = pd.to_numeric(data['usdprice'], errors='coerce')

    # Drop rows with NaN values in 'price' and 'usdprice' columns
    data.dropna(subset=['price', 'usdprice'], inplace=True)

    # Remove duplicate rows
    data.drop_duplicates(inplace=True)

    print("Data after preprocessing. Shape:", data.shape)
    return data

def load_and_process_db_data(user_data):
    # Check if user_data is not None and not empty
    if user_data is None or len(user_data) == 0:
        print("Error: No user data provided.")
        return None

    # Convert user_data to a DataFrame
    df = pd.DataFrame(user_data)

    # Check if required columns are present
    required_columns = ['market', 'category', 'price']
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        print("Error: Missing columns in DataFrame:", missing_columns)
        return None

    # Drop rows with missing values in required columns
    df.dropna(subset=required_columns, inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    print("Data after processing. Shape:", df.shape)
    return df

def train_model(data):
    # Check if data is loaded correctly
    if data is None or data.empty:
        print("Error: No data loaded or data is empty.")
        return None, None

    # Check if 'market' and 'category' columns exist and are not empty
    if 'market' not in data or 'category' not in data or data['market'].empty or data['category'].empty:
        print("Error: 'market' and 'category' columns are required.")
        return None, None

    # Define the features and target
    X = data[['market', 'category']]
    y = data['price']

    # Convert categorical variables into dummy/indicator variables
    enc = OneHotEncoder()
    X = enc.fit_transform(X)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    print("Model training completed.")
    return model, enc


def save_image_plot(plot, filename):
    plt.savefig(filename)
    plt.close()

def send_image_from_directory(directory, filename):
    return send_from_directory(directory, filename)
