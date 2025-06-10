import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Load your labeled review file
df = pd.read_csv("../data/reviews_with_sentiment.csv")

# Initialize VADER
sia = SentimentIntensityAnalyzer()


def get_vader_sentiment(text):
    scores = sia.polarity_scores(str(text))
    compound = scores['compound']
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"


df['vader_sentiment'] = df['review_text'].apply(get_vader_sentiment)

# Compare with TextBlob
match = (df['sentiment'] == df['vader_sentiment']).sum()
print(f"Match rate between TextBlob and VADER: {match / len(df):.2%}")


df.to_csv("../data/reviews_with_sentiment_vader.csv", index=False)
print(" Saved VADER sentiment to reviews_with_sentiment_vader.csv")
