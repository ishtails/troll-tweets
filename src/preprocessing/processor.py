"""Module for processing tweets data."""

import pandas as pd


def process_tweets():
    """Process the tweets data."""
    df = pd.read_csv("data/raw/IRAhandle_tweets_1.csv")

    keep_cols = [
        "content",
        "region",
        "language",
        "publish_date",
        "following",
        "followers",
        "updates",
        "account_type",
        "retweet",
        "account_category",
    ]

    df_new = df[keep_cols]
    print(df_new.columns)


if __name__ == "__main__":
    process_tweets()
