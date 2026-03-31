import spacy
import streamlit as st
from collections import Counter

COMMON_NOISE = {
    "this app", "the app", "app", "this", "it",
    "this issue", "the issue", "a problem",
    "this problem", "everything", "something"
}

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
            text = chunk.text.strip().lower()

            if text in COMMON_NOISE:
                continue

            if len(text.split()) < 2:
                continue

            if any(token.pos_ == "PRON" for token in chunk):
                continue

            phrases.append(text)

    return Counter(phrases).most_common(top_n)

def extract_action_phrases(docs, top_n=15):
    phrases = []

    for doc in docs:
        for token in doc:

            if token.pos_ == "ADJ" and token.head.pos_ == "NOUN":
                phrase = f"{token.text} {token.head.text}"
                phrases.append(phrase.lower())

            if token.dep_ == "compound" and token.head.pos_ == "NOUN":
                phrase = f"{token.text} {token.head.text}"
                phrases.append(phrase.lower())

    return Counter(phrases).most_common(top_n)

def extract_complaints(docs, sentiments, top_n=10):
    complaints = []

    for doc, sentiment in zip(docs, sentiments):

        if sentiment == "negative":

            for token in doc:

                # ADJ + NOUN pattern
                if token.pos_ == "ADJ" and token.head.pos_ == "NOUN":
                    phrase = f"{token.text} {token.head.text}"

                    if phrase not in COMMON_NOISE:
                        complaints.append(phrase.lower())

    return Counter(complaints).most_common(top_n)