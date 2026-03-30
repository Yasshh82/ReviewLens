import spacy
import streamlit as st
from collections import Counter

@st.cache_resource
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except Exception as e:
        st.error(f"Error loading spaCy model: {e}")
        raise

@st.cache_data
def process_reviews(texts):
    nlp = load_nlp()
    docs = list(nlp.pipe(texts, batch_size=50))
    return docs

def extract_keywords(docs, top_n=15):
    phrases = []

    for doc in docs:
        for chunk in doc.noun_chunks:
            text = chunk.text.strip()

            if len(text.split()) > 1:
                phrases.append(text)

    return Counter(phrases).most_common(top_n)

def extract_complaints(docs, sentiments, top_n=10):
    complaints = []

    for doc, sentiment in zip(docs, sentiments):
        if sentiment == "negative":
            for chunk in doc.noun_chunks:
                text = chunk.text.strip()

                if len(text.split()) > 1:
                    complaints.append(text)

    return Counter(complaints).most_common(top_n)