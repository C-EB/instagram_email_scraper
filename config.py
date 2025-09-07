import os
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger(__name__)

# Load environment variables from a .env file
load_dotenv()

class Config:
    """
    Configuration class to hold settings and credentials.
    """
    def __init__(self):
        self.instagram_username = os.getenv("INSTAGRAM_USERNAME")
        self.instagram_password = os.getenv("INSTAGRAM_PASSWORD")
        self.validate()

    def validate(self):
        """
        Validates that required environment variables are set.
        Raises ValueError if a required variable is missing.
        """
        if not self.instagram_username or not self.instagram_password:
            error_msg = "Error: INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD must be set in the .env file."
            logger.error(error_msg)
            raise ValueError(error_msg)

# Instantiate the config object to be imported by other modules
try:
    config = Config()
except ValueError as e:
    # Exit if configuration is invalid
    exit(1)