"""Utility functions for the project"""

import pandas as pd


def load_data():
    """Load both the trimmed and derived datasets"""
    # fetch 1 to 5 from data/raw
    trimmed_df1 = pd.read_csv("data/raw/1_trimmed.csv")
    trimmed_df2 = pd.read_csv("data/raw/2_trimmed.csv")
    trimmed_df3 = pd.read_csv("data/raw/3_trimmed.csv")
    trimmed_df4 = pd.read_csv("data/raw/4_trimmed.csv")
    trimmed_df5 = pd.read_csv("data/raw/5_trimmed.csv")

    derived_df1 = pd.read_csv("data/raw/1_derived.csv")
    derived_df2 = pd.read_csv("data/raw/2_derived.csv")
    derived_df3 = pd.read_csv("data/raw/3_derived.csv")
    derived_df4 = pd.read_csv("data/raw/4_derived.csv")
    derived_df5 = pd.read_csv("data/raw/5_derived.csv")

    combined_raw_df = pd.concat(
        [trimmed_df1, trimmed_df2, trimmed_df3, trimmed_df4, trimmed_df5], axis=0
    )
    combined_derived_df = pd.concat(
        [derived_df1, derived_df2, derived_df3, derived_df4, derived_df5], axis=0
    )
    combined_df = pd.concat([combined_raw_df, combined_derived_df], axis=1)

    # Handle duplicated columns (if any)
    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

    return combined_raw_df, combined_derived_df, combined_df
