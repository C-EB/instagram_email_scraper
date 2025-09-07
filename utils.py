import re
from typing import List, Optional, Set
from email_validator import validate_email, EmailNotValidError
from logger import get_logger

logger = get_logger(__name__)

def find_emails_in_text(text: str) -> Set[str]:
    """
    Finds all email addresses in a given text using regex.

    Args:
        text (str): The text to search for emails.

    Returns:
        Set[str]: A set of unique email addresses found in the text.
    """
    if not text:
        return set()

    # A comprehensive regex for finding email addresses
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return set(re.findall(email_regex, text))

def is_valid_email(email: str) -> bool:
    """
    Validates an email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        logger.debug(f"Invalid email '{email}': {e}")
        return False

def clean_and_verify_emails(emails: Set[str]) -> Set[str]:
    """
    Cleans and verifies a set of email addresses.

    Args:
        emails (Set[str]): A set of email addresses to clean and verify.

    Returns:
        Set[str]: A set of clean and verified email addresses.
    """
    verified_emails = set()
    for email in emails:
        # Simple cleaning
        cleaned_email = email.lower().strip()
        if is_valid_email(cleaned_email):
            verified_emails.add(cleaned_email)
    return verified_emails