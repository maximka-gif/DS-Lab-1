import requests
from bs4 import BeautifulSoup
from typing import Dict

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_wikipedia_page(url: str) -> str:
    """
    Fetch the HTML content of the given Wikipedia page.

    Args:
        url (str): The URL of the Wikipedia page to fetch.

    Returns:
        str: The HTML content of the page as a string.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If there was a network error.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) DS-Lab-1-Bot/1.0"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract the title of the Wikipedia page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.

    Returns:
        str: The title of the page.
    """
    heading = soup.find("h1", id="firstHeading")
    if heading:
        return heading.get_text(strip=True)
    raise ValueError("Could not find page title (<h1 id='firstHeading'>).")


def extract_first_sentence(soup: BeautifulSoup) -> str:
    """
    Extract the first sentence of the first paragraph on the Wikipedia page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.

    Returns:
        str: The first sentence of the first paragraph.
    """
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if text:
            first_sentence = text.split(".")[0].strip()
            return f"{first_sentence}."
    raise ValueError("Could not find any non-empty paragraph (<p>).")


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    try:
        page_content = fetch_wikipedia_page(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        title = extract_title(soup)

        first_sentence = extract_first_sentence(soup)

        extracted_data = {
            "title": title,
            "first_sentence": first_sentence
        }

        print("Extracted Data:", extracted_data)

        save_to_json(extracted_data, 'extracted_wikipedia_data.json')

        print("Data successfully saved to extracted_wikipedia_data.json")
    except Exception as e:
        print(f"An error occurred: {e}")