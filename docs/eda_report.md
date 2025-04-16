
---

**Report: Exploratory Data Analysis of Coordinated Inauthentic Behavior on Twitter**

**Abstract**

Online platforms, particularly X/Twitter, have become significant arenas for political discourse, but are susceptible to manipulation by coordinated inauthentic actors, including state-sponsored troll farms like the Russian Internet Research Agency (IRA). These efforts aim not just to influence specific outcomes but to erode trust in information, amplify societal divisions, and promote a "post-truth" environment by injecting chaos and contradictory narratives. Compounding this, recent changes to platform governance, such as paid verification and reduced safety teams, have potentially exacerbated the problem. This report details an extensive Exploratory Data Analysis (EDA) performed on a dataset identified as containing Twitter troll activity (~500k tweets analyzed in segments). The analysis employed statistical methods, Natural Language Processing (NLP), and network analysis to characterize account behaviors, content patterns, temporal activity, and network structures. Key findings reveal a dataset dominated by US-centric, English-language activity peaking during US afternoon hours. Significant behavioral anomalies, including extreme outlier values in engagement metrics (followers, following, updates) and content features (mentions, emojis), strongly suggest non-organic activity. Network analysis identified distinct clusters centered around polarizing US political figures and movements (e.g., #MAGA, @realDonaldTrump, #BlackLivesMatter), alongside persistent non-political entities hinting at diverse automated activities. Comparative analysis of dataset segments highlighted differing dominant troll categories ('RightTroll' vs. 'LeftTroll') with distinct behavioral signatures, particularly in retweet strategies and follower/following ratios. These findings quantitatively substantiate characteristics of coordinated manipulation campaigns, providing empirical evidence aligned with documented troll tactics and motivations. The analysis underscores the scale and multifaceted nature of the challenge and identifies avenues for future research, including deeper narrative analysis and temporal dynamics.

**1. Introduction**

**1.1. Background: The Problem of Online Political Manipulation**
The digital public sphere, particularly social media platforms like X/Twitter, plays a crucial role in modern political engagement. However, this space is increasingly contaminated by inauthentic activity orchestrated by malicious actors. A significant portion of online political discourse involves interactions not with genuine users, but with automated bots and coordinated human operators ("trolls"), often working from organized "troll farms." Notable among these is the Russian Internet Research Agency (IRA), whose tactics have been extensively documented (Project Motivation).

The strategy employed, often associated with figures like Vladislav Surkov under Vladimir Putin, represents a shift from traditional propaganda (hiding truth) to an attack on the concept of truth itself. By disseminating contradictory narratives, promoting conspiracy theories, and funding opposing groups simultaneously, the goal is to generate chaos, confusion, and polarization – fostering a "post-truth" environment where objective reality seems unknowable (Project Motivation).

**1.2. IRA Tactics and Operational Sophistication**
The IRA employed sophisticated methods, including:
*   Paid employees operating networks of fake accounts.
*   Methodical persona-building: establishing fake accounts with non-political content over time, joining local groups, and befriending real users before disseminating propaganda (Project Motivation - Point 1).
*   Infiltrating online communities and targeting divisive issues across the political spectrum (e.g., BLM, white supremacist movements, Sanders/Trump campaigns) to maximize discord (Project Motivation - Point 4).
*   Utilizing repetitive negative framing (e.g., "Crooked Hillary").
*   Leveraging less moderated platforms (e.g., Telegram) for content dissemination.
*   Creating fabricated content, such as fake videos (Project Motivation - Point 3).
Knowledge of these tactics is partly derived from leaked internal IRA documents, providing concrete evidence (Project Motivation - Point 2).

**1.3. Platform Context: X/Twitter Under Elon Musk**
The challenge of identifying and mitigating such activity has been significantly complicated by recent changes at X/Twitter under Elon Musk's ownership. Key issues include:
*   Paid verification ($8 check), which inadvertently legitimized fake/troll accounts.
*   Dismissal of significant portions of safety and integrity teams.
*   API changes hindering independent research into platform manipulation.
*   Obscuring metrics like 'likes', making bot activity harder to detect.
*   Studies suggesting algorithmic manipulation favoring specific political viewpoints near elections, raising concerns about potential external coordination (Project Motivation).

**1.4. Scale and Definition**
The scale of fake and bot activity on X/Twitter is reported to be massive, potentially constituting a third or more of engagement during specific political events and increasing significantly post-Musk ownership (Project Motivation). For this analysis, "bot" encompasses a broad definition including AI-generated content, human trolls operating fake accounts, and any coordinated activity designed to deceive and manipulate public discourse (Project Motivation).

**1.5. Project Goal and Dataset**
The ultimate goal of these manipulation campaigns extends beyond influencing specific elections; it seeks to erode trust in information systems, exhaust the public, deepen polarization, and undermine democratic processes. This research aims to contribute to understanding this phenomenon through a detailed Exploratory Data Analysis (EDA) of a publicly available dataset known to contain tweets associated with troll/inauthentic accounts. The goal is to quantitatively characterize the behaviors, content, and network structures within this dataset, seeking empirical evidence that aligns with or diverges from the documented characteristics and motivations of coordinated online manipulation campaigns.

**2. Methodology**

**2.1. Dataset Description**
The analysis was performed on a dataset comprising approximately 500,000 tweets identified as originating from troll or inauthentic accounts. Due to processing constraints or analytical strategy, the EDA was conducted on two large, roughly equal segments (Segment 1: ~244k tweets, Segment 2: ~251k tweets).

*   **Raw Features:** The initial dataset included tweet content, region, language, publication date, user follower/following counts, user update counts, account type, retweet status, and account category (e.g., 'RightTroll', 'LeftTroll', 'NewsFeed', 'HashtagGamer') (`2_schema.md`).
*   **Derived Features:** Numerous features were engineered to facilitate deeper analysis (`2_schema.md`), including:
    *   **Engagement Ratios:** `followers_to_following_ratio`.
    *   **Temporal Features:** `hour_of_day`, `day_of_week`, `day_of_month`.
    *   **NLP/Content Features:** Extracted `hashtags`, `mentions`, counts (`count_hashtags`, `count_mentions`, `count_emojis`, `count_special_characters`, `word_count`, `count_links`, `text_length`), format flags (`all_words_caps`, `starts_with_hashtag`, `starts_with_mention`, `has_quote`).
    *   **Sentiment Scores:** Derived using VADER.
    *   **Cleaned Text:** Preprocessed text for NLP tasks.

**2.2. Data Preprocessing**
*   **Column Selection:** Initial data was trimmed to relevant columns (`2_schema.md`).
*   **Feature Engineering:** As described above.
*   **Text Cleaning:** A `clean_text` function was applied (using `eda_helpers.py`) involving lowercasing, removal of punctuation, stopwords, URLs, and excessive whitespace (`3_1_eda.md`).
*   **Handling Missing Values:** Missing values were identified and handled appropriately (e.g., ratio calculation avoided division by zero; high expected missingness in hashtags/mentions noted) (`2_1_gemini_insights_eda_1.md`).

**2.3. Exploratory Data Analysis (EDA) Pipeline**
A comprehensive EDA pipeline was implemented (`3_1_eda.md`, `3_2_eda_charts.md`) covering multiple analysis dimensions:

*   **Basic Statistical Analysis (`eda_basic.py`):** Descriptive statistics, data type checks, missing value analysis. Output: Statistical summaries.
*   **Categorical Feature Analysis (`eda_basic.py`):** Analysis of distributions for `region`, `language`, `account_type`, `account_category`. Visualization: Bar charts.
*   **Numerical Feature Analysis (`eda_basic.py`):** Analysis of distributions for engagement metrics and content counts. Visualization: Histograms with KDE, Boxplots. Outlier detection using IQR.
*   **Temporal Analysis (`eda_basic.py`):** Analysis of tweet activity patterns over time (hour of day, day of week). Visualization: Line plots, bar charts.
*   **Account Behavior Analysis (`eda_basic.py`):** Examination of retweet rates and follower/following ratios across different account categories. Visualization: Bar charts, statistical summaries per category.
*   **NLP Analysis (`eda_nlp.py`):**
    *   Correlation Analysis: Relationships between derived NLP features. Visualization: Heatmaps.
    *   Content Analysis: Examination of common words, hashtags, mentions. Visualization: Word clouds, frequency lists.
    *   Sentiment Analysis: Using VADER to assess tweet polarity (positive, neutral, negative). Analysis of overall sentiment and sentiment by category/region. Visualization: Histograms, bar charts.
*   **Network Analysis (`eda_network.py`):** Construction and analysis of hashtag co-occurrence and user mention networks. Calculation of network density and identification of key nodes. Output: Network data saved in JSON format.
*   **LLM-Interpretable Output Generation (`eda_llm.py`):** Translation of EDA findings into structured JSON formats (`llm_eda_context.json`, `llm_eda_context_insights.json`) suitable for processing by Large Language Models (LLMs) to enable automated insight generation and summarization.

**2.4. Comparative Analysis**
Recognizing potential heterogeneity, the EDA was performed separately on two dataset segments. The results were then systematically compared (`2_2_gemini_insights_eda_2.md`, `2_3_gemini_differences.md`) to identify consistent patterns and significant differences, particularly regarding the influence of dominant account categories in each segment.

**3. Results and Findings**

**3.1. Overall Dataset Profile**
Across both analyzed segments, several core characteristics were consistent:
*   **Geographic & Language Focus:** Predominantly US-based (~65-67%) and English-language (~78%) activity, aligning the dataset with the context of targeting US political discourse (`2_1`, `2_2`). A large "Unknown" region category (~24%) was also present.
*   **Temporal Peaks:** Tweet activity consistently peaked during US afternoon hours (14:00-16:00) and mid-week (Monday/Wednesday/Thursday), suggesting coordination or alignment with specific working hours or news cycles rather than typical user behavior spread (`2_1`, `2_2`).
*   **Sentiment Profile:** Overall sentiment was dominated by neutral tweets (~48%), with negative sentiment (28%) slightly outweighing positive sentiment (24%). This pattern held across both segments (`2_1`, `2_2`).

**3.2. Comparative Analysis: Account Category Dominance**
The most significant difference between the two analyzed segments lay in the dominant account category (`2_2`, `2_3`):
*   **Segment 1:** Dominated by `RightTroll` accounts (47%).
*   **Segment 2:** Dominated by `LeftTroll` accounts (34%), with `RightTroll` being the second largest (19%).
This fundamental difference indicates the dataset captures substantial activity attributed to *both* sides of the political spectrum, but potentially clustered or segregated within the data. Findings from each segment are heavily influenced by the behavior of its dominant troll category.

**3.3. Behavioral Anomalies and Outliers**
Both dataset segments exhibited significant outlier populations across numerous features, strongly indicating non-organic or atypical behavior (`2_1`, `2_2`, `2_4`):
*   **Engagement Metrics:** High percentages of outliers were found for `followers` (higher in Segment 2), `following` (higher in Segment 1), `updates` (higher in Segment 1), and `followers_to_following_ratio` (higher in Segment 2). This indicates the presence of accounts with extreme activity levels and follower/following dynamics compared to the median user. The high *mean* follower counts, especially in Segment 2, were heavily skewed by these outliers (`2_4`).
*   **Content Features:** High outlier percentages were also observed for `count_emojis` (higher in Segment 1), `count_mentions` (high in both), and `count_hashtags` (high in both). This suggests strategic "stuffing" of tweets with mentions or hashtags by a subset of accounts, likely for visibility or network activation.
*   **Implication:** The multifaceted nature of these outliers across account size, activity, and content composition points towards highly irregular patterns characteristic of automated or coordinated manipulation efforts (`2_4`).

**3.4. Network Analysis: Connectivity and Focus**
Network analysis revealed insights into the communication structure (`2_1`, `2_2`, `2_3`):
*   **Structure:** Both hashtag and mention networks were relatively sparse, suggesting focused conversations rather than dense interconnections among all top entities. Segment 2's hashtag network was slightly denser, while its mention network was sparser than Segment 1's.
*   **Key Nodes (Reflecting Dominant Category):**
    *   **Segment 1 (RightTroll Dom):** Top hashtags included `#MAGA`, `#PJNET`, `#tcot`. Top mention was `@realDonaldTrump`.
    *   **Segment 2 (LeftTroll Dom):** Top hashtag was `#BlackLivesMatter`. Top mention was `@midnight` (likely the comedy show's hashtag game), followed by `@realDonaldTrump`. Other mentions included left-leaning or racial justice figures (`@deray`, `@ShaunKing`).
*   **Persistent Non-Political/Ambiguous Entities:** Notably, entities like `@midnight`, `@YouTube`, `@rus_improvisation`, and ambiguous hashtag pairs (e.g., `#amb`, `#ara` in P1; `#cadens`/`#canden` in P2) appeared prominently in *both* segments (`2_1`, `2_2`, `2_4`). This suggests underlying layers of activity (e.g., hashtag gaming, cross-ideological botnets, potentially Russian non-political content) persisting regardless of the dominant political troll type.

**3.5. NLP and Content Insights**
Analysis of tweet content provided further details (`2_1`, `2_2`, `2_4`):
*   **Top Words:** Dominated by English stop words, `rt` (indicating high retweet volume), and `trump`. The presence of Russian words (`в`) confirmed the multilingual nature.
*   **Empty Cleaned Text:** A significant portion (~16.5%) of tweets resulted in empty `cleaned_text` strings (`2_4`). This could indicate tweets consisting solely of links/media, heavy reliance on retweets where original content wasn't captured/cleaned properly, or specific low-content amplification strategies.
*   **Sentiment by Category:** Sentiment varied by category, with `RightTroll` consistently showing more negative average sentiment than `LeftTroll` across both segments. `NewsFeed` was also typically negative, while `HashtagGamer` was slightly positive (`2_1`, `2_2`).
*   **Average Content Differences:** Subtle differences were observed: Segment 2 (LeftTroll dominant) showed slightly higher average `count_mentions` but lower average `count_hashtags`, `count_emojis`, `word_count`, and `text_length` per tweet compared to Segment 1 (RightTroll dominant) (`2_4`).
*   **Most Frequent Specific Content:** The single most frequent raw tweet content across both segments was a Russian-language tweet about the Sochi Olympics ("В городе Сочи..."), potentially indicating a specific recurring campaign point (`2_4`).

**3.6. Account Behavior Differences**
Account behavior analysis revealed distinct strategies, particularly when comparing dominant categories (`2_1`, `2_2`, `2_3`):
*   **Retweet Behavior:**
    *   `LeftTroll`: Consistently high retweet rate (73-80%) across both segments, suggesting amplification is a primary tactic.
    *   `RightTroll`: Showed drastically different behavior between segments – moderate retweet rate (51%) in Segment 1, but very low (9%) in Segment 2. This implies different strategies or types of 'RightTroll' accounts captured in each segment (content generation vs. amplification).
    *   `HashtagGamer`: Consistently high retweet rate (66-74%).
    *   `Commercial`: Highly inconsistent behavior between segments.
*   **Influence Ratio (Median Followers/Following):**
    *   `RightTroll`: Consistently low ratio (~0.2-0.3) in both segments, strongly suggesting aggressive mass-following tactics rather than organic influence building.
    *   `LeftTroll`: Ratio consistently near or slightly above parity (~1.1-1.4), suggesting potentially more reciprocal following or slightly higher organic engagement compared to RightTrolls based on this metric.
    *   `Commercial`, `NewsFeed`: Showed inconsistent ratios between segments.

**4. Discussion**

The EDA findings provide substantial quantitative evidence that aligns with the characteristics and motivations of online manipulation campaigns described in the project motivation (`3_insight_inferences.md`).

*   **Confirmation of Landscape:** The dataset's focus on US/English political discourse, including significant engagement around figures like Trump and movements like MAGA and BLM, directly corresponds to the described targets of IRA and similar operations aimed at exploiting societal divisions. The presence of distinct 'RightTroll' and 'LeftTroll' categories supports the tactic of amplifying conflict across the political spectrum.
*   **Evidence of Coordinated/Inauthentic Activity:** The pronounced temporal peaks during specific hours/days strongly suggest coordinated, potentially scheduled activity rather than organic user behavior. The pervasive presence of outliers with extreme engagement and content metrics serves as a classic signature of automation or atypical, dedicated human operator behavior (troll farms). The low follower/following ratios observed, particularly for 'RightTroll' accounts, point directly to non-organic, aggressive following strategies intended to gain visibility or infiltrate networks, consistent with troll farm tactics.
*   **Targeting Political Discourse:** The network analysis clearly shows the centrality of divisive political figures, movements, and media outlets, confirming the focus on manipulating political conversations as highlighted in the motivation. The contrasting focal points between the RightTroll-dominant (#MAGA) and LeftTroll-dominant (#BlackLivesMatter) segments illustrate the tactic of engaging intensely with polarizing issues from multiple angles.
*   **Indications of Specific Strategies:**
    *   *Varied Amplification:* The differing retweet rates (high for LeftTroll, variable for RightTroll) suggest different core strategies or roles within campaigns (e.g., content generation vs. signal boosting).
    *   *Visibility Tactics:* The outlier counts for hashtags and mentions suggest strategic "stuffing" to increase visibility or trigger notifications, a common manipulation tactic.
    *   *Potential Persona Differences:* The contrasting influence ratios might hint at different approaches to persona management between LeftTroll and RightTroll categories in this dataset.
*   **Diverse Activity Layers:** The persistence of non-political network entities like `@midnight` and ambiguous tags across segments dominated by different political trolls highlights the complexity of the dataset. It suggests the presence of potentially unrelated automated activity (spam, game participation) or cross-cutting botnets alongside the politically motivated trolls.
*   **Data Artifacts & Limitations:** The high incidence of empty `cleaned_text` warrants further investigation, potentially indicating heavy reliance on retweets or link-sharing without original commentary, a form of low-effort amplification. The inconsistent behavior of the 'Commercial' category suggests it may be poorly defined or heterogeneous.

In essence, the EDA successfully identified numerous quantitative indicators within the dataset that mirror the known operational patterns and strategic goals of coordinated inauthentic behavior online, particularly those attributed to actors like the IRA.

**5. Conclusion and Future Work**

**5.1. Conclusion**
This Exploratory Data Analysis provided a detailed characterization of a large dataset associated with Twitter troll activity. The analysis confirmed the dataset's strong alignment with the context of US-centric political manipulation, revealing distinct temporal patterns, significant behavioral anomalies (outliers, skewed ratios), and network structures centered on divisive political topics and figures. Key findings include the identification of substantial 'RightTroll' and 'LeftTroll' populations exhibiting different behavioral strategies (notably in retweeting and follower ratios), and the persistence of non-political network entities suggesting diverse forms of automated activity. The prevalence of outliers and non-organic behavioral signatures provides strong empirical support for the presence of coordinated, inauthentic activity consistent with documented troll farm operations. The results highlight the multifaceted nature of online manipulation and provide a quantitative foundation for understanding these campaigns.

**5.2. Future Work**
While this EDA provided valuable structural and behavioral insights, further research is needed to fully understand the nuances of the manipulation campaigns captured in this data. Based on the findings and the initial project motivation, promising directions for future work include:

1.  **Qualitative Narrative Analysis:** Move beyond sentiment and topic frequency to analyze the *specific narratives*, disinformation techniques (e.g., false flags, whataboutism), and argumentative structures used in the tweet content to understand *how* chaos and mistrust are sown.
2.  **Mapping to Documented Tactics:** Attempt to correlate observed patterns with specific, documented IRA tactics, such as analyzing account age versus activity type for evidence of long-term persona building or using NLP to detect repetitive negative framing.
3.  **Temporal Dynamics Analysis:** Investigate how activity patterns, topics, sentiment, and network structures evolve *over time* within the dataset, particularly around key political events.
4.  **Investigating "Unknowns":** Conduct targeted analysis of tweets with "Unknown" region classifications or empty `cleaned_text` to determine if these represent deliberate obfuscation or specific content strategies (e.g., link dropping).
5.  **Deeper Network Interaction Analysis:** Analyze not just co-occurrence but direct interactions (e.g., who retweets/quotes whom) to better map influence flows and community structures between different account categories.
6.  **Comparative Baseline Analysis:** Compare the metrics and behaviors observed in this troll dataset against a baseline dataset of verified non-troll users to rigorously quantify the differences and strengthen the identification of inauthentic signatures.
7.  **Combined Dataset Analysis:** Perform the full suite of EDA and potentially modeling on the *entire combined dataset* to understand the interplay between different troll groups within the complete ecosystem.

**6. References**

[Placeholder for citations used in the thesis, referencing studies on IRA, Twitter platform changes, bot detection, etc.]

**7. Appendices**

[Optional: Could include detailed statistical tables, full lists of top hashtags/mentions per segment, data schema details, example outlier tweets, etc.]

---