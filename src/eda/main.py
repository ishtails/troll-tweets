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
from .eda_network import save_network_data
from .eda_helpers import progress_bar
from .eda_llm import generate_llm_eda

# Set style for visualizations
os.makedirs("plots", exist_ok=True)
plt.style.use("fivethirtyeight")
sns.set_theme(font_scale=1.2)
sns.set_palette("husl")


def eda():
    """Run the full EDA process"""
    print("Starting Exploratory Data Analysis...")

    nltk.download("stopwords")
    nltk.download("vader_lexicon")
    nltk.download("punkt")

    raw_df, derived_df, combined_df2 = load_data()
    combined_df = combined_df2.head(100)

    # Basic statistics
    basic_stats(raw_df, "raw")
    basic_stats(derived_df, "derived")
    progress_bar(0, 8)  # Updated total steps from 7 to 8
    # Analyze categorical features
    analyze_categorical_features(combined_df, "combined")
    progress_bar(1, 8)
    # Analyze numerical features
    analyze_numerical_features(combined_df, "combined")
    progress_bar(2, 8)
    # Analyze temporal patterns
    analyze_temporal_patterns(combined_df, "combined")
    progress_bar(3, 8)
    # Analyze account behavior
    analyze_account_behavior(combined_df, "combined")
    progress_bar(4, 8)
    # Analyze correlation matrix
    correlation_matrix(combined_df, "combined")
    progress_bar(5, 8)
    # Analyze content
    analyze_content(combined_df, "combined")
    progress_bar(6, 8)
    # Analyze sentiment
    sentiment_analysis(combined_df, "combined")
    # Analyze network structures
    save_network_data(combined_df, "plots/network_data.json")
    progress_bar(7, 8)

    # Generate LLM-interpretable EDA context
    print("\nGenerating LLM-interpretable EDA outputs...")
    generate_llm_eda(combined_df)
    progress_bar(8, 8)

    print("EDA completed. Visualizations saved to 'plots' directory.")
    print("LLM-interpretable EDA context saved to 'llm_eda_context.json'")
    print("LLM-interpretable insights saved to 'llm_eda_context_insights.json'")
    print("\nNote: Each EDA function now returns JSON-compatible results in addition")
    print("to generating visualizations, making it easier to use them with LLMs.")


if __name__ == "__main__":
    eda()
