import pandas as pd
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
from keybert import KeyBERT
from nltk.tokenize import word_tokenize
import re
import matplotlib.pyplot as plt
from pprint import pprint
from collections import Counter

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def load_and_preprocess(file_path):
    """
    Load and preprocess the headlines
    """
    df = pd.read_csv(file_path)
    headlines = df['headline'].astype(str).tolist()
    
    def preprocess_text(text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join(text.split())
        return text
    
    processed_headlines = [preprocess_text(headline) for headline in headlines]
    processed_headlines = [headline for headline in processed_headlines if headline.strip()]
    
    return processed_headlines, headlines  # Return both processed and original headlines

def create_lda_model(processed_headlines, num_topics=10):
    """
    Create and train LDA model using scikit-learn
    """
    stop_words = list(stopwords.words('english'))
    
    vectorizer = CountVectorizer(
        max_df=0.7,
        min_df=3,
        stop_words=stop_words,
        token_pattern=r'(?u)\b[a-zA-Z]{3,}\b'
    )
    
    doc_term_matrix = vectorizer.fit_transform(processed_headlines)
    
    lda_model = LatentDirichletAllocation(
        n_components=num_topics,
        random_state=42,
        max_iter=20,
        learning_method='online'
    )
    
    doc_topics = lda_model.fit_transform(doc_term_matrix)
    
    return lda_model, vectorizer, doc_topics, doc_term_matrix

def get_topic_labels(lda_model, vectorizer, original_headlines, doc_topics):
    """
    Generate meaningful labels for topics using KeyBERT and topic keywords
    """
    feature_names = vectorizer.get_feature_names_out()
    kw_model = KeyBERT()
    labels = {}
    
    for topic_idx, topic in enumerate(lda_model.components_):
        # Get top documents for this topic
        top_doc_indices = doc_topics[:, topic_idx].argsort()[-5:][::-1]
        topic_docs = [original_headlines[idx] for idx in top_doc_indices]
        
        # Get top words for this topic
        top_words_idx = topic.argsort()[:-10:-1]
        top_words = [feature_names[i] for i in top_words_idx]
        
        # Use KeyBERT to extract keywords from the top documents
        topic_text = ' '.join(topic_docs)
        keywords = kw_model.extract_keywords(topic_text, 
                                          keyphrase_ngram_range=(1, 2),
                                          stop_words='english',
                                          use_maxsum=True,
                                          nr_candidates=20,
                                          top_n=1)
        
        # Combine KeyBERT label with top words
        if keywords:
            main_label = keywords[0][0]
        else:
            main_label = top_words[0]
            
        labels[topic_idx] = {
            'main_label': main_label,
            'top_words': top_words,
            'example_headlines': topic_docs[:3]
        }
    
    return labels

def analyze_topics(lda_model, vectorizer, doc_topics, topic_labels):
    """
    Analyze and visualize the topics with their labels
    """
    # Print labeled topics
    print("\nTopics with automatically generated labels:")
    for topic_idx, topic_info in topic_labels.items():
        print(f"\nTopic {topic_idx}: {topic_info['main_label'].upper()}")
        print(f"Top keywords: {', '.join(topic_info['top_words'])}")
        print("Example headlines:")
        for headline in topic_info['example_headlines']:
            print(f"- {headline}")
    
    # Calculate and plot topic distribution
    topic_weights = doc_topics.mean(axis=0)
    
    plt.figure(figsize=(15, 7))
    bars = plt.bar(range(len(topic_weights)), topic_weights)
    plt.xlabel('Topics')
    plt.ylabel('Average Weight')
    plt.title('Topic Distribution in Headlines')
    
    # Add labels to bars
    plt.xticks(range(len(topic_weights)), 
              [f"{topic_labels[i]['main_label'][:10]}..." for i in range(len(topic_weights))],
              rotation=45,
              ha='right')
    
    plt.tight_layout()
    plt.savefig('topic_distribution_labeled.png')
    plt.close()
    
    return topic_weights

def assign_headlines_to_topics(doc_topics, original_headlines, topic_labels):
    """
    Assign each headline to its most probable topic
    """
    headline_topics = {}
    for idx, headline in enumerate(original_headlines):
        topic_probs = doc_topics[idx]
        main_topic = topic_probs.argmax()
        prob = topic_probs[main_topic]
        
        topic_label = topic_labels[main_topic]['main_label']
        
        if topic_label not in headline_topics:
            headline_topics[topic_label] = []
        
        headline_topics[topic_label].append((headline, prob))
    
    return headline_topics

def main():
    # Load and process the data
    processed_headlines, original_headlines = load_and_preprocess('cnn_headlines.csv')
    
    # Create and train the model
    lda_model, vectorizer, doc_topics, doc_term_matrix = create_lda_model(processed_headlines)
    
    # Generate topic labels
    topic_labels = get_topic_labels(lda_model, vectorizer, original_headlines, doc_topics)
    
    # Analyze topics with labels
    topic_weights = analyze_topics(lda_model, vectorizer, doc_topics, topic_labels)
    
    # Assign headlines to topics
    headline_topics = assign_headlines_to_topics(doc_topics, original_headlines, topic_labels)
    
    # Print headlines by topic
    print("\nHeadlines grouped by topic:")
    for topic_label, headlines in headline_topics.items():
        print(f"\nTOPIC: {topic_label.upper()}")
        # Sort by probability and show top 5
        sorted_headlines = sorted(headlines, key=lambda x: x[1], reverse=True)[:5]
        for headline, prob in sorted_headlines:
            print(f"- {headline} (probability: {prob:.3f})")

    # Print model evaluation metrics
    print("\nModel Evaluation:")
    print(f"Perplexity: {lda_model.perplexity(doc_term_matrix):.2f}")
    print(f"Log Likelihood: {lda_model.score(doc_term_matrix):.2f}")

if __name__ == "__main__":
    main()