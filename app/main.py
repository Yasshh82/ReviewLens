import streamlit as st
from src.scraper import fetch_reviews
from src.preprocess import clean_reviews
from src.sentiment import add_sentiment
from src.nlp_pipeline import process_reviews, extract_keywords, extract_complaints

st.title("ReviewLens🔍")

app_id = st.text_input("Enter App ID (e.g., com.instragram.android)")

@st.cache_data
def load_data(app_id):
    df = fetch_reviews(app_id)
    df = clean_reviews(df)
    df = add_sentiment(df)
    return df

if st.button("Analyze"):

    if app_id:
        df = load_data(app_id)

        docs = process_reviews(df['review'].tolist())

        keywords = extract_keywords(docs)
        complaints = extract_complaints(docs, df['sentiment'])

        st.success(f"Analyzed {len(df)} reviews!")

        st.dataframe(df.head())

        st.subheader("Top Keywords")
        st.write(keywords)

        st.subheader("Top Complaints")
        st.write(complaints)

    else:
        st.warning("Please enter a valid App ID.")