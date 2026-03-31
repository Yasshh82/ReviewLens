def generate_insights(positive_phrases, negative_phrases):
    insights = []

    if positive_phrases:
        top_positive = positive_phrases[0][0]
        insights.append(f"✅ Users love {top_positive}")

    if negative_phrases:
        top_negative = negative_phrases[0][0]
        insights.append(f"⚠️ Users complain about {top_negative}")

    return insights