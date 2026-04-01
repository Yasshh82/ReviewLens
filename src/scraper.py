from google_play_scraper import reviews, Sort
import pandas as pd

def fetch_reviews(app_id, count: int = 500) -> pd.DataFrame:
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
    if not result:
        raise ValueError("No reviews fetched. App may not exist or is restricted.")

    df = pd.DataFrame(result)

    column_map = {
        "content": "review",
        "score": "rating",
        "at": "date"
    }

    available_cols = [col for col in column_map.keys() if col in df.columns]

    if len(available_cols) < 3:
        raise ValueError(f"Unexpected API response. Columns found: {list(df.columns)}")

    df = df[available_cols]
    df.rename(columns=column_map, inplace=True)

    return df