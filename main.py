from datetime import datetime

import requests
from bs4 import BeautifulSoup


def scrape_and_save_data():
    url = "https://www.distributorcentral.com/p/supplier-list"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        print("Accessing website...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        print("Parsing webpage content...")
        soup = BeautifulSoup(response.content, "html.parser")

        p_tags = soup.find_all("p")
        processed_data = []

        for p in p_tags:
            # First, replace <br> tags with a special marker
            for br in p.find_all("br"):
                br.replace_with("|BREAK|")

            text = p.text
            if text and len(text.strip()) > 1:
                # Split by our marker and process each part
                parts = text[1:].split("|BREAK|")
                parts = [part.strip() for part in parts if part.strip()]
                if parts:
                    processed_data.extend(parts)
            elif text:
                processed_data.append(text.strip())

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"supplier_data_{timestamp}.csv"

        # Create single-row CSV with all data
        with open(filename, "w", encoding="utf-8") as file:
            single_row = ",".join(processed_data)
            file.write(single_row)

        return filename, len(processed_data)

    except requests.RequestException as e:
        print(f"Error accessing the website: {str(e)}")
        return None, 0
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None, 0


if __name__ == "__main__":
    output_file, count = scrape_and_save_data()
    if output_file:
        print(f"Successfully scraped {count} items")
        print(f"Data saved to: {output_file}")
    else:
        print(
            "Scraping failed. Please check the website structure or your internet connection."
        )
