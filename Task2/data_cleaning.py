import pandas as pd


def clean_data(input_file, output_file):
    # Load data
    df = pd.read_csv(input_file)

    print("📊 Missing values per column:\n", df.isnull().sum())

    # Strip ₹ and commas, then convert Price to float
    df['Price'] = df['Price'].astype(str).str.replace('₹', '', regex=False).str.replace(',', '', regex=False)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Convert Rating to float (some may be 'No ratings' or NaN)
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(0)  # Replace NaN with 0

    # Convert Reviews to int if it's not already
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

    print("\nSummary BEFORE filtering:")
    print(df[['Price', 'Rating']].describe(include='all'))
    print("🔍 Unique ratings:", df['Rating'].dropna().unique())
    print("🔍 Unique prices (sample):", df['Price'].dropna().unique()[:10])

    # Drop rows where essential numeric values are missing
    df.dropna(subset=['Price'], inplace=True)  # Don't drop rows with 0 ratings

    # Filter: only keep reasonable products
    df = df[df['Price'] > 0]
    df = df[df['Rating'] >= 0]  # Keep all rows with non-negative ratings (including 0)

    # Final shape
    print(f"\nFinal cleaned data shape: {df.shape}")

    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")


if __name__ == "__main__":
    clean_data('soft_toys_sponsored.csv', 'cleaned_soft_toys.csv')
