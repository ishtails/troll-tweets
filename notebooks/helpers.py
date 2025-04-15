"""
This file contains helper functions for the EDA notebook.
"""
import re


def extract_hashtags(text):
    """
    Extracts hashtags from a text.
    """
    return {
        "hashtags": re.findall(r"#\w+", text),
        "count": len(re.findall(r"#\w+", text)),
    }


def extract_mentions(text):
    """
    Extracts mentions from a text.
    """
    return {
        "mentions": re.findall(r"@\w+", text),
        "count": len(re.findall(r"@\w+", text)),
    }


def count_emojis(text):
    """
    Counts emojis in a text.
    """
    return len(re.findall(r"[^\x00-\x7F]+", text))


def count_special_characters(text):
    """
    Counts special characters in a text.
    """
    return len(re.findall(r"[^a-zA-Z0-9\s]", text))


def all_caps(text):
    """
    Checks if all words in a text are in uppercase.
    """
    return all(word.isupper() for word in text.split())


def count_links(text):
    """
    Counts links in a text.
    """
    return len(re.findall(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", text))


def has_quote(text):
    """
    Checks if a text contains a quote.
    """
    return 1 if re.search(r'["\'].*["\']', text) else 0
