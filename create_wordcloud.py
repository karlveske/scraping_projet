import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords

# Download required NLTK data
nltk.download('stopwords')

def create_headlines_wordcloud(csv_path, width=800, height=400):
    """
    Create a wordcloud from headlines and save word frequencies to CSV.
    
    Parameters:
    csv_path (str): Path to the CSV file containing headlines
    width (int): Width of the wordcloud image
    height (int): Height of the wordcloud image
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
    stop_words = set(stopwords.words('english'))
    
    # Add custom stopwords that might be common in headlines
    custom_stopwords = {'breaking', 'news', 'says', 'told', 'according'}
    stop_words.update(custom_stopwords)
    
    # Create and configure the WordCloud object
    wordcloud = WordCloud(
        width=width,
        height=height,
        background_color='white',
        stopwords=stop_words,
        min_font_size=10,
        max_font_size=150,
        random_state=42
    )
    
    # Generate the wordcloud
    wordcloud.generate(text)
    
    # Create the plot
    plt.figure(figsize=(width/100, height/100))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save the wordcloud
    plt.savefig('headlines_wordcloud.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Get word frequencies
    words = text.split()
    words = [word for word in words if word not in stop_words and len(word) > 1]  # Filter out single characters
    word_freq = Counter(words)
    
    # Create DataFrame from word frequencies and save to CSV
    freq_df = pd.DataFrame(word_freq.most_common(), columns=['word', 'count'])
    freq_df.to_csv('word_frequencies.csv', index=False)
    
    return word_freq.most_common(10)

# Run the analysis
word_frequencies = create_headlines_wordcloud('cnn_headlines.csv')
print("Top 10 most frequent words:", word_frequencies)