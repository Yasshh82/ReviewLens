import matplotlib.pyplot as plt

def plot_sentiment_distribution(df):
    counts = df['sentiment'].value_counts()

    fig, ax = plt.subplots()
    counts.plot(kind='bar', ax=ax)

    ax.set_title('Sentiment Distribution')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Number of Reviews')

    return fig