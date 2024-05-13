import seaborn as sns
import matplotlib.pyplot as plt

def visualize(data):
    return {
        'scatterplot': scatterplot_of_price_vs_date(data),
        'boxplot': boxplot_of_price_distribution_by_category(data)
    }

def scatterplot_of_price_vs_date(data):
    # Plot 1: Scatterplot of price vs. date
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='date', y='price', hue='category', data=data)
    plt.title('Price Variation Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (NGN)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    scatterplot_name = 'scatterplot.png'
    plt.savefig('/app/images/'+scatterplot_name)
    plt.close()
    return scatterplot_name


def boxplot_of_price_distribution_by_category(data):
    # Plot 2: Boxplot of price distribution by category
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='category', y='price', data=data)
    plt.title('Price Distribution by Category')
    plt.xlabel('Category')
    plt.ylabel('Price (NGN)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    boxplot_name = 'boxplot.png'
    plt.savefig('/app/images/'+boxplot_name)
    plt.close()
    return boxplot_name