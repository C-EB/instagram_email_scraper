import argparse
import pandas as pd
from typing import List

from logger import get_logger
from instagram_scraper import InstagramScraper
from website_scraper import scrape_emails_from_website
from utils import clean_and_verify_emails

logger = get_logger(__name__)

def read_influencers(file_path: str) -> List[str]:
    """
    Reads a list of influencer usernames from a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        List[str]: A list of influencer usernames.
    """
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.error(f"Input file not found: {file_path}")
        return []

def save_results(data: List[dict], filename: str = "results.csv"):
    """
    Saves the scraped data to a CSV file.

    Args:
        data (List[dict]): A list of dictionaries containing the scraped data.
        filename (str): The name of the output file.
    """
    if not data:
        logger.info("No data to save.")
        return

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    logger.info(f"Results saved to {filename}")

def main(source: str):
    """
    Main function to run the scraper.

    Args:
        source (str): The source to scrape from ('instagram' or 'website').
    """
    influencers = read_influencers("influencers.txt")
    if not influencers:
        logger.warning("No influencers found in influencers.txt")
        return

    results = []
    scraper = InstagramScraper()
    scraper.login()

    for username in influencers:
        emails = set()
        if source == "instagram":
            raw_emails = scraper.scrape_email_from_profile(username)
            if raw_emails:
                verified_emails = clean_and_verify_emails(raw_emails)
                for email in verified_emails:
                    results.append({"username": username, "email": email, "source": "instagram"})
                    logger.info(f"Found email for {username}: {email}")

        elif source == "website":
            _, website_url = scraper.get_profile_info(username)
            if website_url:
                raw_emails = scrape_emails_from_website(website_url)
                if raw_emails:
                    verified_emails = clean_and_verify_emails(raw_emails)
                    for email in verified_emails:
                        results.append({"username": username, "email": email, "source": "website"})
                        logger.info(f"Found email for {username} on their website: {email}")

    scraper.close()
    save_results(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape emails of Instagram influencers.")
    parser.add_argument(
        "--source",
        type=str,
        choices=["instagram", "website"],
        required=True,
        help="The source to scrape emails from: 'instagram' bios or linked 'website's."
    )
    args = parser.parse_args()
    main(args.source)