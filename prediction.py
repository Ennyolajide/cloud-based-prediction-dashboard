import pandas as pd

def prediction(model, enc, category, market):
    # Convert the category and market into a DataFrame
    input_df = pd.DataFrame([[market if market else 'unknown', category if category else 'unknown']], columns=['market', 'category'])

    # Convert categorical variables into dummy/indicator variables
    input_df = enc.transform(input_df)

    # Use the model to predict the price
    return model.predict(input_df)