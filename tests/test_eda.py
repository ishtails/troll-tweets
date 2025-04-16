"""Test the EDA module"""

import os
import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock
import tempfile
import shutil
from pathlib import Path

# Import the functions to test
from src.eda.eda import (
    basic_stats,
    analyze_categorical_features,
    analyze_numerical_features,
    analyze_temporal_patterns,
    analyze_account_behavior,
    analyze_nlp_features,
    analyze_content,
    clean_text,
    sentiment_analysis,
    run_eda,
)


class TestEDA(unittest.TestCase):
    """Tests for the EDA module"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for test plots
        self.test_dir = tempfile.mkdtemp()
        # Store original directory
        self.original_dir = os.getcwd()
        # Change to test directory
        os.chdir(self.test_dir)
        # Create plots directory
        os.makedirs("plots", exist_ok=True)

        # Sample data with all required columns for testing
        self.sample_data = pd.DataFrame(
            {
                # Categorical features
                "region": ["US", "Russia", "China", "UK", "Germany", None],
                "language": ["en", "ru", "zh", "en", "de", None],
                "account_type": ["bot", "human", "bot", "human", "bot", None],
                "account_category": [
                    "RightTroll",
                    "LeftTroll",
                    "Commercial",
                    "NonEnglish",
                    "NewsFeeds",
                    None,
                ],
                # Numerical features
                "following": [100, 500, 1000, 1500, 2000, np.nan],
                "followers": [200, 1000, 50, 3000, 100, np.nan],
                "updates": [50, 200, 300, 400, 500, np.nan],
                "followers_to_following_ratio": [2.0, 2.0, 0.05, 2.0, 0.05, np.nan],
                "count_hashtags": [2, 5, 0, 10, 3, np.nan],
                "count_mentions": [1, 3, 0, 5, 2, np.nan],
                "count_emojis": [0, 2, 4, 0, 1, np.nan],
                "word_count": [15, 25, 5, 50, 10, np.nan],
                "text_length": [80, 140, 20, 280, 60, np.nan],
                "count_special_characters": [5, 10, 2, 20, 8, np.nan],
                # Boolean features
                "all_words_caps": [True, False, True, False, True, None],
                "starts_with_hashtag": [True, False, False, True, True, None],
                "starts_with_mention": [False, True, False, False, True, None],
                "retweet": [True, False, True, False, True, None],
                # Temporal features
                "publish_date": pd.to_datetime(
                    [
                        "2018-01-01",
                        "2018-01-02",
                        "2018-01-03",
                        "2018-01-04",
                        "2018-01-05",
                        None,
                    ]
                ),
                "hour_of_day": [0, 6, 12, 18, 23, np.nan],
                "day_of_week": [0, 1, 2, 3, 4, np.nan],
                # Content features
                "content": [
                    "This is a sample tweet #politics @user",
                    "Русский текст с хэштегом #russia and some emoji 😊",
                    "ALL CAPS TWEET WITH NO TAGS",
                    "A very long tweet with multiple hashtags #one #two #three #four #five and mentions @user1 @user2 @user3",
                    "Short text",
                    None,
                ],
                "hashtags": [
                    "#politics",
                    "#russia",
                    "",
                    "#one, #two, #three, #four, #five",
                    "",
                    None,
                ],
            }
        )

        # Create edge cases dataframe
        self.edge_data = pd.DataFrame(
            {
                # Empty dataframe with correct columns
                "region": [],
                "language": [],
                "account_type": [],
                "account_category": [],
                "following": [],
                "followers": [],
                "updates": [],
                "followers_to_following_ratio": [],
                "count_hashtags": [],
                "count_mentions": [],
                "count_emojis": [],
                "word_count": [],
                "text_length": [],
                "publish_date": [],
                "content": [],
                "hashtags": [],
            }
        )

        # Minimal dataframe with only content
        self.minimal_data = pd.DataFrame(
            {"content": ["This is a minimal tweet", "Another minimal tweet"]}
        )

        # Extreme values dataframe
        self.extreme_data = pd.DataFrame(
            {
                "following": [0, 1000000],
                "followers": [0, 2000000],
                "content": ["", "a" * 1000],  # Empty and very long text
            }
        )

    def tearDown(self):
        """Tear down test fixtures"""
        # Change back to original directory
        os.chdir(self.original_dir)
        # Remove test directory
        shutil.rmtree(self.test_dir)
        # Close all plt figures
        plt.close("all")

    def test_basic_stats(self):
        """Test the basic_stats function"""
        with patch("builtins.print") as mock_print:
            stats = basic_stats(self.sample_data, "test")
            # Check if the function creates the expected output file
            self.assertTrue(os.path.exists("plots/test_descriptive_stats.csv"))
            # Check if stats are returned
            self.assertIsInstance(stats, pd.DataFrame)
            # Ensure print was called (basic validation)
            self.assertTrue(mock_print.called)

        # Test with empty dataframe
        with patch("builtins.print") as mock_print:
            stats_empty = basic_stats(self.edge_data, "empty")
            self.assertTrue(os.path.exists("plots/empty_descriptive_stats.csv"))
            self.assertIsInstance(stats_empty, pd.DataFrame)

    def test_analyze_categorical_features(self):
        """Test the analyze_categorical_features function"""
        # Test with sample data
        analyze_categorical_features(self.sample_data, "test")
        # Check if the function creates the expected output files
        for feature in ["region", "language", "account_type", "account_category"]:
            self.assertTrue(os.path.exists(f"plots/test_{feature}_distribution.png"))

        # Test with empty dataframe
        analyze_categorical_features(self.edge_data, "empty")
        # Should not error but may not create files

        # Test with missing categorical features
        analyze_categorical_features(self.minimal_data, "minimal")
        # Should not error

    def test_analyze_numerical_features(self):
        """Test the analyze_numerical_features function"""
        # Test with sample data
        analyze_numerical_features(self.sample_data, "test")
        # Check if the function creates the expected output files
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
            self.assertTrue(os.path.exists(f"plots/test_{feature}_analysis.png"))

        # Test with extreme values
        analyze_numerical_features(self.extreme_data, "extreme")
        self.assertTrue(os.path.exists("plots/extreme_following_analysis.png"))
        self.assertTrue(os.path.exists("plots/extreme_followers_analysis.png"))

        # Test with empty dataframe
        analyze_numerical_features(self.edge_data, "empty")
        # Should not error

    def test_analyze_temporal_patterns(self):
        """Test the analyze_temporal_patterns function"""
        # Test with sample data
        analyze_temporal_patterns(self.sample_data, "test")
        # Check if the function creates the expected output files
        self.assertTrue(os.path.exists("plots/test_hourly_distribution.png"))
        self.assertTrue(os.path.exists("plots/test_dayofweek_distribution.png"))

        # Test with no temporal data
        analyze_temporal_patterns(self.minimal_data, "minimal")
        # Should not error

        # Create data with string dates that need conversion
        string_dates_df = pd.DataFrame(
            {"publish_date": ["2018-01-01", "2018-01-02", "2018-01-03"]}
        )
        analyze_temporal_patterns(string_dates_df, "string_dates")
        # Should handle conversion

    def test_analyze_account_behavior(self):
        """Test the analyze_account_behavior function"""
        # Test with sample data
        analyze_account_behavior(self.sample_data, "test")
        # Check if the function creates the expected output files
        self.assertTrue(os.path.exists("plots/test_retweet_by_category.png"))
        self.assertTrue(os.path.exists("plots/test_follower_following_by_category.png"))

        # Test with data missing required columns
        analyze_account_behavior(self.minimal_data, "minimal")
        # Should not error

    def test_analyze_nlp_features(self):
        """Test the analyze_nlp_features function"""
        # Test with sample data
        analyze_nlp_features(self.sample_data, "test")
        # Check if the function creates the expected output files
        self.assertTrue(os.path.exists("plots/test_nlp_feature_correlation.png"))

        for feature in ["starts_with_hashtag", "starts_with_mention"]:
            self.assertTrue(os.path.exists(f"plots/test_{feature}_pie.png"))

        # Test with data missing required columns
        analyze_nlp_features(self.minimal_data, "minimal")
        # Should not error

    def test_analyze_content(self):
        """Test the analyze_content function"""
        # Test with sample data
        analyze_content(self.sample_data, "test")
        # Check if the function creates the expected output files
        self.assertTrue(os.path.exists("plots/test_content_wordcloud.png"))
        self.assertTrue(os.path.exists("plots/test_hashtags_wordcloud.png"))
        self.assertTrue(os.path.exists("plots/test_top_hashtags.png"))

        # Test with minimal data
        analyze_content(self.minimal_data, "minimal")
        self.assertTrue(os.path.exists("plots/minimal_content_wordcloud.png"))

        # Test with empty content
        empty_content_df = pd.DataFrame({"content": [""]})
        analyze_content(empty_content_df, "empty_content")
        # Should not error

    def test_clean_text(self):
        """Test the clean_text function"""
        # Test normal text cleaning
        test_text = (
            "This is a @mention with #hashtag and http://example.com link 123 😊"
        )
        cleaned = clean_text(test_text)
        # Check if cleaning is working as expected
        self.assertNotIn("@mention", cleaned)
        self.assertNotIn("#hashtag", cleaned)
        self.assertNotIn("http", cleaned)
        self.assertNotIn("123", cleaned)
        self.assertNotIn("😊", cleaned)

        # Test empty text
        self.assertEqual(clean_text(""), "")

        # Test text with only elements to be removed
        only_removable = "@user #tag http://t.co 123 😊"
        self.assertEqual(clean_text(only_removable).strip(), "")

    def test_sentiment_analysis(self):
        """Test the sentiment_analysis function"""
        # Test with sample data
        sentiment_analysis(self.sample_data, "test")
        # Check if the function creates the expected output files
        self.assertTrue(os.path.exists("plots/test_sentiment_histogram.png"))
        self.assertTrue(os.path.exists("plots/test_sentiment_by_category.png"))
        self.assertTrue(os.path.exists("plots/test_sentiment_by_region.png"))
        self.assertTrue(os.path.exists("plots/test_outlier_analysis.png"))

        # Test with minimal data
        sentiment_analysis(self.minimal_data, "minimal")
        self.assertTrue(os.path.exists("plots/minimal_sentiment_histogram.png"))

        # Test with missing content column
        no_content_df = pd.DataFrame({"other_column": [1, 2, 3]})
        with self.assertRaises(ValueError):
            sentiment_analysis(no_content_df, "no_content")

    @patch("src.eda.eda.load_data")
    @patch("src.eda.eda.basic_stats")
    @patch("src.eda.eda.analyze_categorical_features")
    @patch("src.eda.eda.analyze_numerical_features")
    @patch("src.eda.eda.analyze_temporal_patterns")
    @patch("src.eda.eda.analyze_account_behavior")
    @patch("src.eda.eda.analyze_nlp_features")
    @patch("src.eda.eda.analyze_content")
    @patch("src.eda.eda.sentiment_analysis")
    @patch("builtins.print")
    def test_run_eda(
        self,
        mock_print,
        mock_sentiment,
        mock_content,
        mock_nlp,
        mock_account,
        mock_temporal,
        mock_numerical,
        mock_categorical,
        mock_basic,
        mock_load,
    ):
        """Test the run_eda function"""
        # Mock load_data to return our test dataframes
        mock_load.return_value = (self.sample_data, self.sample_data, self.sample_data)

        # Call the function under test
        run_eda()

        # Check that all expected functions were called
        mock_load.assert_called_once()
        mock_basic.assert_called()
        mock_categorical.assert_called_once()
        mock_numerical.assert_called_once()
        mock_temporal.assert_called_once()
        mock_account.assert_called_once()
        mock_nlp.assert_called_once()
        mock_content.assert_called_once()
        mock_sentiment.assert_called_once()

        # Final print should be called
        self.assertIn("EDA completed", mock_print.call_args_list[-1][0][0])


if __name__ == "__main__":
    unittest.main()
