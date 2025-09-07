# Instagram Influencer Email Scraper

A production-ready Python web scraper designed to collect public contact emails from high-follower Instagram influencers. The tool is built with a focus on modularity, maintainability, and best practices. It offers two distinct methods for data collection: scraping directly from Instagram profiles or crawling the external websites linked in their bios.

## Project Description

This project provides a systematic way to gather publicly available contact information from Instagram influencers. It automates the process of visiting profiles, extracting potential emails from bios, and crawling linked websites for contact details. The scraper is designed for educational and professional purposes, such as for marketing research or outreach campaigns, where accessing public contact information at a modest scale is required.

**Disclaimer:** This tool is for educational purposes only. Automated data collection is against Instagram's Terms of Service. Users should be aware of and comply with Instagram's policies. The developers of this tool are not responsible for any misuse or consequences, such as account suspension or IP blocks. **Use this tool responsibly and at your own risk.**

## Goal of the Project

The primary goal is to provide a reliable, free, and open-source tool for professionals who need to compile a list of public contact emails from a specific set of Instagram influencers. It solves the manual and time-consuming task of visiting each profile and website individually. The intended audience includes marketing professionals, talent scouts, researchers, and developers looking for a well-structured example of a web scraping project.

## Features

-   **Dual Scraping Modes**: Scrape emails directly from Instagram bios or from linked external websites.
-   **Bulk Input**: Accepts a list of influencer usernames from a text file for batch processing.
-   **Data Validation**: Includes a robust email verification and cleaning module to ensure the quality and validity of the collected emails, filtering out junk and invalid formats.
-   **Clean Output**: Saves the collected data in a structured CSV or JSON file, including the username, verified email, and the source of the find.
-   **Maintainable Code**: Written in a modular structure with clear separation of concerns (configuration, logging, utilities, and scrapers).
-   **Secure Configuration**: Uses environment variables (`.env` file) to manage sensitive data like login credentials, keeping them separate from the source code.
-   **Error Handling & Logging**: Implements error handling for common issues like network timeouts and missing data, with a lightweight logging system for monitoring and debugging.
-   **Human-like Behavior**: Utilizes `undetected-chromedriver` and randomized delays to minimize the risk of detection and blocking by Instagram.

## Installation Instructions

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites
-   Python 3.8+
-   Google Chrome browser installed.

### 2. Clone the Repository
Clone the project to your local machine using Git:
```bash
git clone https://github.com/your-username/instagram-email-scraper.git
cd instagram-email-scraper
```

### 3. Set Up a Virtual Environment
It is a best practice to use a virtual environment to manage project dependencies.
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 4. Install Dependencies
Install all the required Python libraries using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 5. Configure Credentials
Create a file named `.env` in the root directory of the project. This file will hold your Instagram credentials. **It is highly recommended to use a secondary or test account for scraping.**

Add the following lines to your `.env` file:
```env
INSTAGRAM_USERNAME="your_instagram_username"
INSTAGRAM_PASSWORD="your_instagram_password"
```

## Usage Examples

### 1. Prepare Input File
Create a file named `influencers.txt` in the project root. Add the Instagram usernames you wish to scrape, with one username per line.

**Example `influencers.txt`:**
```
cristiano
natgeo
nasa
```

### 2. Run the Scraper
You can run the scraper from your terminal using command-line arguments to specify the scraping source.

**Option 1: Scrape emails directly from Instagram profiles:**
```bash
python main.py --source instagram
```

**Option 2: Scrape emails from the websites linked in profiles:**
```bash
python main.py --source website
```

### 3. View the Output
The results will be saved in a `results.csv` file in the project root.

**Example `results.csv` output:**
```csv
username,email,source
cristiano,contact@cristiano.com,website
nasa,info@nasa.gov,instagram
```

## Dependencies
The project relies on the following open-source Python libraries:
-   `requests`: For making HTTP requests to external websites.
-   `BeautifulSoup4` (`bs4`): For parsing HTML and XML documents.
-   `selenium`: For browser automation to interact with Instagram.
-   `undetected-chromedriver`: An optimized version of Selenium's ChromeDriver to avoid bot detection.
-   `pandas`: For easy data manipulation and saving to CSV.
-   `python-dotenv`: For managing environment variables.
-   `email-validator`: For validating and verifying email addresses.
-   `lxml`: High-performance XML and HTML parser used with BeautifulSoup.

## Project Structure
The project is organized into several modules to ensure clarity and maintainability.
```
instagram-email-scraper/
├── .env                  # Stores environment variables (credentials) - create manually
├── README.md             # This file
├── requirements.txt      # List of Python dependencies
├── influencers.txt       # Input file with target usernames
├── results.csv           # Output file with scraped data
├── main.py               # Main entry point for the application
├── config.py             # Handles loading configuration from .env
├── logger.py             # Configures the application logger
├── instagram_scraper.py  # Contains all logic for scraping Instagram
├── website_scraper.py    # Contains logic for scraping external websites
└── utils.py              # Utility functions (e.g., email validation)
```

-   **`main.py`**: The orchestrator. It parses command-line arguments, reads the input file, initializes the scrapers, and saves the results.
-   **`instagram_scraper.py`**: A class that handles all direct interactions with Instagram, including logging in, navigating to profiles, and extracting data using Selenium.
-   **`website_scraper.py`**: A module dedicated to fetching and parsing external website content to find contact information.
-   **`config.py`**: Loads credentials securely from the `.env` file and makes them available to the application.
-   **`utils.py`**: Contains helper functions, primarily for finding, cleaning, and validating email addresses to ensure data quality.
-   **`logger.py`**: Provides a simple, reusable logging configuration for consistent output across all modules.

## Contributing
Contributions are welcome! If you would like to contribute, please follow these steps:
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Open a Pull Request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Additional Notes
-   **Instagram UI Changes**: Social media platforms frequently update their website's layout and structure. These changes can break the scraper's selectors and logic. Regular maintenance may be required to keep the tool functional.
-   **Rate Limiting and IP Blocks**: To avoid being temporarily blocked, the scraper uses randomized delays. However, aggressive or high-frequency scraping can still lead to rate limiting or a temporary IP ban from Instagram. For larger-scale operations, consider integrating proxies.
