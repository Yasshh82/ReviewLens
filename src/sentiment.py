import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import streamlit as st

@st.cache_resource
def load_sentiment_analyzer():
    try:
        return SentimentIntensityAnalyzer()
    except Exception as e:
        st.error(f"Error loading sentiment analyzer: {e}")
        raise

analyzer = load_sentiment_analyzer()

def add_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    sentiments = []

    for text in df['review']:
        score = analyzer.polarity_scores(text)['compound']

        if score >= 0.05:
            sentiments.append("positive")
        elif score <= -0.05:
            sentiments.append("negative")
        else:
            sentiments.append("neutral")

    df['sentiment'] = sentiments
    return df