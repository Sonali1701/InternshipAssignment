import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_data(input_file):
    # Load the cleaned data
    df = pd.read_csv(input_file)

    # Display basic statistics of numerical columns
    print("\nDescriptive Statistics:\n", df.describe())

    # Plotting price distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Price'], bins=30, kde=True, color='blue')
    plt.title('Price Distribution of Soft Toys')
    plt.xlabel('Price (₹)')
    plt.ylabel('Frequency')
    plt.show()

    # Plotting rating distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Rating'], bins=20, kde=True, color='green')
    plt.title('Rating Distribution of Soft Toys')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.show()

    # Plotting the most common brands
    plt.figure(figsize=(12, 8))
    brand_counts = df['Brand'].value_counts().head(10)  # Top 10 brands
    sns.barplot(x=brand_counts.index, y=brand_counts.values, palette='viridis')
    plt.title('Top 10 Most Common Brands')
    plt.xlabel('Brand')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

    # Plotting relationship between Price and Rating
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Price', y='Rating', data=df, color='purple')
    plt.title('Price vs Rating')
    plt.xlabel('Price (₹)')
    plt.ylabel('Rating')
    plt.show()

if __name__ == "__main__":
    analyze_data('cleaned_soft_toys.csv')
