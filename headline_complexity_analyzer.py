import pandas as pd
import numpy as np
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import matplotlib.pyplot as plt
import seaborn as sns

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def analyze_complexity(file_path):
    """
    Analyze headline complexity using various metrics
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    def get_headline_metrics(headline):
        # Ensure headline is string
        headline = str(headline)
        
        # Basic length metrics
        words = word_tokenize(headline)
        chars = len(headline)
        
        # Get parts of speech
        pos_tags = nltk.pos_tag(words)
        
        metrics = {
            'word_count': len(words),
            'char_count': chars,
            'avg_word_length': chars / len(words) if words else 0,
            'complex_words': sum(1 for word in words if len(word) > 6),
            'nouns': sum(1 for _, pos in pos_tags if pos.startswith('NN')),
            'verbs': sum(1 for _, pos in pos_tags if pos.startswith('VB')),
            'adjectives': sum(1 for _, pos in pos_tags if pos.startswith('JJ')),
            'prepositions': sum(1 for _, pos in pos_tags if pos.startswith('IN')),
        }
        
        # Calculate additional complexity metrics
        metrics['noun_verb_ratio'] = (metrics['nouns'] / metrics['verbs'] 
                                    if metrics['verbs'] > 0 else metrics['nouns'])
        
        return metrics

    # Apply analysis to all headlines
    results = pd.DataFrame([get_headline_metrics(h) for h in df['headline']])
    
    # Combine with original dataframe
    df = pd.concat([df, results], axis=1)
    
    # Calculate summary statistics
    summary = {
        'total_headlines': len(df),
        'avg_word_count': df['word_count'].mean(),
        'avg_char_count': df['char_count'].mean(),
        'avg_word_length': df['avg_word_length'].mean(),
        'avg_complex_words': df['complex_words'].mean(),
        'avg_noun_verb_ratio': df['noun_verb_ratio'].mean(),
        'longest_headlines': df.nlargest(5, 'word_count')[['headline', 'word_count']].values.tolist(),
        'shortest_headlines': df.nsmallest(5, 'word_count')[['headline', 'word_count']].values.tolist(),
        'most_complex': df.nlargest(5, 'complex_words')[['headline', 'complex_words']].values.tolist()
    }
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # Word count distribution
    plt.subplot(2, 2, 1)
    sns.histplot(data=df['word_count'], bins=20)
    plt.title('Distribution of Headline Word Counts')
    plt.xlabel('Word Count')
    
    # Average word length distribution
    plt.subplot(2, 2, 2)
    sns.histplot(data=df['avg_word_length'], bins=20)
    plt.title('Distribution of Average Word Lengths')
    plt.xlabel('Average Word Length')
    
    # Parts of speech composition
    plt.subplot(2, 2, 3)
    pos_data = df[['nouns', 'verbs', 'adjectives', 'prepositions']].mean()
    sns.barplot(x=pos_data.index, y=pos_data.values)
    plt.title('Average Parts of Speech Usage')
    plt.xticks(rotation=45)
    
    # Complex words vs. total words
    plt.subplot(2, 2, 4)
    plt.scatter(df['word_count'], df['complex_words'])
    plt.title('Complex Words vs Total Words')
    plt.xlabel('Total Words')
    plt.ylabel('Complex Words')
    
    plt.tight_layout()
    plt.savefig('headline_complexity_analysis.png')
    plt.close()
    
    return df, summary

# Run the analysis
df, summary = analyze_complexity('foxnews_h3_elements.csv')

# Print results
print("\n=== Headline Complexity Analysis ===")
print(f"\nGeneral Statistics:")
print(f"Total Headlines Analyzed: {summary['total_headlines']}")
print(f"Average Word Count: {summary['avg_word_count']:.2f}")
print(f"Average Character Count: {summary['avg_char_count']:.2f}")
print(f"Average Word Length: {summary['avg_word_length']:.2f}")
print(f"Average Complex Words per Headline: {summary['avg_complex_words']:.2f}")
print(f"Average Noun/Verb Ratio: {summary['avg_noun_verb_ratio']:.2f}")

print("\nLongest Headlines:")
for headline, count in summary['longest_headlines']:
    print(f"- {headline} ({count} words)")

print("\nShortest Headlines:")
for headline, count in summary['shortest_headlines']:
    print(f"- {headline} ({count} words)")

print("\nMost Complex Headlines:")
for headline, count in summary['most_complex']:
    print(f"- {headline} ({count} complex words)")

# Save results to CSV
df.to_csv('headlines_with_complexity_metrics.csv', index=False)