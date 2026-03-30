import pandas as pd

def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning of reviews
    """

    df = df.dropna(subset=['review'])

    df['review'] = df['review'].str.lower()

    df['review'] = df['review'].str.strip()

    return df