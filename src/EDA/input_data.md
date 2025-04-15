### 1. Raw Data

```python
trimmed_cols = [
    "content",
    "region",
    "language",
    "publish_date",
    "following",
    "followers",
    "updates",
    "account_type",
    "retweet",
    "account_category",
]

df = raw_data[trimmed_cols]
df.to_csv('1_trimmed.csv', index=False)
```

### 2. Derived Features

Several new features are derived from the existing data:

```python
derived = pd.DataFrame()
derived["followers_to_following_ratio"] = df["followers"].div(df["following"].replace(0, np.nan))
derived['date'] = pd.to_datetime(df['publish_date'], errors='coerce')
derived['hour_of_day'] = derived['date'].dt.hour
derived['day_of_week'] = derived['date'].dt.dayofweek
derived['day_of_month'] = derived['date'].dt.day
derived['hashtags'] = df['content'].apply(extract_hashtags).apply(lambda x: ', '.join(x['hashtags']))
derived['mentions'] = df['content'].apply(extract_mentions).apply(lambda x: ', '.join(x['mentions']))
derived['count_hashtags'] = df['content'].apply(extract_hashtags).apply(lambda x: x['count'])
derived['count_mentions'] = df['content'].apply(extract_mentions).apply(lambda x: x['count'])
derived['count_emojis'] = df['content'].apply(count_emojis)
derived['count_special_characters'] = df['content'].apply(count_special_characters)
derived['word_count'] = df['content'].apply(lambda x: len(str(x).split()))
derived['count_links'] = df['content'].apply(count_links)
derived['text_length'] = df['content'].apply(len)
derived['all_words_caps'] = df['content'].apply(all_caps).apply(lambda x: 1 if x else 0)
derived['starts_with_hashtag'] = df['content'].apply(lambda x: 1 if x.startswith('#') else 0)
derived['starts_with_mention'] = df['content'].apply(lambda x: 1 if x.startswith('@') else 0)
derived['has_quote'] = df['content'].apply(has_quote)
```

## Outputs

- `1_trimmed.csv`: path: `data/processed/1_trimmed.csv`
- `1_derived.csv`: path: `data/processed/1_derived.csv`

## 1_trimmed.csv

The trimmed dataset contains the following columns:

| Column Name      | Description                                                      |
| ---------------- | ---------------------------------------------------------------- |
| content          | The text content of the tweet.                                   |
| region           | The region associated with the tweet.                            |
| language         | The language in which the tweet is written.                      |
| publish_date     | The date and time when the tweet was published.                  |
| following        | The number of accounts the user is following.                    |
| followers        | The number of followers the user has.                            |
| updates          | The number of updates (tweets) the user has posted.              |
| account_type     | The type of account (e.g., Right, Left, etc.).                   |
| retweet          | Indicates whether the tweet is a retweet (1=True, 0=False).      |
| account_category | The category of the account (e.g., RightTroll, LeftTroll, etc.). |

## 1_derived.csv

The derived dataset contains the following columns:

| Column Name                  | Description                                                        |
| ---------------------------- | ------------------------------------------------------------------ |
| followers_to_following_ratio | Ratio of followers to following count.                             |
| date                         | The publish date of the tweet.                                     |
| hour_of_day                  | The hour of the day the tweet was published.                       |
| day_of_week                  | The day of the week the tweet was published (0=Monday, 6=Sunday).  |
| day_of_month                 | The day of the month the tweet was published.                      |
| hashtags                     | List of hashtags used in the tweet.                                |
| mentions                     | List of mentions in the tweet.                                     |
| count_hashtags               | Number of hashtags in the tweet.                                   |
| count_mentions               | Number of mentions in the tweet.                                   |
| count_emojis                 | Number of emojis in the tweet.                                     |
| count_special_characters     | Number of special characters in the tweet.                         |
| word_count                   | Number of words in the tweet.                                      |
| count_links                  | Number of links in the tweet.                                      |
| text_length                  | Length of the tweet text.                                          |
| all_words_caps               | Whether all words in the tweet are in uppercase (1=True, 0=False). |
| starts_with_hashtag          | Whether the tweet starts with a hashtag (1=True, 0=False).         |
| starts_with_mention          | Whether the tweet starts with a mention (1=True, 0=False).         |
| has_quote                    | Whether the tweet contains a quote (1=True, 0=False).              |
