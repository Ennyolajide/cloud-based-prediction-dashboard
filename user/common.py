import pandas as pd
from models import User, Data 
from utils.common import train_model
from flask_login import current_user

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

def get_trained_model(data):
    return train_model(data)

def get_logged_in_user(db_session):
    user = current_user
    return db_session.query(User).get(int(user.id))

def get_and_load_user_data(db_session):
    user = get_logged_in_user(db_session)
    user_data = db_session.query(Data).filter_by(user_id=user.id).all()
    # Convert SQLAlchemy objects to dictionaries
    user_data_dicts = []
    for data_entry in user_data:
        data_dict = {
            'date': data_entry.date,
            'market': data_entry.market,
            'category': data_entry.category,
            'commodity': data_entry.commodity,
            'unit': data_entry.unit,
            'currency': data_entry.currency,
            'price': data_entry.price
        }
        user_data_dicts.append(data_dict)
    
    # Load and process user data
    return load_and_process_db_data(user_data_dicts)

