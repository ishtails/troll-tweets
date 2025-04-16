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
    """
    Analyze NLP-specific features.
    
    Args:
        df: DataFrame with NLP features
        name: Name prefix for output files
        
    Returns:
        Dictionary with NLP feature correlations in JSON-compatible format
    """
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
    
    # Initialize result dictionary
    result = {"has_nlp_correlations": False}

    # Create a correlation matrix for NLP features
    nlp_corr_df = df[[col for col in nlp_features if col in df.columns]].copy()

    if not nlp_corr_df.empty and len(nlp_corr_df.columns) > 1:
        # Generate the visualization
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
        
        # Add correlation data to result
        result["has_nlp_correlations"] = True
        result["features"] = list(nlp_corr_df.columns)
        result["correlation_matrix"] = {}
        
        # Create a dictionary of correlation values
        for col1 in nlp_corr_df.columns:
            result["correlation_matrix"][col1] = {}
            for col2 in nlp_corr_df.columns:
                result["correlation_matrix"][col1][col2] = float(corr.loc[col1, col2])
                
        # Find top correlations
        top_correlations = []
        for i, col1 in enumerate(nlp_corr_df.columns):
            for j, col2 in enumerate(nlp_corr_df.columns):
                if i < j:  # Only include each pair once
                    correlation = float(corr.loc[col1, col2])
                    if abs(correlation) > 0.3:  # Only include meaningful correlations
                        top_correlations.append({
                            "feature1": col1,
                            "feature2": col2,
                            "correlation": correlation
                        })
        
        # Sort by absolute correlation value
        top_correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)
        result["top_correlations"] = top_correlations[:10]  # Include top 10 correlations
        
    return result


def analyze_content(df, name):
    """
    Analyze the textual content of tweets.
    
    Args:
        df: DataFrame with text content
        name: Name prefix for output files
        
    Returns:
        Dictionary with content analysis results in JSON-compatible format
    """
    # Initialize result dictionary
    result = {
        "has_content_data": False,
        "has_hashtag_data": False,
        "has_special_format_data": False
    }

    # Content analysis
    if "content" in df.columns and not df["content"].dropna().empty:
        # Analyze text content
        result["has_content_data"] = True
        
        # Generate word cloud for visualization
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
            
            # Extract common words for JSON
            words = text.lower().split()
            word_counts = Counter(words).most_common(20)
            result["top_words"] = [{"word": word, "count": count} for word, count in word_counts]
        else:
            print("Skipping word cloud for content: No words to process.")

    # Hashtag analysis
    if "hashtags" in df.columns and not df["hashtags"].dropna().empty:
        all_hashtags = [
            tag for tags in df["hashtags"].dropna() for tag in tags.split(", ") if tag
        ]
        if all_hashtags:  # Ensure there's data
            result["has_hashtag_data"] = True
            
            # Generate visualizations
            tags_string = ", ".join(all_hashtags).replace("#", "")
            wordcloud = WordCloud(
                width=800, height=800, background_color="white", min_font_size=10
            ).generate(tags_string)
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(f"plots/{name}_hashtags_wordcloud.png")
            plt.close()
            
            # Add top hashtags to result
            top_hashtags = Counter(all_hashtags).most_common(20)
            result["top_hashtags"] = [{"hashtag": tag, "count": count} for tag, count in top_hashtags]
            
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
    special_format_stats = {}
    for feature in ["starts_with_hashtag", "starts_with_mention"]:
        if feature in df.columns:
            result["has_special_format_data"] = True
            
            # Generate visualization
            plt.figure(figsize=(10, 6))
            counts = df[feature].map({0: "No", 1: "Yes"}).value_counts()
            counts.plot(kind="pie", autopct="%1.1f%%")
            plt.title(f'Proportion of Tweets that {feature.replace("_", " ").title()}')
            plt.ylabel("")
            plt.tight_layout()
            plt.savefig(f"plots/{name}_{feature}_pie.png")
            plt.close()
            
            # Add stats to result
            yes_count = int(df[feature].sum())
            total_count = len(df[feature])
            special_format_stats[feature] = {
                "yes_count": yes_count,
                "no_count": total_count - yes_count,
                "yes_percentage": float(yes_count / total_count * 100) if total_count > 0 else 0
            }
    
    if result["has_special_format_data"]:
        result["special_format_stats"] = special_format_stats

    return result


def sentiment_analysis(df, name):
    """
    Analyze the sentiment of the tweets.
    
    Args:
        df: DataFrame with a 'content' column
        name: Name prefix for output files
        
    Returns:
        Dictionary with sentiment analysis results in JSON-compatible format
    """
    if "content" not in df.columns:
        raise ValueError("DataFrame must have a 'content' column")
    
    # Initialize result dictionary
    result = {"has_sentiment_data": False}
    
    analyzer = SentimentIntensityAnalyzer()
    df["cleaned_text"] = df["content"].apply(clean_text)
    df["sentiment"] = df["cleaned_text"].apply(
        lambda x: analyzer.polarity_scores(x)["compound"]
    )
    
    if not df.empty and not df["sentiment"].dropna().empty:
        # Set sentiment data flag to true
        result["has_sentiment_data"] = True
        
        # Add sentiment distribution statistics
        result["sentiment_distribution"] = {
            "mean": float(df["sentiment"].mean()),
            "median": float(df["sentiment"].median()),
            "std": float(df["sentiment"].std()),
            "positive_ratio": float((df["sentiment"] > 0.05).mean()),
            "neutral_ratio": float((df["sentiment"].between(-0.05, 0.05)).mean()),
            "negative_ratio": float((df["sentiment"] < -0.05).mean()),
        }
        
        # Add category-based sentiment if available
        if "account_category" in df.columns:
            sentiment_by_category = df.groupby("account_category")["sentiment"].mean().to_dict()
            result["sentiment_by_category"] = {
                str(k): float(v) for k, v in sentiment_by_category.items()
            }
        
        # Add region-based sentiment if available
        if "region" in df.columns:
            sentiment_by_region = df.groupby("region")["sentiment"].mean().to_dict()
            result["sentiment_by_region"] = {
                str(k): float(v) for k, v in sentiment_by_region.items()
            }
        
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
        print("DataFrame is empty or has no sentiment data, no plots generated.")
    
    return result
