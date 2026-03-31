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