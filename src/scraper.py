from google_play_scraper import reviews, Sort
import pandas as pd

def fetch_reviews(app_id, count: int = 100) -> pd.DataFrame:
    """
    Fetch reviews from Google Play Store and return a DataFrame
    """

    result, _ = reviews(
        app_id,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=count
    )

    df = pd.DataFrame(result)

    df = df[['content', 'score', 'at']]

    df.columns = ['review', 'rating', 'date']

    return df