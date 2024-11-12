import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

PROXY = os.getenv("PROXY")
proxies = {
    "http": PROXY,
    "https": PROXY
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

def scrape_headline_elements(url):
    try:
        # Make an HTTP request to the webpage
        response = requests.get(url, headers=headers, proxies=proxies)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all elements with the specific class
            headlines = soup.find_all(class_="container__headline-text")

            # Extract text from headlines
            headline_data = []
            for headline in headlines:
                text = headline.get_text(strip=True)
                if text:  # Only add non-empty headlines
                    headline_data.append({'headline': text})

            # Create DataFrame
            df = pd.DataFrame(headline_data)
            
            # Remove duplicates
            df = df.drop_duplicates(subset=['headline'])
            
            # Save to CSV
            df.to_csv("cnn_headlines.csv", index=False)
            print(f"Found {len(df)} unique headlines!")
            print("Headlines scraped and saved successfully to cnn_headlines.csv!")
            
            # Print the headlines for verification
            print("\nHeadlines found:")
            for idx, row in df.iterrows():
                print(f"{idx + 1}. {row['headline']}")

        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # URL of the webpage to scrape
    url = "https://edition.cnn.com/"
    scrape_headline_elements(url)