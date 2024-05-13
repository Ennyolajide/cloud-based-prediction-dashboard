import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def average_price_by_category(data):
    if isinstance(data, pd.DataFrame) and 'category' in data.columns and 'price' in data.columns:
        return data.groupby('category')['price'].mean().to_dict()
    else:
        return {}

def total_markets(data):
    if isinstance(data, pd.DataFrame) and 'market' in data.columns:
        return data['market'].nunique()
    else:
        return 0

def total_commodities(data):
    if isinstance(data, pd.DataFrame) and 'commodity' in data.columns:
        return data['commodity'].nunique()
    else:
        return 0

def price_distribution_by_category(data):
    if isinstance(data, pd.DataFrame) and 'category' in data.columns and 'price' in data.columns:
        plt.figure(figsize=(12, 8))
        sns.histplot(data=data, x='price', hue='category', multiple='stack', kde=True)
        plt.title('Price Distribution by Category')
        plt.xlabel('Price')
        plt.ylabel('Frequency')
        plt.legend(title='Category')
        path = '/app/images/price_distribution.png'
        plt.savefig(path)
        plt.close()
        return path
    else:
        return None

def price_trends_over_time(data):
    if isinstance(data, pd.DataFrame) and 'date' in data.columns and 'price' in data.columns and 'category' in data.columns:
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=data, x='date', y='price', hue='category')
        plt.title('Price Trends Over Time by Category')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend(title='Category')
        path = '/app/images/price_trends_over_time.png'
        plt.savefig(path)
        plt.close()
        return path
    else:
        return None

def market_concentration(data):
    if isinstance(data, pd.DataFrame) and 'market' in data.columns:
        plt.figure(figsize=(10, 6))
        top_markets = data['market'].value_counts().head(10)  # Top 10 markets
        top_markets.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Market Concentration')
        plt.axis('equal')
        plt.tight_layout()
        path = '/app/images/market_concentration.png'
        plt.savefig(path)
        plt.close()
        return path
    else:
        return None

def price_variability(data):
    if isinstance(data, pd.DataFrame) and 'category' in data.columns and 'price' in data.columns:
        plt.figure(figsize=(12, 8))
        sns.boxplot(data=data, x='category', y='price')
        plt.title('Price Variability by Category')
        plt.xlabel('Category')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = '/app/images/price_variability.png'
        plt.savefig(path)
        plt.close()
        return path
    else:
        return None

def seasonal_patterns(data):
    if isinstance(data, pd.DataFrame) and 'date' in data.columns and 'price' in data.columns and 'category' in data.columns:
        seasonal_patterns = data.copy()
        seasonal_patterns['date'] = pd.to_datetime(seasonal_patterns['date'])
        seasonal_patterns.set_index('date', inplace=True)
        seasonal_decomposition = seasonal_patterns.groupby('category')['price'].resample('M').mean().unstack(level=0)
        plt.figure(figsize=(12, 8))
        seasonal_decomposition.plot()
        plt.title('Seasonal Patterns in Price')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend(title='Category')
        plt.tight_layout()
        path = '/app/images/seasonal_patterns.png'
        plt.savefig(path)
        plt.close()
        return path
    else:
        return None
