import pandas as pd


def add_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    def get_sentiment(rating):
        if rating >= 4:
            return "positive"
        elif rating == 3:
            return "neutral"
        else:
            return "negative"

    df['sentiment'] = df['rating'].apply(get_sentiment)
    return df