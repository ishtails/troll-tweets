"""Basic EDA functions"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def basic_stats(df, name):
    """Print basic statistics about the dataset"""
    print(f"\n=== Basic Statistics for {name} ===")
    print(f"Shape: {df.shape}")
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nData types:")
    print(df.dtypes)

    # Save descriptive statistics to CSV
    desc_stats = df.describe(include="all").T
    desc_stats.to_csv(f"plots/{name}_descriptive_stats.csv")

    return desc_stats


def analyze_categorical_features(df, name):
    """Analyze categorical features like region, language, account_type"""
    categorical_features = ["region", "language", "account_type", "account_category"]

    for feature in categorical_features:
        if feature in df.columns and not df[feature].dropna().empty:
            plt.figure(figsize=(12, 6))
            counts = df[feature].value_counts().head(15)
            counts.plot(kind="bar")
            plt.title(f'Top 15 {feature.replace("_", " ").title()} Distribution')
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(f"plots/{name}_{feature}_distribution.png")
            plt.close()
        else:
            print(f"Skipping {feature} as data is empty.")


def analyze_numerical_features(df, name):
    """Analyze numerical features with histograms and boxplots"""
    numerical_features = [
        "following",
        "followers",
        "updates",
        "followers_to_following_ratio",
        "count_hashtags",
        "count_mentions",
        "count_emojis",
        "word_count",
        "text_length",
    ]

    for feature in numerical_features:
        if feature in df.columns:
            plt.figure(figsize=(12, 5))

            # Histogram
            plt.subplot(1, 2, 1)
            sns.histplot(df[feature].dropna(), kde=True)
            plt.title(f'Distribution of {feature.replace("_", " ").title()}')

            # Boxplot
            plt.subplot(1, 2, 2)
            sns.boxplot(x=df[feature].dropna())
            plt.title(f'Boxplot of {feature.replace("_", " ").title()}')

            plt.tight_layout()
            plt.savefig(f"plots/{name}_{feature}_analysis.png")
            plt.close()


def analyze_temporal_patterns(df, name):
    """Analyze temporal patterns in the data"""
    if "publish_date" in df.columns and not df["publish_date"].dropna().empty:
        df["date"] = pd.to_datetime(df["publish_date"], errors="coerce")

        if "hour_of_day" in df.columns and not df["hour_of_day"].dropna().empty:
            hourly_posts = df["hour_of_day"].value_counts().sort_index()
            plt.figure(figsize=(12, 6))
            hourly_posts.plot(kind="bar")
            plt.title("Tweet Distribution by Hour of Day")
            plt.xlabel("Hour of Day")
            plt.ylabel("Number of Tweets")
            plt.xticks(rotation=0)
            plt.tight_layout()
            plt.savefig(f"plots/{name}_hourly_distribution.png")
            plt.close()

        if "day_of_week" in df.columns and not df["day_of_week"].dropna().empty:
            dow_posts = df["day_of_week"].dropna().value_counts().sort_index()
            dow_posts.index = dow_posts.index.astype(int)  # Convert to integers
            days = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            valid_indices = [
                i for i in dow_posts.index if i in range(7)
            ]  # Filter valid indices
            if valid_indices:
                dow_posts = dow_posts.loc[valid_indices]
                dow_posts.index = [days[i] for i in dow_posts.index]
                plt.figure(figsize=(12, 6))
                dow_posts.plot(kind="bar")
                plt.title("Tweet Distribution by Day of Week")
                plt.xlabel("Day of Week")
                plt.ylabel("Number of Tweets")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(f"plots/{name}_dayofweek_distribution.png")
                plt.close()
            else:
                print("Skipping day of week plot: No valid data.")


def analyze_account_behavior(df, name):
    """Analyze account behavior patterns"""
    if "account_category" in df.columns and "retweet" in df.columns:
        # Retweet behavior by account category
        plt.figure(figsize=(12, 6))
        retweet_by_category = (
            df.groupby("account_category")["retweet"]
            .mean()
            .sort_values(ascending=False)
        )
        retweet_by_category.plot(kind="bar")
        plt.title("Retweet Ratio by Account Category")
        plt.ylabel("Proportion of Retweets")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(f"plots/{name}_retweet_by_category.png")
        plt.close()

    if (
        "account_category" in df.columns
        and "followers" in df.columns
        and "following" in df.columns
    ):
        # Follower/Following analysis by account category
        plt.figure(figsize=(14, 6))
        stats = (
            df.groupby("account_category")
            .agg({"followers": "median", "following": "median"})
            .sort_values(by="followers", ascending=False)
        )

        stats.plot(kind="bar")
        plt.title("Median Followers and Following by Account Category")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(f"plots/{name}_follower_following_by_category.png")
        plt.close()
