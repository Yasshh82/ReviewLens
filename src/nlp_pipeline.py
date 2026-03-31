import spacy
import streamlit as st
from collections import Counter

COMMON_NOISE = {
    "this app", "the app", "app", "this", "it",
    "this issue", "the issue", "a problem",
    "this problem", "everything", "something"
}

NEGATIVE_WORDS = {
    "bad", "slow", "worst", "poor", "terrible",
    "lag", "issue", "problem", "error", "fail",
    "crash", "bug", "delay", "annoying", "broken"
}

def normalize_phrase(phrase):
    replacements = {
        "issue": "problem",
        "issues": "problem",
        "error": "problem",
        "errors": "problem",
        "fail": "failure",
        "failed": "failure",
        "bug": "problem",
        "bugs": "problem"
    }

    words = phrase.split()
    normalized = [replacements.get(w, w) for w in words]

    return " ".join(normalized)

def filter_phrases(counter, min_count=2):
    return [(p, c) for p, c in counter if c >= min_count]

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

            normalized = normalize_phrase(text)
            phrases.append(normalized)
    
    counter = Counter(phrases).most_common(top_n)
    return filter_phrases(counter)

def extract_action_phrases(docs, top_n=15):
    phrases = []

    for doc in docs:
        for token in doc:

            if token.pos_ == "ADJ" and token.head.pos_ == "NOUN":
                phrase = f"{token.text} {token.head.text}"
                normalized = normalize_phrase(phrase)
                phrases.append(normalized)

            if token.dep_ == "compound" and token.head.pos_ == "NOUN":
                phrase = f"{token.text} {token.head.text}"
                normalized = normalize_phrase(phrase)
                phrases.append(normalized)

    counter = Counter(phrases).most_common(top_n)
    return filter_phrases(counter)

def extract_complaints(docs, sentiments, top_n=10):
    complaints = []

    for doc, sentiment in zip(docs, sentiments):

        if sentiment == "negative":

            for token in doc:

                # ADJ + NOUN pattern
                if token.pos_ == "ADJ" and token.head.pos_ == "NOUN":
                    phrase = f"{token.text} {token.head.text}".lower()

                    # if phrase not in COMMON_NOISE:
                    #     normalized = normalize_phrase(phrase.lower())
                    #     complaints.append(normalized)

                    if token.text.lower() in NEGATIVE_WORDS:
                        complaints.append(phrase)

                if token.pos_ == "NOUN" and token.text.lower() in NEGATIVE_WORDS:
                    if token.i > 0:
                        prev = doc[token.i - 1].text
                        phrase = f"{prev} {token.text}".lower()
                    else:
                        phrase = token.text.lower()
                    
                    complaints.append(phrase)

    counter = Counter(complaints).most_common(top_n)
    return filter_phrases(counter)