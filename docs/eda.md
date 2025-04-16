# Exploratory Data Analysis (EDA) Framework

This directory contains a comprehensive framework for performing Exploratory Data Analysis on the Twitter Troll dataset, with special emphasis on generating LLM-interpretable outputs that can be fed to large language models.

## Overview

The EDA framework is designed to systematically analyze different aspects of the Twitter Troll dataset, including basic statistics, categorical features, numerical features, temporal patterns, NLP features, sentiment analysis, and network analysis. The framework not only generates human-readable visualizations but also creates machine-readable structured outputs specifically optimized for LLMs.

## Components

### Core Modules

- **main.py**: Central orchestration script that executes the full EDA pipeline
- **eda_basic.py**: Basic statistical analysis and visualization functions
- **eda_nlp.py**: NLP-specific analyses including text features and sentiment analysis
- **eda_helpers.py**: Utility functions for cleaning text and displaying progress
- **eda_network.py**: Network analysis for hashtag co-occurrence and mention networks
- **eda_llm.py**: LLM-interpretable EDA output generation

### Functionality

#### Basic EDA (eda_basic.py)
- Dataset shape and type analysis
- Missing value identification
- Categorical feature distribution analysis
- Numerical feature distribution and outlier detection
- Temporal pattern analysis
- Account behavior analysis

#### NLP Analysis (eda_nlp.py)
- Text feature analysis (hashtags, mentions, word count, etc.)
- Correlation analysis between NLP features
- Content analysis through word clouds and top hashtags
- Sentiment analysis across different account categories and regions

#### Network Analysis (eda_network.py)
- Hashtag co-occurrence networks
- Mention networks
- Network density and size calculations
- Identification of central nodes and connections

#### LLM-Interpretable EDA (eda_llm.py)
- Structured JSON output generation for LLM consumption
- Comprehensive dataset summary
- Key insights extraction
- Network structure representation

## Why We Built This

### Human-Readable + Machine-Readable

Traditional EDA outputs are designed for human interpretation through visualizations and statistical summaries. However, to fully leverage the power of LLMs in understanding our dataset, we needed a way to translate these insights into a structured format that LLMs can easily process and reason with.

### Comprehensive Understanding

The LLM-interpretable EDA framework ensures that LLMs can gain a complete understanding of:
- Dataset structure and composition
- Feature distributions and relationships
- Temporal patterns
- Text characteristics
- Sentiment patterns
- Network structures and relationships

### Enabling LLM-Assisted Analysis

By providing structured, comprehensive data summaries to LLMs, we enable them to:
1. Synthesize complex patterns across multiple dimensions
2. Identify anomalies and interesting correlations
3. Generate insights that might be missed in traditional visual analysis
4. Assist in feature engineering and selection

## How It Works

### Data Processing Pipeline

1. **Data Loading**: The dataset is loaded from processed CSV files
2. **Basic Analysis**: Statistical summaries and distributions are calculated
3. **Feature Analysis**: Categorical, numerical, and temporal features are analyzed
4. **NLP Processing**: Text features are extracted and analyzed
5. **Network Analysis**: Hashtag and mention networks are constructed
6. **LLM Context Generation**: All analyses are compiled into structured JSON
7. **Insight Extraction**: Key patterns, anomalies, and relationships are identified

### LLM-Interpretable Output Format

The framework generates two main JSON files:

1. **llm_eda_context.json**: A comprehensive dataset summary containing:
   - Dataset overview (shape, types, missing values)
   - Categorical feature analysis (distributions, unique values)
   - Numerical feature analysis (statistics, distributions, correlations)
   - Temporal pattern analysis (hourly/daily distributions, peak times)
   - NLP feature analysis (text characteristics, hashtag usage)
   - Sentiment analysis (distributions, patterns by category/region)
   - Network analysis (hashtag/mention networks, key nodes)

2. **llm_eda_context_insights.json**: Extracted key insights including:
   - Dominant patterns in the data
   - Anomalies and outliers
   - Strong correlations
   - Imbalanced distributions
   - Network characteristics

### Network Analysis Approach

The network analysis module constructs and analyzes two types of networks:

1. **Hashtag Co-occurrence Network**:
   - Nodes represent hashtags
   - Edges represent co-occurrence in the same tweet
   - Weight reflects frequency of co-occurrence
   
2. **Mention Network**:
   - Nodes represent mentioned accounts
   - Edges represent co-mention in the same tweet
   - Weight reflects frequency of co-mention

Both networks are analyzed for:
- Size (number of nodes/edges)
- Density (proportion of potential connections that exist)
- Central nodes (most frequently occurring)
- Connection patterns

## Usage

### Running the Full EDA Pipeline

To execute the complete EDA pipeline:

```python
from src.eda import eda

eda()
```

This will:
1. Load the data
2. Perform all analyses
3. Generate visualizations in the `plots` directory
4. Create LLM-interpretable outputs:
   - `llm_eda_context.json`: Complete dataset summary
   - `llm_eda_context_insights.json`: Key insights
   - `network_data.json`: Network structure data

### Using Only LLM Context Generation

To generate just the LLM-interpretable outputs for an existing DataFrame:

```python
from src.eda.eda_llm import save_llm_context, generate_llm_insights
import json

# Generate and save the comprehensive context
save_llm_context(dataframe, "output_path.json")

# Generate insights
insights = generate_llm_insights(dataframe)
with open("insights_path.json", 'w') as f:
    json.dump(insights, f, indent=2)
```

### Using Network Analysis

To perform only network analysis:

```python
from src.eda.eda_network import save_network_data

save_network_data(dataframe, "network_output.json")
```

## Implementation Details

### Data Representation for LLMs

The LLM-interpretable output formats all numerical data as native JSON numbers and ensures all keys and values are descriptive and well-structured. Special attention was given to:

1. **Consistency**: Using consistent naming conventions and data structures
2. **Completeness**: Including all relevant information while avoiding redundancy
3. **Clarity**: Using descriptive keys and hierarchical organization
4. **Compactness**: Limiting output size while preserving information content

### Network Representation

Networks are represented in a node-edge format:
- Nodes include identifiers and weights
- Edges include source, target, and weight information
- Summary statistics provide quick insights into structure

For LLM consumption, we simplify the networks to include only the most significant nodes and connections.

## Example Output Structure

The LLM-interpretable output follows this general structure:

```json
{
  "metadata": {
    "dataset_name": "Twitter Troll Dataset",
    "analysis_timestamp": "2023-05-15T12:34:56.789012",
    "number_of_features": 25,
    "number_of_samples": 240000
  },
  "dataset_overview": {
    "dataset_shape": {"rows": 240000, "columns": 25},
    "column_types": {...},
    "missing_values": {...},
    "numerical_columns": [...],
    "categorical_columns": [...],
    "temporal_columns": [...],
    "numerical_summary": {...}
  },
  "categorical_analysis": {...},
  "numerical_analysis": {...},
  "temporal_analysis": {...},
  "nlp_analysis": {...},
  "sentiment_analysis": {...},
  "network_analysis": {...}
}
```

## Future Enhancements

Potential future improvements:
- Integration with interactive visualization tools
- Dynamic querying of the LLM context
- Automatic interpretation generation
- Real-time analysis capabilities
- Comparison between multiple datasets

## Dependencies

- pandas: Data manipulation and analysis
- numpy: Numerical computing
- matplotlib & seaborn: Data visualization
- nltk: Natural language processing
- json: JSON file handling
- collections: Specialized container datatypes 