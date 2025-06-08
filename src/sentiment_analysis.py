import pandas as pd
from textblob import TextBlob

df = pd.read_csv("../data/cleaned_reviews.csv")

def get_sentiment_label(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'

df['sentiment'] = df['review_text'].apply(get_sentiment_label)

df.to_csv("../data/reviews_with_sentiment.csv", index=False)
print("✅ Sentiment analysis complete. Saved to reviews_with_sentiment.csv")
