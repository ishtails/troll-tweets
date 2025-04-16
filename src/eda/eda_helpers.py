"""Helper functions for EDA"""

import re
import string
from nltk.corpus import stopwords

def progress_bar(current, total, bar_length=70):
    """Print a progress bar"""
    percent = float(current) * 100 / total
    arrow = "=" * int(percent / 100 * bar_length)
    spaces = " " * (bar_length - len(arrow))
    print(f"Progress: [{arrow}{spaces}] {percent:.2f}%", end="\r")

def clean_text(text):
    """Clean text"""
    if text is None:
        text = ""  # Handle None values
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\S+", "", text)
    text = re.sub(r"#\S+", "", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\d+", "", text)
    stop_words = set(stopwords.words("english"))
    text = " ".join(
        word
        for word in text.split()
        if word.lower() not in stop_words and word not in string.punctuation
    )
    return text.lower()
