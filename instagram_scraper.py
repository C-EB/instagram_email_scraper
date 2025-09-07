import time
import random
from typing import Optional, Tuple, Set

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import config
from logger import get_logger
from utils import find_emails_in_text

logger = get_logger(__name__)

class InstagramScraper:
    """
    A class to scrape data from Instagram using Selenium.
    """

    def __init__(self):
        """
        Initializes the InstagramScraper.
        """
        self.driver = self._init_driver()
        self.is_logged_in = False

    def _init_driver(self) -> uc.Chrome:
        """
        Initializes the undetected_chromedriver.

        Returns:
            uc.Chrome: The Chrome driver instance.
        """
        logger.info("Initializing Chrome driver...")
        options = uc.ChromeOptions()
        # Add arguments to prevent detection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        driver = uc.Chrome(options=options)
        return driver

    def login(self):
        """
        Logs into Instagram using credentials from the config.
        """
        if self.is_logged_in:
            logger.info("Already logged in.")
            return

        logger.info("Logging into Instagram...")
        self.driver.get("https://www.instagram.com/accounts/login/")
        try:
            # Wait for the username input field to be present
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_input = self.driver.find_element(By.NAME, "password")

            # Introduce random delays to mimic human behavior
            time.sleep(random.uniform(1, 3))
            username_input.send_keys(config.instagram_username)
            time.sleep(random.uniform(1, 2))
            password_input.send_keys(config.instagram_password)
            time.sleep(random.uniform(1, 2))

            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            # Wait for the login to complete by checking for a known element on the home page
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Home')]"))
            )
            self.is_logged_in = True
            logger.info("Successfully logged in.")
        except TimeoutException:
            logger.error("Login failed: Timed out waiting for page elements.")
            self.close()
        except NoSuchElementException as e:
            logger.error(f"Login failed: Could not find an element - {e}")
            self.close()

    def get_profile_info(self, username: str) -> Optional[Tuple[Optional[str], Optional[str]]]:
        """
        Navigates to an influencer's profile and scrapes their bio and website.

        Args:
            username (str): The Instagram username of the influencer.

        Returns:
            Optional[Tuple[Optional[str], Optional[str]]]: A tuple containing the bio text and website URL, or None if the profile is not found.
        """
        logger.info(f"Fetching profile info for {username}...")
        profile_url = f"https://www.instagram.com/{username}/"
        self.driver.get(profile_url)

        # Add random delay to mimic human behavior
        time.sleep(random.uniform(2, 4))

        bio_text = None
        website_url = None

        try:
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "header"))
            )

            # Extract bio text using multiple selectors
            bio_text = self._extract_bio_text()
            
            # Extract website URL
            website_url = self._extract_website_url()

            logger.info(f"Successfully extracted profile info for {username}")
            
        except TimeoutException:
            logger.warning(f"Could not load profile for {username}. The profile might be private or does not exist.")
            return None, None

        return bio_text, website_url

    def _extract_bio_text(self) -> Optional[str]:
        """
        Extract bio text using multiple methods for better reliability.
        
        Returns:
            Optional[str]: The bio text or None if not found.
        """
        bio_selectors = [
            # Primary bio text selector
            "span[class*='_ap3a'][class*='_aaco'][class*='_aacu'][class*='_aacx'][class*='_aad7'][class*='_aade']",
            # Alternative selectors
            "div[class*='x7a106z'] span[dir='auto']",
            "header section[class*='xc3tme8'] div span[dir='auto']",
            # Fallback to broader bio section
            "section[class*='xc3tme8'][class*='x1xdureb'][class*='x18wylqe'][class*='x1vnunu7']"
        ]

        for selector in bio_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and len(text) > 10:  # Filter out empty or very short text
                        logger.debug(f"Found bio text using selector: {selector}")
                        return text
            except NoSuchElementException:
                continue

        logger.warning("Could not extract bio text using any selector")
        return None

    def _extract_website_url(self) -> Optional[str]:
        """
        Extract website URL from bio.
        
        Returns:
            Optional[str]: The website URL or None if not found.
        """
        website_selectors = [
            # Standard external link selector
            'a[rel="me nofollow noopener noreferrer"]',
            # Alternative selectors for external links
            'a[href^="http"]:not([href*="instagram.com"])',
            # Links in bio area that don't start with /
            'section[class*="xc3tme8"] a:not([href^="/"])',
            # Button with link icon (for "youtube.com/@mekaito and 2 more" type)
            'button[class*="_aswp"] + a',
            'button svg[aria-label="Link icon"] + div'
        ]

        for selector in website_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if selector.endswith('div'):  # For text content
                    url_text = element.text.strip()
                    if url_text and ('.' in url_text) and not url_text.startswith('@'):
                        logger.debug(f"Found website URL in text: {url_text}")
                        return url_text
                else:  # For href attributes
                    url = element.get_attribute('href')
                    if url:
                        logger.debug(f"Found website URL: {url}")
                        return url
            except NoSuchElementException:
                continue

        logger.debug("No website URL found")
        return None

    def scrape_email_from_profile(self, username: str) -> Set[str]:
        """
        Scrapes email directly from an Instagram profile's bio.

        Args:
            username (str): The Instagram username.

        Returns:
            Set[str]: A set of unique emails found in the bio.
        """
        logger.info(f"Scraping emails from profile: {username}")
        
        bio_text, website_url = self.get_profile_info(username)
        emails = set()
        
        if bio_text:
            logger.debug(f"Bio text found: {bio_text[:100]}...")
            found_emails = find_emails_in_text(bio_text)
            emails.update(found_emails)
            
            if found_emails:
                logger.info(f"Found {len(found_emails)} email(s) in bio: {found_emails}")
            else:
                logger.info("No emails found in bio text")
        else:
            logger.warning(f"No bio text found for {username}")

        # Also check if there are any email links (mailto:)
        try:
            mailto_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href^="mailto:"]')
            for link in mailto_links:
                href = link.get_attribute('href')
                if href and href.startswith('mailto:'):
                    email = href.replace('mailto:', '')
                    emails.add(email)
                    logger.info(f"Found email in mailto link: {email}")
        except NoSuchElementException:
            pass

        return emails

    def get_detailed_profile_info(self, username: str) -> dict:
        """
        Get comprehensive profile information including emails.
        
        Args:
            username (str): The Instagram username.
            
        Returns:
            dict: Dictionary containing all profile information.
        """
        logger.info(f"Getting detailed profile info for {username}")
        
        profile_url = f"https://www.instagram.com/{username}/"
        self.driver.get(profile_url)
        time.sleep(random.uniform(2, 4))

        profile_info = {
            'username': username,
            'display_name': None,
            'bio_text': None,
            'website_url': None,
            'emails': set(),
            'follower_count': None,
            'following_count': None,
            'post_count': None,
            'category': None
        }

        try:
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "header"))
            )

            # Extract display name
            try:
                display_name_element = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    "span[class*='xvs91rp'][class*='x1s688f']"
                )
                profile_info['display_name'] = display_name_element.text.strip()
            except NoSuchElementException:
                pass

            # Extract category (Digital creator, etc.)
            try:
                category_element = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "div[class*='_ap3a'][class*='_aaco'][class*='_aacu'][class*='_aacy']"
                )
                profile_info['category'] = category_element.text.strip()
            except NoSuchElementException:
                pass

            # Extract bio and website
            profile_info['bio_text'] = self._extract_bio_text()
            profile_info['website_url'] = self._extract_website_url()

            # Extract emails from bio
            if profile_info['bio_text']:
                profile_info['emails'] = find_emails_in_text(profile_info['bio_text'])

            # Extract follower stats
            try:
                stats_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    "span[class*='x5n08af'][class*='x1s688f'] span"
                )
                
                for element in stats_elements:
                    parent_text = element.find_element(By.XPATH, "../..").text.lower()
                    value = element.text.strip()
                    
                    if 'followers' in parent_text:
                        profile_info['follower_count'] = value
                    elif 'following' in parent_text:
                        profile_info['following_count'] = value
                    elif 'posts' in parent_text:
                        profile_info['post_count'] = value
                        
            except NoSuchElementException:
                pass

            logger.info(f"Successfully extracted detailed info for {username}")
            
        except TimeoutException:
            logger.error(f"Timeout while extracting detailed info for {username}")

        return profile_info

    def close(self):
        """
        Closes the browser and quits the driver.
        """
        if self.driver:
            logger.info("Closing the browser.")
            self.driver.quit()