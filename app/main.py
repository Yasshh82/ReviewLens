import sys
import os
import streamlit as st
from src.scraper import fetch_reviews
from src.preprocess import clean_reviews
from src.sentiment import add_sentiment
from src.nlp_pipeline import (
    process_reviews, 
    extract_keywords, 
    extract_complaints, 
    extract_action_phrases
)
from src.visualization import plot_sentiment_distribution, plot_sentiment_trend
from src.utils import generate_insights, compare_apps

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(page_title="ReviewLens", layout="wide")

st.title("ReviewLens🔍")

# Input Section
st.sidebar.header("Input")

app_id = st.sidebar.text_input("Enter App ID (e.g., com.instragram.android)")

@st.cache_data
def load_data(app_id):
    df = fetch_reviews(app_id)
    df = clean_reviews(df)
    df = add_sentiment(df)
    return df

# Main Analysis Logic
if st.sidebar.button("Analyze"):

    if app_id:
        df = load_data(app_id)

        docs = process_reviews(df['review'].tolist())

        keywords = extract_keywords(docs)
        complaints = extract_complaints(docs, df['sentiment'])
        action_phrases = extract_action_phrases(docs)

        positive_phrases = [p for p in action_phrases if p[1] > 1]
        negative_phrases = complaints

        insights = generate_insights(positive_phrases, negative_phrases)

        st.success(f"Analyzed {len(df)} reviews!")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Reviews", len(df))
        col2.metric("Positive %", round((df['sentiment'] == "positive").mean()*100, 1))
        col3.metric("Negative %", round((df['sentiment'] == "negative").mean()*100, 1))

        col1, col2 = st.columns(2)

        # Sentiment Chart
        with col1:
            st.subheader("Sentiment Overview")
            fig = plot_sentiment_distribution(df)
            st.pyplot(fig)

        with col2:
            st.subheader("Quick Stats")
            st.write(df['sentiment'].value_counts())

        # Sentiment Trend
        st.subheader("Sentiment Trend")

        trend_fig = plot_sentiment_trend(df)
        st.pyplot(trend_fig)

        # Insights
        col3, col4, col5 = st.columns(3)

        with col3:
            st.subheader("Keywords")
            st.write(keywords)

        with col4:
            st.subheader("Action Insights")
            st.write(action_phrases)

        with col5:
            st.subheader("Complaints")
            st.write(complaints)

        # Insights Section
        st.subheader("💡 Key Insights")

        for insight in insights:
            st.markdown(f"- {insight}")

        # Download
        st.subheader("Export Data")

        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name=f"{app_id}_reviews.csv",
            mime="text/csv"
        )

    else:
        st.warning("Please enter a valid App ID.")

st.markdown("---")
st.header("App Comparison")

app1 = st.text_input("Enter First App ID")
app2 = st.text_input("Enter Second App ID")

if st.button("Compare Apps"):

    if app1 and app2:

        df1 = load_data(app1)
        df2 = load_data(app2)

        docs1 = process_reviews(df1['review'].tolist())
        docs2 = process_reviews(df2['review'].tolist())

        complaints1 = extract_complaints(docs1, df1['sentiment'])
        complaints2 = extract_complaints(docs2, df2['sentiment'])

        unique1, unique2 = compare_apps(complaints1, complaints2)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"{app1} Sentiment")
            st.write(df1['sentiment'].value_counts())

        with col2:
            st.subheader(f"{app2} Sentiment")
            st.write(df2['sentiment'].value_counts())

        st.subheader("Unique Issues Comparison")

        col3, col4 = st.columns(2)

        with col3:
            st.write(f"Issues Unique to {app1}")
            st.write(list(unique1)[:10])

        with col4:
            st.write(f"Issues Unique to {app2}")
            st.write(list(unique2)[:10])

    else:
        st.warning("Please enter valid App IDs for comparison.")