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
from src.visualization import plot_sentiment_distribution

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

        st.success(f"Analyzed {len(df)} reviews!")

        col1, col2 = st.columns(2)

        # Sentiment Chart
        with col1:
            st.subheader("Sentiment Overview")
            fig = plot_sentiment_distribution(df)
            st.pyplot(fig)

        with col2:
            st.subheader("Quick Stats")
            st.write(df['sentiment'].value_counts())

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

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"{app1} Sentiment")
            st.write(df1['sentiment'].value_counts())

        with col2:
            st.subheader(f"{app2} Sentiment")
            st.write(df2['sentiment'].value_counts())

    else:
        st.warning("Please enter valid App IDs for comparison.")