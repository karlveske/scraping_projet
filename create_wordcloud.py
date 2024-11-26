import pandas as pd
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords

# Download required NLTK data
nltk.download('stopwords')

def analyze_headline_frequencies(csv_path):
    """
    Create a wordcloud from headlines and save word frequencies to CSV.
    
    Parameters:
    csv_path (str): Path to the CSV file containing headlines
    """
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Combine all headlines into one string
    text = ' '.join(df['headline'].astype(str))
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    
    # Get stopwords
    '''
     Stopwords are common words that are filtered out of text analysis because they typically don't carry significant meaning on their own. 
     These are words like "the," "is," "at, etc.
     The code uses two sets of stopwords. Built in ones and specific to news ones. 
    '''
    stop_words = set(stopwords.words('english'))
    
    # Add custom stopwords that might be common in headlines
    custom_stopwords = {'breaking', 'news', 'says', 'told', 'according'}
    stop_words.update(custom_stopwords)
    
    # Get word frequencies
    words = text.split()
    words = [word for word in words if word not in stop_words and len(word) > 1]  # Filter out single characters and stopwords
    word_freq = Counter(words)
    
    # Create DataFrame from word frequencies and save to CSV
    freq_df = pd.DataFrame(word_freq.most_common(), columns=['word', 'count'])
    freq_df.to_csv('word_frequencies.csv', index=False)
    
    return word_freq.most_common(10)

# Run the analysis
word_frequencies = analyze_headline_frequencies('cnn_headlines.csv')
print("Top 10 most frequent words:", word_frequencies)