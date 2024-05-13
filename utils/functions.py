import pandas as pd
from utils.analysis import *

def predict(model, enc, category, market):
    # Convert the category and market into a DataFrame
    input_df = pd.DataFrame([[market if market else 'unknown', category if category else 'unknown']], columns=['market', 'category'])
    # Convert categorical variables into dummy/indicator variables
    input_df = enc.transform(input_df)
    # Use the model to predict the price
    return model.predict(input_df)


def analyze_market(data):
    market_analysis_result = {
        'average_price_by_category': average_price_by_category(data),
        'total_markets': total_markets(data),
        'total_commodities': total_commodities(data),
        'plots': {
            'price_distribution': price_distribution_by_category(data),
            'price_trends_over_time': price_trends_over_time(data),
            'market_concentration': market_concentration(data),
            'price_variability': price_variability(data),
            'seasonal_patterns': seasonal_patterns(data),
        }
    }

    return {'market_analysis': market_analysis_result}

def simulate_market(data, num_markets, num_commodities):
    simulated_markets = data['market'].sample(num_markets).tolist()
    simulated_commodities = data['commodity'].sample(num_commodities).tolist()
    return {
        'num_markets': num_markets,
        'num_commodities': num_commodities,
        'simulated_markets': simulated_markets,
        'simulated_commodities': simulated_commodities
    }

