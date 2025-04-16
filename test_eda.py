"""
Test script for modified EDA functions.
"""

import pandas as pd
from src.eda.eda_nlp import sentiment_analysis
from src.eda.eda_basic import basic_stats, analyze_categorical_features
from src.eda.eda_llm import generate_llm_summary

def main():
    """Run tests on the EDA functions"""
    # Create a small test DataFrame
    test_df = pd.DataFrame({
        'content': ['This is a positive tweet', 'This is a negative tweet'],
        'sentiment': [0.5, -0.3],
        'account_category': ['bot', 'human'],
        'region': ['US', 'EU'],
        'day_of_week': [1, 3],
        'hour_of_day': [12, 15]
    })
    
    # Test sentiment_analysis
    print("\n== Testing sentiment_analysis ==")
    sentiment_result = sentiment_analysis(test_df, 'test')
    print(f"Result has sentiment data: {'has_sentiment_data' in sentiment_result}")
    print(f"Keys in result: {list(sentiment_result.keys())}")
    
    # Test basic_stats
    print("\n== Testing basic_stats ==")
    stats_result = basic_stats(test_df, 'test')
    print(f"Shape in result: {'shape' in stats_result}")
    print(f"Keys in result: {list(stats_result.keys())}")
    
    # Test analyze_categorical_features
    print("\n== Testing analyze_categorical_features ==")
    cat_result = analyze_categorical_features(test_df, 'test')
    print(f"Result has categorical features: {'categorical_features' in cat_result}")
    if 'categorical_features' in cat_result:
        print(f"Features analyzed: {list(cat_result['categorical_features'].keys())}")
    
    # Test generate_llm_summary
    print("\n== Testing generate_llm_summary ==")
    try:
        summary_result = generate_llm_summary(test_df)
        print(f"Result is a dictionary: {isinstance(summary_result, dict)}")
        print(f"Keys in summary: {list(summary_result.keys())}")
        print("\nAll tests completed successfully!")
    except Exception as e:
        print(f"Error in generate_llm_summary: {str(e)}")
    

if __name__ == "__main__":
    main() 