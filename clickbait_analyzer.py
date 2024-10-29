import pandas as pd
import re
from textblob import TextBlob
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def analyze_clickbait(file_path):
    """
    Analyze headlines for clickbait characteristics using comprehensive patterns
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Comprehensive clickbait patterns
    emotional_words = {
        # Extreme/Sensational
        'shocking', 'unbelievable', 'amazing', 'incredible', 'mind-blowing',
        'insane', 'crazy', 'staggering', 'extraordinary', 'spectacular',
        'breathtaking', 'phenomenal', 'revolutionary', 'game-changing',
        'devastating', 'terrifying', 'horrifying', 'astonishing', 'devastating',
        
        # Superlatives
        'best', 'worst', 'ultimate', 'perfect', 'essential', 'crucial',
        'greatest', 'absolute', 'totally', 'completely', 'entirely',
        'never', 'ever', 'always', 'impossible', 'magical', 'legendary',
        
        # Emotional Appeal
        'heartbreaking', 'touching', 'moving', 'powerful', 'inspiring',
        'adorable', 'beautiful', 'hilarious', 'horrible', 'tragic',
        'outrageous', 'furious', 'genius', 'wonderful', 'magnificent',
        'terrible', 'awful', 'disgusting', 'brilliant', 'fantastic',
        
        # Urgency/Fear
        'urgent', 'breaking', 'warning', 'alert', 'danger',
        'threat', 'critical', 'emergency', 'deadly', 'killer',
        'viral', 'spreading', 'panic', 'crisis', 'nightmare',
        
        # Mystery/Curiosity
        'secret', 'hidden', 'revealed', 'mysterious', 'strange',
        'weird', 'suspicious', 'surprising', 'shocking', 'discovered',
        'finally', 'actually', 'truth', 'real reason', 'what happened',
        
        # Success/Transformation
        'miracle', 'breakthrough', 'transformed', 'life-changing',
        'successful', 'triumph', 'revolutionary', 'innovative', 'groundbreaking',
        
        # Controversy/Conflict
        'controversial', 'scandal', 'exposed', 'accused', 'versus',
        'fight', 'battle', 'war', 'chaos', 'crisis', 'feud', 'clash'
    }
    
    clickbait_phrases = {
        'you won\'t believe', 'never seen before', 'changed forever',
        'what happened next', 'goes viral', 'breaks the internet',
        'here\'s why', 'the truth about', 'this is why',
        'what you need', 'must see', 'need to know'
    }
    
    number_patterns = {
        'top', 'reasons why', 'ways to', 'things you',
        'facts', 'tricks', 'secrets', 'tips', 'ideas',
        'steps', 'lessons', 'principles', 'rules'
    }
    
    def analyze_headline(headline):
        headline = str(headline).lower()
        
        features = {
            'emotional_words': 0,
            'clickbait_phrases': 0,
            'number_patterns': 0,
            'question_marks': headline.count('?'),
            'exclamation_marks': headline.count('!'),
            'all_caps_words': sum(1 for word in headline.split() if word.isupper()),
            'personal_pronouns': len(re.findall(r'\b(you|your|you\'re|we|our)\b', headline, re.IGNORECASE)),
            'starts_number': int(bool(re.match(r'^\d+', headline))),
            'ellipsis': headline.count('...'),
        }
        
        # Count emotional words
        features['emotional_words'] = sum(1 for word in emotional_words 
                                        if word in headline)
        
        # Count clickbait phrases
        features['clickbait_phrases'] = sum(1 for phrase in clickbait_phrases 
                                          if phrase in headline)
        
        # Count number patterns
        features['number_patterns'] = sum(1 for pattern in number_patterns 
                                        if pattern in headline)
        
        # Get sentiment intensity
        features['sentiment_intensity'] = abs(TextBlob(headline).sentiment.polarity)
        
        # Calculate clickbait score with weights
        score = (
            features['emotional_words'] * 2.0 +
            features['clickbait_phrases'] * 2.5 +
            features['number_patterns'] * 1.5 +
            features['question_marks'] * 1.0 +
            features['exclamation_marks'] * 1.5 +
            features['all_caps_words'] * 1.0 +
            features['personal_pronouns'] * 1.5 +
            features['sentiment_intensity'] * 2.0 +
            features['starts_number'] * 1.5 +
            features['ellipsis'] * 1.0
        )
        
        return features, score

    # Analyze all headlines
    results = [analyze_headline(h) for h in df['headline']]
    features_list, scores = zip(*results)
    
    # Add scores to dataframe
    df['clickbait_score'] = scores
    
    # Add individual features to dataframe
    for feature in features_list[0].keys():
        df[f'feature_{feature}'] = [f[feature] for f in features_list]
    
    # Calculate summary statistics
    summary = {
        'total_headlines': len(df),
        'avg_clickbait_score': np.mean(scores),
        'median_clickbait_score': np.median(scores),
        'std_clickbait_score': np.std(scores),
        'high_clickbait_count': sum(1 for score in scores if score > 5),
        'most_clickbaity': df.nlargest(10, 'clickbait_score')[['headline', 'clickbait_score']].values.tolist(),
        'least_clickbaity': df.nsmallest(5, 'clickbait_score')[['headline', 'clickbait_score']].values.tolist()
    }
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # Distribution of clickbait scores
    plt.subplot(2, 2, 1)
    sns.histplot(data=df['clickbait_score'], bins=30)
    plt.title('Distribution of Clickbait Scores')
    plt.xlabel('Clickbait Score')
    
    # Feature importance
    plt.subplot(2, 2, 2)
    feature_means = df[[col for col in df.columns if col.startswith('feature_')]].mean()
    sns.barplot(x=feature_means.values, y=[col.replace('feature_', '') for col in feature_means.index])
    plt.title('Average Feature Occurrence')
    plt.xlabel('Average Count')
    
    plt.tight_layout()
    plt.savefig('clickbait_analysis.png')
    plt.close()
    
    return df, summary

# Run the analysis
print("Analyzing headlines for clickbait...")
df, summary = analyze_clickbait('foxnews_h3_elements.csv')

# Print results
print("\n=== Clickbait Analysis Results ===")
print(f"\nTotal Headlines Analyzed: {summary['total_headlines']}")
print(f"Average Clickbait Score: {summary['avg_clickbait_score']:.2f}")
print(f"Median Clickbait Score: {summary['median_clickbait_score']:.2f}")
print(f"Standard Deviation: {summary['std_clickbait_score']:.2f}")
print(f"Headlines with High Clickbait Score (>5): {summary['high_clickbait_count']}")

print("\nTop 10 Most Clickbaity Headlines:")
for headline, score in summary['most_clickbaity']:
    print(f"- Score {score:.2f}: {headline}")

print("\nLeast Clickbaity Headlines:")
for headline, score in summary['least_clickbaity']:
    print(f"- Score {score:.2f}: {headline}")

# Save results
df.to_csv('FOX_headlines_with_clickbait_analysis.csv', index=False)
print("\nResults saved to 'headlines_with_clickbait_analysis.csv'")
print("Visualizations saved to 'clickbait_analysis.png'")