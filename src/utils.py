def generate_insights(positive_phrases, negative_phrases):
    insights = []

    if positive_phrases:
        top_positive = positive_phrases[0][0]
        insights.append(f"✅ Users love {top_positive}")

    if negative_phrases:
        top_negative = negative_phrases[0][0]
        insights.append(f"⚠️ Users complain about {top_negative}")

    return insights

def compare_apps(complaints1, complaints2):
    set1 = set([c[0] for c in complaints1])
    set2 = set([c[0] for c in complaints2])

    unique_to_app1 = set1 - set2
    unique_to_app2 = set2 - set1

    return unique_to_app1, unique_to_app2