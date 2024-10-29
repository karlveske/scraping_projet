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

# Function to scrape all h2 and h3 elements from a webpage
def scrape_h2_h3_elements(url):
    try:
        # Make an HTTP request to the webpage
        response = requests.get(url, headers=headers, proxies=proxies)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract all h2 and h3 elements
            h2_elements = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]
            h3_elements = [h3.get_text(strip=True) for h3 in soup.find_all('h3')]

            # Combine the h2 and h3 elements
            elements = h2_elements + h3_elements

            # Optionally, print the extracted elements to verify the output
            print(elements)

            # Save the elements to a DataFrame, where each element is a separate row
            df = pd.DataFrame(elements, columns=["header_text"])
            df.to_csv("webpage_h2_h3_elements.csv", index=False)
            print("H2 and H3 elements scraped and saved successfully to webpage_h2_h3_elements.csv!")
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # URL of the webpage to scrape
    url = "https://www.msnbc.com/"
    scrape_h2_h3_elements(url)
