"""
Framework for generating LLM-interpretable EDA results.

This module contains functions to generate structured summaries of EDA results
that can be consumed by Large Language Models (LLMs) to understand dataset
characteristics and patterns. Each function now uses the appropriate EDA function
from other modules, which have been updated to return JSON-compatible data in 
addition to generating visualizations.
"""

import json
import pandas as pd
from typing import Dict, Any

# Import EDA functions from other modules
from .eda_network import analyze_networks
from .eda_nlp import sentiment_analysis, correlation_matrix, analyze_content
from .eda_basic import (
    basic_stats, 
    analyze_categorical_features, 
    analyze_numerical_features, 
    analyze_temporal_patterns, 
    analyze_account_behavior
)


def dataset_overview(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a comprehensive dataset overview for LLM consumption.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with dataset overview information
    """
    # Use the basic_stats function to get comprehensive statistics
    basic_stats_result = basic_stats(df, "llm_analysis")
    
    # Create a simplified overview from the comprehensive statistics
    overview = {
        "dataset_shape": basic_stats_result["shape"],
        "missing_values": basic_stats_result["missing_values"],
        "column_types": basic_stats_result["data_types"],
        "numerical_columns": [
            col for col, dtype in basic_stats_result["data_types"].items()
            if dtype.startswith(("int", "float"))
        ],
        "categorical_columns": [
            col for col, dtype in basic_stats_result["data_types"].items()
            if dtype.startswith(("object", "category"))
        ],
        "temporal_columns": [
            col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])
        ],
        "detailed_stats": basic_stats_result["descriptive_stats"]
    }
    
    return overview


def outlier_check(series: pd.Series) -> bool:
    """Check if a series has outliers using IQR method"""
    if series.empty or not pd.api.types.is_numeric_dtype(series):
        return False

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    return ((series < lower_bound) | (series > upper_bound)).any()


def categorical_feature_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze categorical features for LLM consumption.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with categorical feature analysis
    """
    # Use the analyze_categorical_features function from eda_basic.py
    # This will perform the analysis and generate visualizations
    categorical_result = analyze_categorical_features(df, "llm_analysis")
    
    return categorical_result["categorical_features"]


def numerical_feature_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze numerical features for LLM consumption.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with numerical feature analysis
    """
    # Use the analyze_numerical_features function from eda_basic.py
    # This will perform the analysis and generate visualizations
    numerical_result = analyze_numerical_features(df, "llm_analysis")
    
    return numerical_result["numerical_features"]


def temporal_pattern_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze temporal patterns for LLM consumption.

    Args:
        df: Dataset with 'date' column

    Returns:
        Dictionary with temporal pattern analysis
    """
    # Use the analyze_temporal_patterns function from eda_basic.py
    # This will perform the analysis and generate visualizations
    temporal_result = analyze_temporal_patterns(df, "llm_analysis")
    
    return temporal_result


def nlp_feature_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze NLP features for LLM consumption.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with NLP feature analysis
    """
    # Get correlation analysis from eda_nlp.py
    corr_result = correlation_matrix(df, "llm_analysis")
    
    # Get content analysis from eda_nlp.py
    content_result = analyze_content(df, "llm_analysis")
    
    # Set the flag if any NLP features are found
    result = {"has_nlp_features": False}
    result["has_nlp_features"] = (
        corr_result.get("has_nlp_correlations", False) or 
        content_result.get("has_content_data", False) or
        content_result.get("has_hashtag_data", False) or
        content_result.get("has_special_format_data", False)
    )
    
    # Combine the results
    if result["has_nlp_features"]:
        # Add correlation data if available
        if corr_result.get("has_nlp_correlations", False):
            result["feature_correlations"] = corr_result
            
        # Add content analysis if available
        if content_result:
            if content_result.get("has_content_data", False):
                result["content_analysis"] = {
                    "top_words": content_result.get("top_words", [])
                }
                
            if content_result.get("has_hashtag_data", False):
                result["hashtag_analysis"] = {
                    "top_hashtags": content_result.get("top_hashtags", [])
                }
                
            if content_result.get("has_special_format_data", False):
                result["special_format_stats"] = content_result.get("special_format_stats", {})
    
    return result


def sentiment_analysis_for_llm(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform sentiment analysis for LLM consumption.

    Args:
        df: Dataset DataFrame with 'content' column

    Returns:
        Dictionary with sentiment analysis results
    """
    # Use the sentiment_analysis function from eda_nlp.py
    # This will perform the analysis and generate visualizations
    # The returned result is already in JSON-compatible format
    result = sentiment_analysis(df, "llm_analysis")
    
    return result


def network_analysis_for_llm(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform network analysis for LLM consumption.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with network analysis results
    """
    # Use the analyze_networks function from eda_network.py
    network_data = analyze_networks(df)
    
    # The analyze_networks function has been updated to return JSON-compatible results directly
    return network_data


def account_behavior_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze account behavior patterns for LLM consumption.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with account behavior analysis
    """
    # Use the analyze_account_behavior function from eda_basic.py
    # This will perform the analysis and generate visualizations
    result = analyze_account_behavior(df, "llm_analysis")
    
    return result


def generate_llm_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a comprehensive summary of EDA results for LLM consumption.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with comprehensive EDA results
    """
    summary = {
        "dataset_overview": dataset_overview(df),
        "categorical_analysis": categorical_feature_analysis(df),
        "numerical_analysis": numerical_feature_analysis(df),
        "temporal_analysis": temporal_pattern_analysis(df),
        "nlp_analysis": nlp_feature_analysis(df),
        "sentiment_analysis": sentiment_analysis_for_llm(df),
        "network_analysis": network_analysis_for_llm(df),
        "account_behavior_analysis": account_behavior_analysis(df),
    }

    # Generate metadata
    summary["metadata"] = {
        "dataset_name": "Twitter Troll Dataset",
        "analysis_timestamp": pd.Timestamp.now().isoformat(),
        "number_of_features": df.shape[1],
        "number_of_samples": df.shape[0],
    }

    return summary


def save_llm_context(
    df: pd.DataFrame, output_path: str = "llm_eda_context.json"
) -> None:
    """
    Generate and save the LLM-interpretable EDA context to a JSON file.

    Args:
        df: Dataset DataFrame
        output_path: Path to save the JSON output
    """
    summary = generate_llm_summary(df)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

    print(f"LLM-interpretable EDA context saved to {output_path}")


def generate_llm_insights(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate insights from the data in a format suitable for LLMs.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with key insights from the data
    """
    summary = generate_llm_summary(df)

    # Extract key patterns and anomalies
    insights = {
        "key_patterns": [],
        "anomalies": [],
        "distributions": {},
        "correlations": [],
        "networks": {},
    }

    # Find categorical distributions of interest
    for feature, analysis in summary["categorical_analysis"].items():
        if analysis["unique_values"] > 1:
            # Get top category from top_categories
            if "top_categories" in analysis and analysis["top_categories"]:
                # Find category with highest count
                top_category = max(
                    analysis["top_categories"].items(),
                    key=lambda x: x[1]["count"] if isinstance(x[1], dict) and "count" in x[1] else 0
                )[0]
                
                # Calculate imbalance ratio from top category percentage
                top_percentage = analysis["top_categories"][top_category]["percentage"]
                
                insights["distributions"][feature] = {
                    "top_category": top_category,
                    "imbalance_ratio": top_percentage,
                }

    # Find strong correlations
    for feature, analysis in summary["numerical_analysis"].items():
        if "correlation" in analysis:
            strong_correlations = {
                other_feat: corr
                for other_feat, corr in analysis["correlation"].items()
                if abs(corr) > 0.7
            }
            if strong_correlations:
                for other_feat, corr_value in strong_correlations.items():
                    insights["correlations"].append(
                        {
                            "feature1": feature,
                            "feature2": other_feat,
                            "correlation": corr_value,
                        }
                    )

    # Identify temporal patterns if available
    if summary["temporal_analysis"]["has_temporal_data"]:
        if "peak_hours" in summary["temporal_analysis"]:
            insights["key_patterns"].append(
                {
                    "pattern_type": "temporal",
                    "description": f"Peak activity hours: {summary['temporal_analysis']['peak_hours']}",
                }
            )

    # Identify sentiment patterns if available
    if summary["sentiment_analysis"]["has_sentiment_data"]:
        sentiment_ratio = summary["sentiment_analysis"]["sentiment_distribution"]
        dominant_sentiment = max(
            ["positive", "neutral", "negative"],
            key=lambda x: sentiment_ratio.get(f"{x}_ratio", 0),
        )
        insights["key_patterns"].append(
            {
                "pattern_type": "sentiment",
                "description": f"Dominant sentiment is {dominant_sentiment} ({sentiment_ratio.get(f'{dominant_sentiment}_ratio', 0)*100:.1f}%)",
            }
        )

    # Identify outliers in numerical features
    for feature, analysis in summary["numerical_analysis"].items():
        if "outliers" in analysis and analysis["outliers"]["count"] > 0:
            insights["anomalies"].append(
                {
                    "feature": feature,
                    "description": f"Contains {analysis['outliers']['count']} outliers ({analysis['outliers']['percentage']:.1f}% of data)"
                }
            )

    # Add network insights if available
    if summary["network_analysis"]["summary"]["has_networks"]:
        network_summary = summary["network_analysis"]["summary"]

        # Add hashtag network insights
        if network_summary["hashtag_network_size"] > 0:
            insights["networks"]["hashtag_network"] = {
                "size": network_summary["hashtag_network_size"],
                "density": network_summary["hashtag_network_density"],
                "description": (
                    "Dense"
                    if network_summary["hashtag_network_density"] > 0.5
                    else "Sparse"
                )
                + " hashtag co-occurrence network",
            }

            if "hashtag_network" in summary["network_analysis"]:
                # Add top hashtags from the network
                insights["networks"]["top_hashtags"] = [
                    {"tag": node["id"], "weight": node["weight"]}
                    for node in summary["network_analysis"]["hashtag_network"][
                        "nodes"
                    ][:5]
                ]

        # Add mention network insights
        if network_summary["mention_network_size"] > 0:
            insights["networks"]["mention_network"] = {
                "size": network_summary["mention_network_size"],
                "density": network_summary["mention_network_density"],
                "description": (
                    "Dense"
                    if network_summary["mention_network_density"] > 0.5
                    else "Sparse"
                )
                + " mention network",
            }

            if "mention_network" in summary["network_analysis"]:
                # Add top mentions from the network
                insights["networks"]["top_mentions"] = [
                    {"mention": node["id"], "weight": node["weight"]}
                    for node in summary["network_analysis"]["mention_network"][
                        "nodes"
                    ][:5]
                ]

    return insights


def generate_llm_eda(df, output_path="llm_eda_context.json"):
    """Generate LLM-interpretable EDA results"""
    print("\nGenerating LLM-interpretable EDA context...")
    save_llm_context(df, output_path)

    # Also generate and save insights
    insights = generate_llm_insights(df)
    insights_path = output_path.replace(".json", "_insights.json")
    with open(insights_path, "w", encoding="utf-8") as f:
        json.dump(insights, f, indent=2, ensure_ascii=False)
    print(f"LLM-interpretable insights saved to {insights_path}")
