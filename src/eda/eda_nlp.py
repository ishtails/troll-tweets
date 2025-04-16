"""NLP EDA functions"""

from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from .eda_helpers import clean_text

def correlation_matrix(df, name):
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


def analyze_content(df, name):
    """Analyze the textual content of tweets"""

    # Word cloud for content
    if "content" in df.columns and not df["content"].dropna().empty:
        text = " ".join(df["content"].dropna().astype(str))
        if len(text.strip().split()) > 0:  # Ensure at least one word
            plt.figure(figsize=(12, 12))
            wordcloud = WordCloud(
                width=800, height=800, background_color="white", min_font_size=10
            ).generate(text)
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(f"plots/{name}_content_wordcloud.png")
            plt.close()
        else:
            print("Skipping word cloud for content: No words to process.")

    # Word cloud for hashtags
    if "hashtags" in df.columns and not df["hashtags"].dropna().empty:
        all_hashtags = [
            tag for tags in df["hashtags"].dropna() for tag in tags.split(", ") if tag
        ]
        if all_hashtags:  # Ensure there's data
            tags_string = ", ".join(all_hashtags).replace("#", "")
            wordcloud = WordCloud(
                width=800, height=800, background_color="white", min_font_size=10
            ).generate(tags_string)
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(f"plots/{name}_hashtags_wordcloud.png")
            plt.close()
            top_hashtags = Counter(all_hashtags).most_common(20)
            if top_hashtags:
                plt.figure(figsize=(12, 8))
                hashtag_df = pd.DataFrame(top_hashtags, columns=["Hashtag", "Count"])
                sns.barplot(x="Count", y="Hashtag", data=hashtag_df)
                plt.title("Top 20 Hashtags")
                plt.tight_layout()
                plt.savefig(f"plots/{name}_top_hashtags.png")
                plt.close()
        else:
            print("Skipping hashtags word cloud: No hashtags to process.")

    # Analyse hashtag and mention usage
    for feature in ["starts_with_hashtag", "starts_with_mention"]:
        if feature in df.columns:
            plt.figure(figsize=(10, 6))
            df[feature].map({0: "No", 1: "Yes"}).value_counts().plot(
                kind="pie", autopct="%1.1f%%"
            )
            plt.title(f'Proportion of Tweets that {feature.replace("_", " ").title()}')
            plt.ylabel("")
            plt.tight_layout()
            plt.savefig(f"plots/{name}_{feature}_pie.png")
            plt.close()


def sentiment_analysis(df, name):
    """Analyze the sentiment of the tweets"""
    if "content" not in df.columns:
        raise ValueError("DataFrame must have a 'content' column")
    analyzer = SentimentIntensityAnalyzer()
    df["cleaned_text"] = df["content"].apply(clean_text)
    df["sentiment"] = df["cleaned_text"].apply(
        lambda x: analyzer.polarity_scores(x)["compound"]
    )
    if not df.empty:
        # Histogram
        plt.figure(figsize=(10, 6))
        sns.histplot(df["sentiment"], bins=20, kde=True)
        plt.title("Sentiment Distribution")
        plt.xlabel("Sentiment Score")
        plt.ylabel("Frequency")
        plt.savefig(f"plots/{name}_sentiment_histogram.png")
        plt.close()
        # Bar plot by account category
        if "account_category" in df.columns:
            plt.figure(figsize=(12, 6))
            sns.barplot(x="account_category", y="sentiment", data=df)
            plt.title("Sentiment by Account Category")
            plt.xlabel("Account Category")
            plt.ylabel("Sentiment Score")
            plt.savefig(f"plots/{name}_sentiment_by_category.png")
            plt.close()
        else:
            print("account_category column not found, skipping bar plot.")
        # Bar plot by region
        if "region" in df.columns:
            plt.figure(figsize=(12, 6))
            sns.barplot(x="region", y="sentiment", data=df)
            plt.title("Sentiment by Region")
            plt.xlabel("Region")
            plt.ylabel("Sentiment Score")
            plt.savefig(f"plots/{name}_sentiment_by_region.png")
            plt.close()
        else:
            print("region column not found, skipping bar plot.")
        # Outlier analysis
        if "sentiment" in df.columns:
            plt.figure(figsize=(10, 6))
            sns.boxplot(x="sentiment", data=df)
            plt.title("Outlier Analysis")
            plt.savefig(f"plots/{name}_outlier_analysis.png")
            plt.close()
        else:
            print("sentiment column not found, skipping outlier analysis.")
    else:
        print("DataFrame is empty, no plots generated.")
