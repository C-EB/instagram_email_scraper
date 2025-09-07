import requests
from bs4 import BeautifulSoup
from typing import Set

from logger import get_logger
from utils import find_emails_in_text

logger = get_logger(__name__)

def scrape_emails_from_website(url: str) -> Set[str]:
    """
    Scrapes email addresses from a given website URL.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        Set[str]: A set of unique email addresses found on the website.
    """
    if not url:
        return set()

    logger.info(f"Scraping emails from website: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, 'lxml')
        # Get all text from the website
        text = soup.get_text()
        
        return find_emails_in_text(text)

    except requests.exceptions.RequestException as e:
        logger.error(f"Could not fetch website {url}: {e}")
        return set()