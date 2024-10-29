#import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import csv

# SentimentAnalyzer is a class, so we are creating an instance.
analyzer = SentimentIntensityAnalyzer()

# Input and output file paths
input_file = 'cnn_headlines.csv'
output_file = 'cnn_sentiment.csv'

# Reading the input csv file with UTF-8 encoding
with open(input_file, mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    
    # Assuming the CSV contains a single column with words in each row
    words = [row[0] for row in reader]

# Writing the output sentiment analysis to a new CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    
    # Write the header
    writer.writerow(['word', 'neg', 'neu', 'pos', 'compound'])
    
    # Perform sentiment analysis for each word and write results
    for word in words:
        scores = analyzer.polarity_scores(word)
        writer.writerow([word, scores['neg'], scores['neu'], scores['pos'], scores['compound']])

print(f"Sentiment analysis complete. Results saved to {output_file}")