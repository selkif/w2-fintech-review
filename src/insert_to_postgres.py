import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("../data/reviews_with_sentiment_vader.csv")
df = df.dropna(subset=["review_text"])


theme_dict = {
    "Commercial Bank of Ethiopia": {
        "Login Issues": ["login", "password", "access"],
        "Transfer Delays": ["delay", "transfer", "load"]
    },
    "Bank of Abyssinia": {
        "App Crashes": ["crash", "bug", "error"],
        "Slow Performance": ["slow", "update", "wait"]
    },
    "Dashen Bank": {
        "Good UX": ["interface", "design", "easy"],
        "Feature Requests": ["add", "feature", "option"]
    }
}


def assign_theme(text, bank):
    text = str(text).lower()
    if bank in theme_dict:
        for theme, keywords in theme_dict[bank].items():
            if any(keyword in text for keyword in keywords):
                return theme
    return "Uncategorized"

# Assign themes to the DataFrame
df['theme'] = df.apply(lambda row: assign_theme(row['review_text'], row['bank_name']), axis=1)

# Connect to PostgreSQL database (use your actual password here)
user = "postgres"
password = "chatbot1"
host = "localhost"
port = "5432"
db = "bank_reviews"

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

# Insert banks
bank_names = df['bank_name'].dropna().unique()
banks_df = pd.DataFrame({'name': bank_names})
banks_df.to_sql('banks', engine, if_exists='append', index=False)

# Get the bank_id mapping from DB
bank_map = pd.read_sql("SELECT * FROM banks", engine).set_index('name')['bank_id'].to_dict()
df['bank_id'] = df['bank_name'].map(bank_map)

# Rename columns to match DB schema
df_final = df.rename(columns={
    'review_text': 'review_text',
    'rating': 'rating',
    'date': 'review_date',
    'sentiment': 'sentiment_label_textblob',
    'vader_sentiment': 'sentiment_label_vader'
})

# Select required columns
final_columns = [
    'review_text', 'rating', 'review_date',
    'sentiment_label_textblob', 'sentiment_label_vader',
    'theme', 'bank_id'
]

# Insert into reviews table
df_final[final_columns].to_sql('reviews', engine, if_exists='append', index=False)

print("✅ Data successfully inserted into PostgreSQL!")
