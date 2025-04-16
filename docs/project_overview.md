# Twitter Troll Detection: Exploratory Data Analysis

## Project Overview

This repository contains the code and analysis for my thesis on identifying and analyzing Twitter troll accounts, with a focus on understanding their behavioral patterns, content characteristics, and temporal activity. The analysis examines multiple datasets of Twitter troll accounts to identify distinguishing features that can help detect coordinated inauthentic behavior on social media platforms.

## Dataset

The dataset consists of five pairs of files:
- `*_trimmed.csv`: Contains basic account information and tweet content
- `*_derived.csv`: Contains derived features extracted from the raw data

The data includes tweets from accounts identified as trolls, with features such as:
- **Account metadata**: followers, following, updates, account type, and category
- **Geographic information**: region and language
- **Tweet content**: raw text, hashtags, and mentions
- **Engagement metrics**: retweet status

## Project Structure

```
├── configs/               # Configuration files
├── data/                  # Data directory
│   ├── processed/         # Processed data files
│   └── raw/               # Raw data files (trimmed and derived)
├── notebooks/             # Jupyter notebooks for interactive analysis
│   └── feature_extraction.ipynb
├── plots/                 # Generated visualizations
├── src/                   # Source code
│   ├── eda/               # Exploratory Data Analysis code
│   ├── preprocessing/     # Data preprocessing code
│   └── utils.py           # Utility functions
└── tests/                 # Unit tests
```

## Exploratory Data Analysis Approach

The EDA process is structured to systematically analyze different aspects of the troll accounts:

### 1. Basic Statistical Analysis
- Dataset shape and dimensions
- Missing value identification
- Data type analysis
- Descriptive statistics of numerical features

### 2. Categorical Feature Analysis
- Distribution of accounts by region
- Language distribution
- Account type and category analysis
- Visualization of key categorical distributions

### 3. Numerical Feature Analysis
- Analysis of follower/following counts
- Account activity metrics (updates)
- Followers-to-following ratio analysis
- Distribution and outlier analysis through histograms and boxplots

### 4. Temporal Pattern Analysis
- Distribution of tweets by hour of day
- Distribution of tweets by day of week
- Temporal trends in posting behavior

### 5. Account Behavior Analysis
- Retweet behavior by account category
- Follower/following patterns across different account categories
- Engagement pattern analysis

### 6. NLP Feature Analysis
- Analysis of text-based features:
  - Hashtag usage
  - Mention frequency
  - Word count and text length
  - Special character usage
  - All-caps text frequency
  - Correlation between NLP features

### 7. Content Analysis
- Word cloud visualization of tweet content
- Top hashtag analysis
- Content pattern identification
- Hashtag co-occurrence networks

### 8. Sentiment Analysis
- Sentiment distribution across tweets
- Sentiment analysis by account category
- Sentiment analysis by region
- Outlier analysis in sentiment scores

## Key Findings

The analysis reveals several distinguishing characteristics of troll accounts:

1. **Posting Patterns**: Distinct temporal patterns in posting behavior, with activity spikes during specific hours and days
2. **Account Characteristics**: Unusual follower-to-following ratios compared to typical accounts
3. **Content Features**: Distinctive patterns in hashtag usage, mention frequency, and text characteristics
4. **Sentiment Patterns**: Sentiment distribution that differs from organic content, with higher polarization
5. **Regional Variations**: Different behavioral patterns across different regions/languages

## Visualization Outputs

All visualizations are saved to the `plots/` directory and include:
- Distribution plots of categorical features
- Histograms and boxplots of numerical features
- Temporal analysis plots
- Word clouds of content and hashtags
- Sentiment distribution plots
- Correlation matrices of NLP features

## Usage

To run the full exploratory data analysis:

```python
from src.eda.eda import run_eda

run_eda()
```

This will generate all the analysis plots and save them to the `plots/` directory.

## Technologies Used

- **Python**: Primary programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib & Seaborn**: Data visualization
- **NLTK**: Natural language processing and sentiment analysis
- **WordCloud**: Text visualization