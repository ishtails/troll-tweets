"""Basic EDA functions"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def basic_stats(df, name):
    """
    Print basic statistics about the dataset and return them in JSON-compatible format.
    
    Args:
        df: DataFrame to analyze
        name: Name prefix for output files
        
    Returns:
        Dictionary with basic statistics in JSON-compatible format
    """
    print(f"\n=== Basic Statistics for {name} ===")
    print(f"Shape: {df.shape}")
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nData types:")
    print(df.dtypes)

    # Save descriptive statistics to CSV
    desc_stats = df.describe(include="all").T
    desc_stats.to_csv(f"plots/{name}_descriptive_stats.csv")
    
    # Create a JSON-compatible result
    result = {
        "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "missing_values": {col: int(df[col].isnull().sum()) for col in df.columns},
        "data_types": {col: str(df[col].dtype) for col in df.columns},
        "descriptive_stats": {}
    }
    
    # Add descriptive statistics
    for col in df.columns:
        col_stats = {}
        
        # Numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):
            col_stats = {
                "count": int(df[col].count()),
                "mean": float(df[col].mean()) if not pd.isna(df[col].mean()) else None,
                "std": float(df[col].std()) if not pd.isna(df[col].std()) else None,
                "min": float(df[col].min()) if not pd.isna(df[col].min()) else None,
                "25%": float(df[col].quantile(0.25)) if not pd.isna(df[col].quantile(0.25)) else None,
                "50%": float(df[col].quantile(0.5)) if not pd.isna(df[col].quantile(0.5)) else None,
                "75%": float(df[col].quantile(0.75)) if not pd.isna(df[col].quantile(0.75)) else None,
                "max": float(df[col].max()) if not pd.isna(df[col].max()) else None
            }
        
        # Categorical columns
        else:
            col_stats = {
                "count": int(df[col].count()),
                "unique": int(df[col].nunique()),
                "top_value": str(df[col].value_counts().index[0]) if not df[col].value_counts().empty else None,
                "top_count": int(df[col].value_counts().iloc[0]) if not df[col].value_counts().empty else None
            }
        
        result["descriptive_stats"][col] = col_stats
    
    return result


def analyze_categorical_features(df, name):
    """
    Analyze categorical features like region, language, account_type.
    
    Args:
        df: DataFrame to analyze
        name: Name prefix for output files
        
    Returns:
        Dictionary with categorical feature analysis in JSON-compatible format
    """
    categorical_features = ["region", "language", "account_type", "account_category"]
    
    # Initialize result dictionary
    result = {"categorical_features": {}}

    for feature in categorical_features:
        if feature in df.columns and not df[feature].dropna().empty:
            # Generate visualization
            plt.figure(figsize=(12, 6))
            counts = df[feature].value_counts().head(15)
            counts.plot(kind="bar")
            plt.title(f'Top 15 {feature.replace("_", " ").title()} Distribution')
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(f"plots/{name}_{feature}_distribution.png")
            plt.close()
            
            # Add feature data to result
            value_counts = df[feature].value_counts()
            total_count = value_counts.sum()
            
            # Store top 15 categories and their statistics
            feature_data = {
                "unique_values": int(df[feature].nunique()),
                "top_categories": {}
            }
            
            for category, count in value_counts.head(15).items():
                feature_data["top_categories"][str(category)] = {
                    "count": int(count),
                    "percentage": float(count / total_count * 100)
                }
                
            result["categorical_features"][feature] = feature_data
        else:
            print(f"Skipping {feature} as data is empty.")
    
    return result


def analyze_numerical_features(df, name):
    """
    Analyze numerical features with histograms and boxplots.
    
    Args:
        df: DataFrame to analyze
        name: Name prefix for output files
        
    Returns:
        Dictionary with numerical feature analysis in JSON-compatible format
    """
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
    
    # Initialize result dictionary
    result = {"numerical_features": {}}

    for feature in numerical_features:
        if feature in df.columns and not df[feature].dropna().empty:
            # Generate visualizations
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
            
            # Add feature statistics to result
            feature_data = {
                "count": int(df[feature].count()),
                "mean": float(df[feature].mean()) if not pd.isna(df[feature].mean()) else None,
                "std": float(df[feature].std()) if not pd.isna(df[feature].std()) else None,
                "min": float(df[feature].min()) if not pd.isna(df[feature].min()) else None,
                "25%": float(df[feature].quantile(0.25)) if not pd.isna(df[feature].quantile(0.25)) else None,
                "median": float(df[feature].median()) if not pd.isna(df[feature].median()) else None,
                "75%": float(df[feature].quantile(0.75)) if not pd.isna(df[feature].quantile(0.75)) else None,
                "max": float(df[feature].max()) if not pd.isna(df[feature].max()) else None
            }
            
            # Check for outliers using IQR method
            q1 = df[feature].quantile(0.25)
            q3 = df[feature].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)][feature]
            
            feature_data["outliers"] = {
                "count": int(len(outliers)),
                "percentage": float(len(outliers) / df[feature].count() * 100) if df[feature].count() > 0 else 0,
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound)
            }
            
            result["numerical_features"][feature] = feature_data
    
    return result


def analyze_temporal_patterns(df, name):
    """
    Analyze temporal patterns in the data.
    
    Args:
        df: DataFrame to analyze
        name: Name prefix for output files
        
    Returns:
        Dictionary with temporal pattern analysis in JSON-compatible format
    """
    # Initialize result dictionary
    result = {"has_temporal_data": False}
    
    if "publish_date" in df.columns and not df["publish_date"].dropna().empty:
        result["has_temporal_data"] = True
        df["date"] = pd.to_datetime(df["publish_date"], errors="coerce")

        # Hourly distribution
        if "hour_of_day" in df.columns and not df["hour_of_day"].dropna().empty:
            hourly_posts = df["hour_of_day"].value_counts().sort_index()
            
            # Generate visualization
            plt.figure(figsize=(12, 6))
            hourly_posts.plot(kind="bar")
            plt.title("Tweet Distribution by Hour of Day")
            plt.xlabel("Hour of Day")
            plt.ylabel("Number of Tweets")
            plt.xticks(rotation=0)
            plt.tight_layout()
            plt.savefig(f"plots/{name}_hourly_distribution.png")
            plt.close()
            
            # Add hourly distribution to result
            result["hourly_distribution"] = {
                str(hour): int(count) for hour, count in hourly_posts.items()
            }
            
            # Find peak hours (top 3)
            peak_hours = hourly_posts.nlargest(3)
            result["peak_hours"] = [
                {"hour": str(hour), "count": int(count)} 
                for hour, count in peak_hours.items()
            ]

        # Daily distribution
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
                # Generate visualization
                dow_posts_valid = dow_posts.loc[valid_indices]
                dow_posts_valid.index = [days[i] for i in dow_posts_valid.index]
                plt.figure(figsize=(12, 6))
                dow_posts_valid.plot(kind="bar")
                plt.title("Tweet Distribution by Day of Week")
                plt.xlabel("Day of Week")
                plt.ylabel("Number of Tweets")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(f"plots/{name}_dayofweek_distribution.png")
                plt.close()
                
                # Add daily distribution to result
                result["daily_distribution"] = {
                    days[i]: int(count) for i, count in zip(valid_indices, dow_posts_valid.values)
                }
                
                # Find peak days (top 3)
                peak_days = dow_posts_valid.nlargest(3)
                result["peak_days"] = [
                    {"day": day, "count": int(count)} 
                    for day, count in peak_days.items()
                ]
            else:
                print("Skipping day of week plot: No valid data.")
    
    return result


def analyze_account_behavior(df, name):
    """
    Analyze account behavior patterns.
    
    Args:
        df: DataFrame to analyze
        name: Name prefix for output files
        
    Returns:
        Dictionary with account behavior analysis in JSON-compatible format
    """
    # Initialize result dictionary
    result = {"has_account_behavior_data": False}
    
    # Retweet behavior by account category
    if "account_category" in df.columns and "retweet" in df.columns:
        result["has_account_behavior_data"] = True
        
        # Generate visualization
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
        
        # Add retweet behavior to result
        result["retweet_behavior"] = {
            str(category): float(ratio) 
            for category, ratio in retweet_by_category.items()
        }
        
        # Identify categories with highest and lowest retweet ratios
        if not retweet_by_category.empty:
            result["highest_retweet_category"] = {
                "category": str(retweet_by_category.index[0]),
                "ratio": float(retweet_by_category.iloc[0])
            }
            result["lowest_retweet_category"] = {
                "category": str(retweet_by_category.index[-1]),
                "ratio": float(retweet_by_category.iloc[-1])
            }

    # Follower/Following analysis by account category
    if (
        "account_category" in df.columns
        and "followers" in df.columns
        and "following" in df.columns
    ):
        result["has_account_behavior_data"] = True
        
        # Generate visualization
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
        
        # Add follower/following stats to result
        result["follower_following_stats"] = {}
        for category in stats.index:
            result["follower_following_stats"][str(category)] = {
                "median_followers": int(stats.loc[category, "followers"]),
                "median_following": int(stats.loc[category, "following"]),
                "followers_to_following_ratio": float(
                    stats.loc[category, "followers"] / stats.loc[category, "following"]
                    if stats.loc[category, "following"] > 0 else 0
                )
            }
        
        # Calculate influence ratio (followers/following) for each category
        influence_ratio = stats["followers"] / stats["following"].replace(0, 1)
        most_influential = influence_ratio.nlargest(1)
        least_influential = influence_ratio.nsmallest(1)
        
        if not most_influential.empty:
            result["most_influential_category"] = {
                "category": str(most_influential.index[0]),
                "influence_ratio": float(most_influential.iloc[0])
            }
        
        if not least_influential.empty:
            result["least_influential_category"] = {
                "category": str(least_influential.index[0]),
                "influence_ratio": float(least_influential.iloc[0])
            }
    
    return result
