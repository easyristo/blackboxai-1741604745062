# Target URL for scraping
TARGET_URL = "https://elekter.info/"

# Scheduling configuration
SCRAPE_HOUR = 15
SCRAPE_MINUTE = 39

# Database configuration
DATABASE_FILE = "prices.db"

# Logging configuration
LOG_FILE = "scraper.log"

# Request headers to mimic a browser
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
