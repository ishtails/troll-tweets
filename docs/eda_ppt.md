**Presentation Title:** Analyzing Troll Behavior: Insights from a Large-Scale Twitter Dataset

**Presenter:** Kartikay Tiwari

---

**Slide 1: Title Slide**

*   **Title:** Analyzing Troll Behavior: Insights from a Large-Scale Twitter Dataset
*   **Subtitle:** Uncovering Patterns, Tactics, and Coordination in Online Manipulation
*   **Presenter Name:** Kartikay Tiwari
*   **Date:** 04/16/2025
*   *(Visually: Clean background, maybe a subtle network graphic or abstract representation of digital noise)*

---

**Slide 2: The Problem: The Erosion of Online Truth**

*   **Title:** The Problem: Weaponized Information & Online Manipulation
*   **Content:**
    *   Significant online political discourse isn't organic; involves bots & organized troll farms (e.g., Russian IRA).
    *   **Strategy:** Shift from hiding truth to *attacking truth itself* – creating chaos, confusion, "post-truth" (Surkov/Putin). Funded *opposing* groups to maximize division.
    *   **Tactics:** Fake personas built over time, repetitive negative framing, infiltrating communities, targeting divisive issues (across the spectrum).
    *   **Platform Impact (X/Twitter):** Paid verification ($$), fired safety teams, API changes hindering research, algorithmic manipulation concerns → worsened the problem.
    *   **Scale:** Massive levels of fake/bot activity reported on X.
    *   **Goal:** Erode trust, exhaust the public, increase polarization, make objective reality seem unknowable.
*   **Script:**
    > "Good morning/afternoon. Today, we're diving into a critical issue shaping our online world: the deliberate manipulation of information by coordinated actors like troll farms. These aren't just isolated incidents; they represent a strategy, famously employed by entities like the Russian Internet Research Agency, not just to push one viewpoint, but to attack the very concept of truth, creating chaos and division. They use sophisticated tactics – building fake personas, infiltrating online groups, and relentlessly targeting divisive issues. Recent changes on platforms like X/Twitter have unfortunately amplified these problems, making it harder to distinguish real discourse from manipulation. The scale is staggering, and the ultimate goal is deeply concerning: to erode public trust and make objective reality seem uncertain."
*   *(Visually: Maybe icons representing fake profiles, chaos, platform logos, question marks)*

---

**Slide 3: Project Goal & Dataset**

*   **Title:** Our Objective & The Data Under the Microscope
*   **Content:**
    *   **Goal:** To analyze a large dataset (approx. 500k tweets) of suspected troll activity to quantitatively understand their characteristics, behaviors, and alignment with known manipulation tactics.
    *   **Data Source:** Tweets identified as potentially originating from troll accounts (mention context if known, e.g., related to IRA or specific campaigns).
    *   **Key Raw Info:** Tweet `content`, `region`, `language`, `publish_date`, user `followers`/`following`/`updates`, `account_type`, `retweet` status, `account_category`.
    *   **Analysis Approach:** Dataset was analyzed in two large parts (~244k & ~251k tweets) initially to manage scale and explore potential heterogeneity.
*   **Script:**
    > "Our goal with this project was to move beyond anecdotes and quantitatively analyze a substantial dataset – around half a million tweets – associated with suspected troll activity. We aimed to identify patterns, understand behaviors, and see how well they match the documented tactics. We captured core information like the tweet text, location, user metrics, and importantly, pre-defined account categories like 'RightTroll' or 'LeftTroll'. Due to the size, we initially performed Exploratory Data Analysis (EDA) on two major segments of the data."
*   *(Visually: Database icon, world map highlighting US/Russia, tweet icon)*

---

**Slide 4: Enhancing the Data: Derived Features**

*   **Title:** Going Deeper: Feature Engineering for Richer Insights
*   **Content:**
    *   Raw data was augmented with calculated features:
        *   **Engagement:** `followers_to_following_ratio`
        *   **Temporal:** `hour_of_day`, `day_of_week`, `day_of_month`
        *   **Content Structure:** `hashtags`/`mentions` (extracted lists & counts), `count_emojis`, `count_special_characters`, `word_count`, `count_links`, `text_length`
        *   **Content Style:** `all_words_caps`, `starts_with_hashtag`/`mention`, `has_quote`
        *   **Sentiment:** Calculated using VADER (suitable for social media)
*   **Script:**
    > "To get richer insights, we didn't just look at the raw data. We engineered several new features. These included engagement ratios, detailed temporal breakdowns to find activity patterns, counts of various content elements like hashtags, mentions, and emojis, flags for specific stylistic choices like starting with a hashtag, and importantly, sentiment analysis scores for each tweet."
*   *(Visually: Gear icon, chart icons, hashtag/mention symbols, sentiment faces)*

---

**Slide 5: Analysis Methodology: A Multi-Faceted Approach**

*   **Title:** How We Explored the Data: Comprehensive EDA
*   **Content:**
    *   **Basic Statistics:** Dataset shape, types, missing values.
    *   **Distribution Analysis:** How are categorical (region, language, type) and numerical (followers, counts) features spread? Outlier detection.
    *   **Temporal Analysis:** When are these accounts most active? (Hourly, daily patterns).
    *   **Account Behavior:** Retweet habits, follower/following dynamics across categories.
    *   **NLP Content Analysis:** Word frequencies, common hashtags/mentions, text characteristics.
    *   **Sentiment Analysis:** Overall tone, variations by category/region.
    *   **Network Analysis:** Co-occurrence of hashtags and mentions to map thematic & communication clusters.
    *   **Visualization:** Used Matplotlib, Seaborn, Word Clouds for clarity.
*   **Script:**
    > "Our Exploratory Data Analysis, or EDA, was comprehensive. We started with basic checks, then dived into the distributions of different features, looking for imbalances and outliers. We analyzed activity timing, specific account behaviors like retweeting, and the textual content itself using NLP techniques. Sentiment analysis gave us the emotional tone, and network analysis helped us understand connections between hashtags and mentioned users. We used various visualization tools to make these patterns clear."
*   *(Visually: Icons for bar chart, histogram, clock, user profile, text document, network graph)*

---

**Slide 6: High-Level Profile: Consistent Characteristics**

*   **Title:** Dataset Snapshot: Common Threads
*   **Content:**
    *   **Geographic/Language Focus:** Heavily dominated by **United States (~66%)** and **English (~78%)**. (Significant 'Unknown' region ~24%).
    *   **Temporal Pattern:** Strong, consistent peak activity in **US afternoon hours (14:00-16:00)** and **mid-week (Mon-Thu)**.
    *   **Overall Sentiment:** Predominantly **Neutral (~48%)**, with Negative (~28%) slightly outweighing Positive (~24%).
*   **Script:**
    > "Looking across the entire dataset, some key characteristics emerged consistently. The activity is overwhelmingly US-centric and in English, confirming the focus often discussed in relation to interference campaigns. There's a very distinct and consistent activity peak during US afternoon hours and mid-week, suggesting potentially coordinated or 'working hours' patterns rather than typical organic user behavior spread throughout the day. Overall sentiment tends to be neutral, though with a slight negative lean."
*   *(Visually: US map highlighted, clock showing 2-4 PM, pie chart for sentiment)*

---

**Slide 7: The Core Finding: A Tale of Two Troll Types**

*   **Title:** Key Discovery: Not All Trolls Are the Same
*   **Content:**
    *   Analyzing the two data parts separately revealed a fundamental difference:
        *   **Part 1 (~244k tweets): Dominated by `RightTroll` accounts (47%)**
        *   **Part 2 (~251k tweets): Dominated by `LeftTroll` accounts (34%)**, with `RightTroll` secondary (19%).
    *   **Implication:** The dataset captures significant populations of *both* major political troll categories, but they appear somewhat segregated in these data splits. Insights are heavily influenced by the dominant group in each part.
*   **Script:**
    > "However, the most crucial finding came from comparing the two parts we analyzed. They weren't identical. Part 1 was heavily dominated by accounts categorized as 'RightTroll', while Part 2 was led by 'LeftTroll' accounts. This is a fundamental difference and tells us the dataset isn't monolithic – it contains large, distinct groups, and analyzing only one part would give a skewed picture."
*   *(Visually: Split screen graphic, maybe contrasting colors or symbols for Left/Right)*

---

**Slide 8: Comparative Insights: Network Focus & Key Entities**

*   **Title:** Contrasting Ecosystems: Who & What They Talk About
*   **Content:**
    *   **Network Centers Reflect Dominance:**
        *   **Part 1 (RightTroll Dom.):** Top Hashtag: `#MAGA`; Top Mention: `@realDonaldTrump`. Network dense with political co-mentions.
        *   **Part 2 (LeftTroll Dom.):** Top Hashtag: `#BlackLivesMatter`; Top Mention: `@midnight` (Comedy Central show, likely hashtag games), `@realDonaldTrump` still #2. Mention network sparser.
    *   **Persistent Entities:** Some entities ranked high in *both* parts:
        *   `@midnight`, `@YouTube`, `@rus_improvisation` (Russian improv account?)
        *   Ambiguous/paired hashtags (e.g., `#cadens`/`#canden`) - suggesting bots, games, or cross-cutting campaigns.
*   **Script:**
    > "This difference in dominant category dramatically changed the focus of conversations. In the RightTroll-dominated Part 1, the network revolved around #MAGA and @realDonaldTrump. In the LeftTroll-dominated Part 2, #BlackLivesMatter was the top hashtag, and surprisingly, the @midnight show's handle was the top mention, likely due to hashtag games, though Trump remained highly mentioned. Interestingly, some non-political or ambiguous entities like @YouTube, a Russian improv handle, and strange paired hashtags appeared prominently in *both* segments, hinting at other types of activity layered within."
*   *(Visually: Two contrasting network diagrams (simplified), key hashtag/mention examples)*

---

**Slide 9: Comparative Insights: Behavioral Differences**

*   **Title:** Contrasting Tactics: How They Behave
*   **Content:**
    *   **Retweet Behavior:**
        *   `LeftTroll`: Consistently HIGH retweet rate (~75%) in both parts (Amplification focus).
        *   `RightTroll`: **Drastic difference!** Moderate RT rate (51%) in Part 1 vs. VERY LOW (9%) in Part 2 (Suggests different strategies or types of RightTrolls).
        *   `Commercial` category: Highly inconsistent behavior (spam/misclassification?).
    *   **Influence Ratio (Median Followers/Following):**
        *   `RightTroll`: Consistently LOW (<0.3) - Suggests mass-following tactics over organic influence.
        *   `LeftTroll`: Moderate (~1.1-1.4) - Closer to parity, maybe more reciprocal following.
*   **Script:**
    > "Their behaviors also differed significantly. LeftTrolls consistently used retweets heavily, focusing on amplification. RightTrolls, however, showed a striking difference between the two parts – moderate retweeting in Part 1, but very little in Part 2. This could indicate different strategies or different types of RightTroll accounts captured. Looking at the follower-to-following ratio, RightTrolls consistently had far more accounts they followed than followers, hinting at mass-following tactics. LeftTrolls were closer to parity."
*   *(Visually: Bar charts comparing RT rates, simplified 'influence' scale graphic)*

---

**Slide 10: Key Insight: Pervasive Anomalies & Outliers**

*   **Title:** Red Flags: Evidence of Non-Organic Activity
*   **Content:**
    *   **Significant Outliers:** Found across *many* features in both dataset parts:
        *   `followers`, `following`, `updates` (e.g., max updates > 70k!)
        *   `count_emojis` (up to 19% outliers in Part 1)
        *   `count_mentions` (up to 15% outliers)
        *   `count_hashtags`
    *   **Interpretation:** A subset of accounts exhibits *extreme* behavior vastly different from the norm across multiple dimensions. This strongly suggests automation, hyper-activity of troll farm workers, or highly atypical user engagement.
*   **Script:**
    > "Across both parts of the dataset, we saw strong evidence of anomalous behavior. A significant percentage of accounts showed extreme outlier values for metrics like follower counts, the sheer number of tweets posted – sometimes tens of thousands – and the counts of emojis, mentions, or hashtags used in single tweets. This isn't typical user behavior; it's a strong indicator of automation or highly coordinated, inorganic activity by a subset of these accounts."
*   *(Visually: Highlighted outlier points on box plots or histograms, warning sign icon)*

---

**Slide 11: Key Insight: Content Nuances & Potential Artifacts**

*   **Title:** Subtle Clues: Content Patterns & Data Quirks
*   **Content:**
    *   **Empty Cleaned Text:** ~16.5% of tweets had no text left after cleaning (removing URLs, mentions, etc.). Implies potential focus on pure Retweets or link-dropping with minimal commentary.
    *   **Subtle Style Differences:** Averages suggest Part 2 (LeftTroll dom.) used slightly more mentions, but fewer hashtags, emojis, and links than Part 1 (RightTroll dom.).
    *   **Confirmed Russian Content:** Specific Russian-language tweets (e.g., about Sochi Olympics) appear repeatedly, confirming multi-lingual campaigns.
    *   **Missing Starts-With-Mention:** Zero tweets started with a mention - highly unusual for Twitter (preprocessing artifact or deliberate broadcast strategy?). *(Correction: Check if this was definitively zero or just low % in the files)*
*   **Script:**
    > "Looking closer at the content revealed more nuances. A surprisingly high percentage of tweets were empty after cleaning, suggesting strategies focused purely on amplification or sharing links. We also saw subtle average differences in style – the LeftTroll-dominant part used slightly more mentions, while the RightTroll-dominant part used more emojis and hashtags on average. We also confirmed the presence of specific, repeated Russian-language content. One potential data quirk or strategy indicator needs verification: an apparent absence or very low number of tweets starting with a mention, which deviates significantly from typical reply behavior on Twitter."
*   *(Visually: Text document icon with "?" , Russian flag icon, link icon)*

---

**Slide 12: Connecting Findings to Motivation: Evidence Alignment**

*   **Title:** Does the Data Support the Premise? Yes.
*   **Content:**
    *   **Confirms Landscape:** Dataset profile (US/English focus, Political categories) matches the motivated context of interference targeting US discourse.
    *   **Evidence of Coordination:** Temporal peaks (working hours?), significant outliers across multiple metrics point to organized, non-organic activity.
    *   **Targets Divisive Issues:** Network analysis confirms focus on key political figures (#MAGA, Trump) and sensitive topics (#BlackLivesMatter), aligning with the goal of sowing discord.
    *   **Suggests Known Tactics:** Low influence ratios (mass-following), high RT rates (amplification), potential content stuffing (emoji/hashtag outliers), varied strategies between groups.
*   **Script:**
    > "So, how does this data connect back to our initial understanding of troll operations? Very strongly. Our findings provide quantitative evidence supporting the descriptions. The dataset's focus aligns geographically and politically. The activity patterns – time peaks, extreme outliers – scream coordination, not organic behavior. The content clearly targets the divisive political figures and topics mentioned as key leverage points. And the behavioral metrics suggest specific tactics like mass-following and amplification, employed differently by various groups within the dataset."
*   *(Visually: Checkmark icons, connecting lines from findings back to motivation points)*

---

**Slide 13: Conclusion: Key Takeaways**

*   **Title:** Conclusion: Synthesizing the Findings
*   **Content:**
    *   This dataset provides a valuable window into large-scale, suspected troll activity, primarily focused on US political discourse.
    *   Activity is **NOT monolithic:** Distinct LeftTroll and RightTroll segments exist with differing network focus and behavioral tactics (esp. RightTroll RT rates).
    *   Strong quantitative evidence of **coordination** (temporal peaks) and **anomalous/non-organic behavior** (extreme outliers, low influence ratios).
    *   Network analysis reveals key **political hubs** (#MAGA, BLM, Trump) but also **persistent non-political entities** (@midnight, @YouTube, ambiguous tags) warranting further study.
    *   Content analysis reveals potential strategies (link dropping/RTs) and confirms multi-lingual aspects.
*   **Script:**
    > "In conclusion, this analysis confirms that the dataset captures significant, complex troll activity targeting US politics. Crucially, this activity isn't uniform; we identified distinct Left and Right troll segments with different behaviors and network focuses. There's strong evidence pointing towards coordination and clearly non-organic activity patterns. While political hubs dominate the networks, the persistence of certain non-political entities suggests other dynamics are also at play. The content itself gives clues about amplification strategies and the multi-lingual nature of these campaigns."

---

**Slide 14: Future Work: Where Do We Go From Here?**

*   **Title:** Next Steps: Deepening the Investigation
*   **Content:**
    *   **Combined Dataset Analysis:** Re-run key analyses on the entire dataset for a holistic view.
    *   **Direct Troll Comparison:** In-depth statistical comparison of `RightTroll` vs. `LeftTroll` behaviors across the full dataset.
    *   **Qualitative Narrative Analysis:** Move beyond counts – what *specific messages, themes, and disinformation techniques* are being used? (Topic Modeling, Manual Review).
    *   **Investigate Anomalies:**
        *   Deep dive into the nature of outlier accounts.
        *   Understand the persistent ambiguous hashtags/mentions (@midnight, `#cadens`, etc.).
        *   Figure out the cause of empty `cleaned_text`.
    *   **Temporal Dynamics:** Analyze how activity, topics, and sentiment evolved *over time* within the dataset.
    *   **Baseline Comparison:** Compare these troll account metrics against a baseline dataset of 'normal' Twitter users to quantify the differences rigorously.
*   **Script:**
    > "This EDA provides a strong foundation, but there's much more to uncover. Key next steps include analyzing the full dataset together, performing direct statistical comparisons between Left and Right Trolls, and crucially, moving into qualitative analysis to understand the actual narratives being spread. We also need to investigate the persistent anomalies like the ambiguous network entities and the empty text issue. Analyzing how these activities changed over time and comparing them rigorously to a baseline of normal users would provide even deeper insights into the nature and impact of this manipulation."
*   *(Visually: Magnifying glass icon, timeline graphic, question mark icon)*

---

**Slide 15: Thank You & Q&A**

*   **Title:** Thank You
*   **Content:**
    *   Questions?
    *   [Your Contact Information - Optional]
*   **Script:**
    > "Thank you for your time and attention. I'm happy to answer any questions you may have."

---