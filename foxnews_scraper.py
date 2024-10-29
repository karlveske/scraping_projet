import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# If you are using a proxy (Optional)
PROXY = os.getenv("PROXY")
proxies = {
    "http": PROXY,
    "https": PROXY
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

# Function to scrape all h3 elements from foxnews.com
def scrape_h3_elements(url):
    try:
        # Make an HTTP request to the webpage
        response = requests.get(url, headers=headers, proxies=proxies)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract all h3 elements
            h3_elements = [h3.get_text(strip=True) for h3 in soup.find_all('h3')]

            # Optionally, print the extracted h3 elements to verify the output
            print(h3_elements)

            # Save the h3 elements to a DataFrame, where each h3 element is a separate row
            df = pd.DataFrame(h3_elements, columns=["headline"])
            df.to_csv("foxnews_h3_elements.csv", index=False)
            print("H3 elements scraped and saved successfully to foxnews_h3_elements.csv!")
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # URL of the webpage to scrape
    url = "https://www.foxnews.com/"
    scrape_h3_elements(url)
