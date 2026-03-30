import streamlit as st
from src.scraper import fetch_reviews
from src.preprocess import clean_reviews

st.title("ReviewLens🔍")

app_id = st.text_input("Enter App ID (e.g., com.instragram.android)")

@st.cache_data
def load_data(app_id):
    df = fetch_reviews(app_id)
    df = clean_reviews(df)
    return df

if st.button("Fetch Reviews"):

    if app_id:
        df = load_data(app_id)

        st.success(f"Fetched {len(df)} reviews!")

        st.dataframe(df.head())

    else:
        st.warning("Please enter a valid App ID.")