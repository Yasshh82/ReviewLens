import matplotlib.pyplot as plt

def plot_sentiment_distribution(df):
    counts = df['sentiment'].value_counts()

    fig, ax = plt.subplots()
    counts.plot(kind='bar', ax=ax)

    ax.set_title('Sentiment Distribution')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Number of Reviews')

    return fig

import matplotlib.pyplot as plt


def plot_sentiment_trend(df):
    df['date'] = df['date'].dt.date

    trend = df.groupby(['date', 'sentiment']).size().unstack().fillna(0)

    fig, ax = plt.subplots()

    trend.plot(ax=ax)

    ax.set_title("Sentiment Trend Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Reviews")

    return fig

def plot_comparison_sentiment(df1, df2, app1, app2):

    counts1 = df1['sentiment'].value_counts()
    counts2 = df2['sentiment'].value_counts()

    labels = ['positive', 'neutral', 'negative']

    values1 = [counts1.get(label, 0) for label in labels]
    values2 = [counts2.get(label, 0) for label in labels]

    x = range(len(labels))

    fig, ax = plt.subplots()

    ax.bar([i - 0.2 for i in x], values1, width=0.4, label=app1)
    ax.bar([i + 0.2 for i in x], values2, width=0.4, label=app2)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("App Sentiment Comparison")
    ax.set_ylabel("Number of Reviews")
    ax.legend()

    return fig