"""
This module performs exploratory data analysis on the third trolls dataset.
"""

from collections import Counter
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Set style for visualizations
plt.style.use("fivethirtyeight")
sns.set_theme(font_scale=1.2)
sns.set_palette("husl")

# Create output directory for plots
os.makedirs("plots", exist_ok=True)


def load_data():
    """Load both the trimmed and derived datasets"""
    trimmed_df = pd.read_csv("data/raw/1_trimmed.csv")
    derived_df = pd.read_csv("data/raw/1_derived.csv")

    # Combine the datasets
    combined_df = pd.concat([trimmed_df, derived_df], axis=1)

    # Handle duplicated columns (if any)
    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

    return trimmed_df, derived_df, combined_df


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
        if feature in df.columns:
            plt.figure(figsize=(12, 6))
            counts = df[feature].value_counts().head(15)
            counts.plot(kind="bar")
            plt.title(f'Top 15 {feature.replace("_", " ").title()} Distribution')
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(f"plots/{name}_{feature}_distribution.png")
            plt.close()


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
    if "publish_date" in df.columns:
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(df["publish_date"]):
            df["date"] = pd.to_datetime(df["publish_date"], errors="coerce")
        else:
            df["date"] = df["publish_date"]

        # Hour of day analysis
        plt.figure(figsize=(12, 6))
        if "hour_of_day" in df.columns:
            hourly_posts = df["hour_of_day"].value_counts().sort_index()
        else:
            hourly_posts = df["date"].dt.hour.value_counts().sort_index()

        hourly_posts.plot(kind="bar")
        plt.title("Tweet Distribution by Hour of Day")
        plt.xlabel("Hour of Day")
        plt.ylabel("Number of Tweets")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(f"plots/{name}_hourly_distribution.png")
        plt.close()

        # Day of week analysis
        plt.figure(figsize=(12, 6))
        if "day_of_week" in df.columns:
            dow_posts = df["day_of_week"].value_counts().sort_index()
        else:
            dow_posts = df["date"].dt.dayofweek.value_counts().sort_index()

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        dow_posts.index = [days[i] for i in dow_posts.index]
        dow_posts.plot(kind="bar")
        plt.title("Tweet Distribution by Day of Week")
        plt.xlabel("Day of Week")
        plt.ylabel("Number of Tweets")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"plots/{name}_dayofweek_distribution.png")
        plt.close()


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


def analyze_nlp_features(df, name):
    """Analyze NLP-specific features"""
    nlp_features = [
        "count_hashtags",
        "count_mentions",
        "word_count",
        "text_length",
        "count_emojis",
        "count_special_characters",
        "all_words_caps",
        "starts_with_hashtag",
        "starts_with_mention",
    ]

    # Create a correlation matrix for NLP features
    nlp_corr_df = df[[col for col in nlp_features if col in df.columns]].copy()

    if not nlp_corr_df.empty and len(nlp_corr_df.columns) > 1:
        plt.figure(figsize=(12, 10))
        corr = nlp_corr_df.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(
            corr, mask=mask, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5
        )
        plt.title("Correlation Matrix of NLP Features")
        plt.tight_layout()
        plt.savefig(f"plots/{name}_nlp_feature_correlation.png")
        plt.close()

    # Analyze hashtag and mention usage
    for feature in ["starts_with_hashtag", "starts_with_mention"]:
        if feature in df.columns:
            plt.figure(figsize=(10, 6))
            df[feature].value_counts().plot(kind="pie", autopct="%1.1f%%")
            plt.title(f'Proportion of Tweets that {feature.replace("_", " ").title()}')
            plt.ylabel("")
            plt.tight_layout()
            plt.savefig(f"plots/{name}_{feature}_pie.png")
            plt.close()


def analyze_content(df, name):
    """Analyze the textual content of tweets"""
    if "content" in df.columns:
        # Generate word cloud from content
        plt.figure(figsize=(12, 12))
        text = " ".join(df["content"].dropna().astype(str))
        wordcloud = WordCloud(
            width=800, height=800, background_color="white", min_font_size=10
        ).generate(text)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.savefig(f"plots/{name}_content_wordcloud.png")
        plt.close()

        # Analyze most common hashtags
        if "hashtags" in df.columns:
            all_hashtags = [
                tag
                for tags in df["hashtags"].dropna()
                for tag in tags.split(", ")
                if tag
            ]
            top_hashtags = Counter(all_hashtags).most_common(20)

            if top_hashtags:
                plt.figure(figsize=(12, 8))
                hashtag_df = pd.DataFrame(top_hashtags, columns=["Hashtag", "Count"])
                sns.barplot(x="Count", y="Hashtag", data=hashtag_df)
                plt.title("Top 20 Hashtags")
                plt.tight_layout()
                plt.savefig(f"plots/{name}_top_hashtags.png")
                plt.close()


def progress_bar(current, total, bar_length=70):
    """Print a progress bar"""
    percent = float(current) * 100 / total
    arrow = "=" * int(percent / 100)
    spaces = " " * (bar_length - len(arrow))
    print(f"Progress: [{arrow}{spaces}] {percent:.2f}%", end="\r")


def run_eda():
    """Run the full EDA process"""
    print("Starting Exploratory Data Analysis...")

    # Load the data
    trimmed_df, derived_df, combined_df = load_data()

    # Basic statistics
    basic_stats(trimmed_df, "trimmed")
    basic_stats(derived_df, "derived")
    progress_bar(0, 6)
    # Analyze categorical features
    analyze_categorical_features(combined_df, "combined")
    progress_bar(1, 6)
    # Analyze numerical features
    analyze_numerical_features(combined_df, "combined")
    progress_bar(2, 6)
    # Analyze temporal patterns
    analyze_temporal_patterns(combined_df, "combined")
    progress_bar(3, 6)
    # Analyze account behavior
    analyze_account_behavior(combined_df, "combined")
    progress_bar(4, 6)
    # Analyze NLP features
    analyze_nlp_features(combined_df, "combined")
    progress_bar(5, 6)
    # Analyze content
    analyze_content(combined_df, "combined")
    progress_bar(6, 6)
    print("EDA completed. Visualizations saved to 'plots' directory.")


if __name__ == "__main__":
    run_eda()
