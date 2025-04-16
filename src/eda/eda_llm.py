"""
Framework for generating LLM-interpretable EDA results.

This module contains functions to generate structured summaries of EDA results
that can be consumed by Large Language Models (LLMs) to understand dataset
characteristics and patterns.
"""

import json
from typing import Dict, Any
from collections import Counter
import pandas as pd
from .eda_network import analyze_networks


def dataset_overview(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a comprehensive dataset overview for LLM consumption.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with dataset overview information
    """
    overview = {
        "dataset_shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "column_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": {col: int(df[col].isna().sum()) for col in df.columns},
        "numerical_columns": list(
            df.select_dtypes(include=["int64", "float64"]).columns
        ),
        "categorical_columns": list(
            df.select_dtypes(include=["object", "category"]).columns
        ),
        "temporal_columns": [
            col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])
        ],
    }

    # Add descriptive statistics for numerical columns
    overview["numerical_summary"] = {}
    for col in overview["numerical_columns"]:
        if col in df.columns:
            overview["numerical_summary"][col] = {
                "min": float(df[col].min()) if not pd.isna(df[col].min()) else None,
                "max": float(df[col].max()) if not pd.isna(df[col].max()) else None,
                "mean": float(df[col].mean()) if not pd.isna(df[col].mean()) else None,
                "median": (
                    float(df[col].median()) if not pd.isna(df[col].median()) else None
                ),
                "std": float(df[col].std()) if not pd.isna(df[col].std()) else None,
                "has_outliers": outlier_check(df[col]),
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
    result = {}
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    for col in categorical_cols:
        if col in df.columns:
            value_counts = df[col].value_counts()
            total_count = len(df[col].dropna())

            result[col] = {
                "unique_values": int(df[col].nunique()),
                "most_common": (
                    value_counts.index[0] if not value_counts.empty else None
                ),
                "distribution": {
                    str(k): {
                        "count": int(v),
                        "percentage": (
                            float(v / total_count * 100) if total_count > 0 else 0
                        ),
                    }
                    for k, v in value_counts.head(10).items()
                },
            }

    return result


def numerical_feature_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze numerical features for LLM consumption.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with numerical feature analysis
    """
    result = {}
    numerical_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    for col in numerical_cols:
        if col in df.columns:
            # Calculate percentiles
            percentiles = df[col].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).to_dict()

            result[col] = {
                "distribution": {
                    "percentiles": {
                        str(int(k * 100)) + "%": float(v)
                        for k, v in percentiles.items()
                    },
                    "skewness": (
                        float(df[col].skew()) if not pd.isna(df[col].skew()) else None
                    ),
                    "kurtosis": (
                        float(df[col].kurtosis())
                        if not pd.isna(df[col].kurtosis())
                        else None
                    ),
                },
                "correlation": {},
            }

            # Add correlations with other numerical features
            for other_col in numerical_cols:
                if other_col != col and df[col].std() > 0 and df[other_col].std() > 0:
                    corr = df[col].corr(df[other_col])
                    if not pd.isna(corr):
                        result[col]["correlation"][other_col] = float(corr)

    return result


def temporal_pattern_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze temporal patterns for LLM consumption.

    Args:
        df: Dataset with 'date' column

    Returns:
        Dictionary with temporal pattern analysis
    """
    result = {"has_temporal_data": False}

    if "hour_of_day" in df.columns and not df["hour_of_day"].dropna().empty:
        hourly_distribution = df["hour_of_day"].value_counts().sort_index()
        result["hourly_distribution"] = {
            str(hour): int(count) for hour, count in hourly_distribution.items()
        }
        result["peak_hours"] = [
            int(hour) for hour in hourly_distribution.nlargest(3).index.tolist()
        ]
        result["has_temporal_data"] = True

    if "day_of_week" in df.columns and not df["day_of_week"].dropna().empty:
        day_distribution = df["day_of_week"].value_counts().sort_index()
        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        result["daily_distribution"] = {
            days[day] if day < len(days) else f"Unknown({day})": int(count)
            for day, count in day_distribution.items()
            if 0 <= day < 7
        }
        result["has_temporal_data"] = True

    return result


def nlp_feature_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze NLP features for LLM consumption.

    Args:
        df: Dataset DataFrame

    Returns:
        Dictionary with NLP feature analysis
    """
    result = {"has_nlp_features": False}

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

    # Feature statistics
    feature_stats = {}
    for feature in nlp_features:
        if feature in df.columns and not df[feature].dropna().empty:
            feature_stats[feature] = {
                "mean": (
                    float(df[feature].mean())
                    if not pd.isna(df[feature].mean())
                    else None
                ),
                "median": (
                    float(df[feature].median())
                    if not pd.isna(df[feature].median())
                    else None
                ),
                "std": (
                    float(df[feature].std()) if not pd.isna(df[feature].std()) else None
                ),
            }
            result["has_nlp_features"] = True

    if result["has_nlp_features"]:
        result["feature_stats"] = feature_stats

    # Correlations between NLP features
    if result["has_nlp_features"]:
        nlp_cols = [col for col in nlp_features if col in df.columns]
        if len(nlp_cols) > 1:
            corr_matrix = df[nlp_cols].corr().round(2).fillna('NaN').to_dict()
            result["feature_correlations"] = corr_matrix

    # Extract top hashtags if available
    if "hashtags" in df.columns and not df["hashtags"].dropna().empty:
        all_hashtags = [
            tag for tags in df["hashtags"].dropna() for tag in tags.split(", ") if tag
        ]
        if all_hashtags:
            top_hashtags = Counter(all_hashtags).most_common(10)
            result["top_hashtags"] = {tag: int(count) for tag, count in top_hashtags}
            result["has_nlp_features"] = True

    return result


def sentiment_analysis_for_llm(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform sentiment analysis for LLM consumption.

    Args:
        df: Dataset DataFrame with 'content' column

    Returns:
        Dictionary with sentiment analysis results
    """
    result = {"has_sentiment_data": False}

    if "sentiment" in df.columns and not df["sentiment"].dropna().empty:
        result["sentiment_distribution"] = {
            "mean": float(df["sentiment"].mean()),
            "median": float(df["sentiment"].median()),
            "std": float(df["sentiment"].std()),
            "positive_ratio": float((df["sentiment"] > 0.05).mean()),
            "neutral_ratio": float((df["sentiment"].between(-0.05, 0.05)).mean()),
            "negative_ratio": float((df["sentiment"] < -0.05).mean()),
        }
        result["has_sentiment_data"] = True

        # Sentiment by category if available
        if "account_category" in df.columns:
            sentiment_by_category = (
                df.groupby("account_category")["sentiment"].mean().to_dict()
            )
            result["sentiment_by_category"] = {
                str(k): float(v) for k, v in sentiment_by_category.items()
            }

        # Sentiment by region if available
        if "region" in df.columns:
            sentiment_by_region = df.groupby("region")["sentiment"].mean().to_dict()
            result["sentiment_by_region"] = {
                str(k): float(v) for k, v in sentiment_by_region.items()
            }

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

    # Filter and format the data for LLM consumption
    result = {
        "has_network_data": network_data["summary"]["has_networks"],
        "summary": network_data["summary"],
    }

    # Include simplified versions of the networks
    if network_data["hashtag_network"]["has_network"]:
        # Include only top 10 nodes and edges for brevity
        top_nodes = sorted(
            network_data["hashtag_network"]["nodes"],
            key=lambda x: x["weight"],
            reverse=True,
        )[:10]

        # Get the IDs of the top nodes
        top_node_ids = [node["id"] for node in top_nodes]

        # Filter edges to only include those connecting top nodes
        top_edges = [
            edge
            for edge in network_data["hashtag_network"]["edges"]
            if edge["source"] in top_node_ids and edge["target"] in top_node_ids
        ]

        result["hashtag_network"] = {
            "top_nodes": top_nodes,
            "top_edges": top_edges[:20],  # Limit to 20 edges for simplicity
        }

    if network_data["mention_network"]["has_network"]:
        # Include only top 10 nodes and edges for brevity
        top_nodes = sorted(
            network_data["mention_network"]["nodes"],
            key=lambda x: x["weight"],
            reverse=True,
        )[:10]

        # Get the IDs of the top nodes
        top_node_ids = [node["id"] for node in top_nodes]

        # Filter edges to only include those connecting top nodes
        top_edges = [
            edge
            for edge in network_data["mention_network"]["edges"]
            if edge["source"] in top_node_ids and edge["target"] in top_node_ids
        ]

        result["mention_network"] = {
            "top_nodes": top_nodes,
            "top_edges": top_edges[:20],  # Limit to 20 edges for simplicity
        }

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
            top_category = max(
                analysis["distribution"].items(),
                key=lambda x: (
                    x[1]["percentage"]
                    if isinstance(x[1], dict) and "percentage" in x[1]
                    else 0
                ),
            )[0]
            insights["distributions"][feature] = {
                "top_category": top_category,
                "imbalance_ratio": max(
                    [
                        item["percentage"]
                        for item in analysis["distribution"].values()
                        if isinstance(item, dict) and "percentage" in item
                    ],
                    default=0,
                ),
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
    for feature, analysis in summary["dataset_overview"]["numerical_summary"].items():
        if analysis.get("has_outliers", False):
            insights["anomalies"].append(
                {
                    "feature": feature,
                    "description": "Contains outliers that may affect analysis",
                }
            )

    # Add network insights if available
    if summary["network_analysis"]["has_network_data"]:
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
                        "top_nodes"
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
                        "top_nodes"
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
