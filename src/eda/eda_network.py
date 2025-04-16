"""
Network analysis functions for EDA.
This module provides functionality to analyze network structures in the dataset,
such as hashtag co-occurrence networks and mention networks.
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
from typing import Dict, List, Any, Tuple


def extract_hashtag_network(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Extract hashtag co-occurrence network.
    
    Args:
        df: DataFrame with a 'hashtags' column
        
    Returns:
        Dictionary with hashtag network data
    """
    if 'hashtags' not in df.columns:
        return {"nodes": [], "edges": [], "has_network": False}
    
    # Filter rows with hashtags
    hashtag_rows = df['hashtags'].dropna()
    
    if hashtag_rows.empty:
        return {"nodes": [], "edges": [], "has_network": False}
    
    # Process hashtags
    all_hashtags = []
    co_occurrence = defaultdict(int)
    
    for tags_str in hashtag_rows:
        if not tags_str:
            continue
            
        tags = [tag.strip() for tag in tags_str.split(',')]
        if len(tags) > 1:  # Only process rows with multiple hashtags
            # Add all tags to the list of all hashtags
            all_hashtags.extend(tags)
            
            # Count co-occurrences
            for i, tag1 in enumerate(tags):
                for tag2 in tags[i+1:]:
                    if tag1 and tag2:  # Ensure not empty
                        # Create a sorted tuple of tags to avoid duplicates
                        edge = tuple(sorted([tag1, tag2]))
                        co_occurrence[edge] += 1
    
    # Get top hashtags
    top_hashtags = [tag for tag, _ in Counter(all_hashtags).most_common(50)]
    
    # Create nodes and edges for network visualization
    nodes = [{"id": tag, "weight": count} 
             for tag, count in Counter(all_hashtags).most_common(50)]
    
    edges = []
    for (source, target), weight in co_occurrence.items():
        if source in top_hashtags and target in top_hashtags:
            edges.append({
                "source": source,
                "target": target,
                "weight": weight
            })
    
    return {
        "nodes": nodes,
        "edges": edges,
        "has_network": len(edges) > 0
    }


def extract_mention_network(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Extract mention network.
    
    Args:
        df: DataFrame with a 'mentions' column
        
    Returns:
        Dictionary with mention network data
    """
    if 'mentions' not in df.columns:
        return {"nodes": [], "edges": [], "has_network": False}
    
    # Filter rows with mentions
    mention_rows = df['mentions'].dropna()
    
    if mention_rows.empty:
        return {"nodes": [], "edges": [], "has_network": False}
    
    # Process mentions
    all_mentions = []
    
    for mentions_str in mention_rows:
        if not mentions_str:
            continue
            
        mentions = [mention.strip() for mention in mentions_str.split(',')]
        all_mentions.extend(mentions)
    
    # Get mention counts
    mention_counts = Counter(all_mentions)
    
    # Create connections between mentions that appear in the same tweet
    connections = defaultdict(int)
    for mentions_str in mention_rows:
        if not mentions_str:
            continue
            
        mentions = [mention.strip() for mention in mentions_str.split(',')]
        if len(mentions) > 1:  # Only process rows with multiple mentions
            for i, mention1 in enumerate(mentions):
                for mention2 in mentions[i+1:]:
                    if mention1 and mention2:  # Ensure not empty
                        # Create a sorted tuple of mentions to avoid duplicates
                        edge = tuple(sorted([mention1, mention2]))
                        connections[edge] += 1
    
    # Select top mentions
    top_mentions = [mention for mention, _ in mention_counts.most_common(50)]
    
    # Create nodes and edges for network visualization
    nodes = [{"id": mention, "weight": count} 
             for mention, count in mention_counts.most_common(50)]
    
    edges = []
    for (source, target), weight in connections.items():
        if source in top_mentions and target in top_mentions:
            edges.append({
                "source": source,
                "target": target,
                "weight": weight
            })
    
    return {
        "nodes": nodes,
        "edges": edges,
        "has_network": len(edges) > 0
    }


def analyze_networks(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze network structures in the dataset.
    
    Args:
        df: Dataset DataFrame
        
    Returns:
        Dictionary with network analysis results
    """
    result = {}
    
    # Extract hashtag network
    hashtag_network = extract_hashtag_network(df)
    result["hashtag_network"] = hashtag_network
    
    # Extract mention network
    mention_network = extract_mention_network(df)
    result["mention_network"] = mention_network
    
    # Compute summary statistics
    result["summary"] = {
        "has_networks": hashtag_network["has_network"] or mention_network["has_network"],
        "hashtag_network_size": len(hashtag_network["nodes"]),
        "hashtag_network_density": len(hashtag_network["edges"]) / 
                                 (len(hashtag_network["nodes"]) * (len(hashtag_network["nodes"]) - 1) / 2) 
                                 if len(hashtag_network["nodes"]) > 1 else 0,
        "mention_network_size": len(mention_network["nodes"]),
        "mention_network_density": len(mention_network["edges"]) / 
                                (len(mention_network["nodes"]) * (len(mention_network["nodes"]) - 1) / 2)
                                if len(mention_network["nodes"]) > 1 else 0
    }
    
    return result


def save_network_data(df: pd.DataFrame, output_path: str = "network_data.json") -> None:
    """
    Save network data to a JSON file.
    
    Args:
        df: Dataset DataFrame
        output_path: Path to save the JSON output
    """
    network_data = analyze_networks(df)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(network_data, f, indent=2, ensure_ascii=False)
    
    print(f"Network data saved to {output_path}")
