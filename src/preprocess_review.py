import pandas as pd

# Load your latest scraped file
df = pd.read_csv("../data/all_bank_reviews_20250608_205256.csv")  # Replace with your actual file name

# Drop empty reviews
df.dropna(subset=['review_text'], inplace=True)

# Drop duplicates (same review text)
df.drop_duplicates(subset=['review_text'], inplace=True)

# Normalize date format
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

# Optional: Keep only needed columns
df = df[['review_text', 'rating', 'date', 'bank_name', 'source']]


df.to_csv("../data/cleaned_reviews.csv", index=False)
print("✅ Cleaned reviews saved to cleaned_reviews.csv")
