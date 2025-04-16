"""
This module performs exploratory data analysis on the third trolls dataset.
"""

import os

import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from ..utils import load_data
from .eda_basic import (
    basic_stats,
    analyze_categorical_features,
    analyze_numerical_features,
    analyze_temporal_patterns,
    analyze_account_behavior,
)
from .eda_nlp import correlation_matrix, analyze_content, sentiment_analysis
from .eda_helpers import progress_bar

# Set style for visualizations
os.makedirs("plots", exist_ok=True)
plt.style.use("fivethirtyeight")
sns.set_theme(font_scale=1.2)
sns.set_palette("husl")

def eda():
    """Run the full EDA process"""
    print("Starting Exploratory Data Analysis...")

    # Download nltk data if not already downloaded
    if not nltk.data.find("vader_lexicon"):
        nltk.download("vader_lexicon")
    if not nltk.data.find("punkt"):
        nltk.download("punkt")
    if not nltk.data.find("stopwords"):
        nltk.download("stopwords")

    raw_df, derived_df, combined_df = load_data()

    # Basic statistics
    basic_stats(raw_df, "raw")
    basic_stats(derived_df, "derived")
    progress_bar(0, 6)
    # Analyze categorical features
    analyze_categorical_features(combined_df, "combined")
    # Analyze numerical features
    analyze_numerical_features(combined_df, "combined")
    # Analyze temporal patterns
    analyze_temporal_patterns(combined_df, "combined")
    # Analyze account behavior
    analyze_account_behavior(combined_df, "combined")
    # Analyze correlation matrix
    correlation_matrix(combined_df, "combined")
    # Analyze content
    analyze_content(combined_df, "combined")
    # Analyze sentiment
    sentiment_analysis(combined_df, "combined")
    print("EDA completed. Visualizations saved to 'visualizations' directory.")

if __name__ == "__main__":
    eda()
