import requests
import logging
import re
from bs4 import BeautifulSoup
from datetime import datetime
from config import TARGET_URL, REQUEST_HEADERS

def scrape_price():
    """
    Scrape the electricity price from elekter.info.
    Returns the current hour's price as a float.
    """
    try:
        # Make the HTTP request with a timeout
        response = requests.get(TARGET_URL, headers=REQUEST_HEADERS, timeout=30)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for elements containing the average price
        avg_element = soup.find(string=re.compile(r'Avg\s+\d+[.,]\d+'))
        if avg_element:
            avg_match = re.search(r'\d+[.,]\d+', avg_element)
            if avg_match:
                price_text = avg_match.group()
                price = float(price_text.replace(',', '.'))
                logging.info(f"Successfully scraped average price: {price}")
                return price

        # If average price not found, look for current hour price
        current_hour = datetime.now().hour
        hour_str = str(current_hour).zfill(2)
        
        # Find elements containing both hour and price
        hour_elements = soup.find_all(string=re.compile(rf'{hour_str}\s+\d+[.,]\d+'))
        
        for element in hour_elements:
            price_match = re.search(r'\d+[.,]\d+', element)
            if price_match:
                price_text = price_match.group()
                price = float(price_text.replace(',', '.'))
                logging.info(f"Successfully scraped price for hour {hour_str}: {price}")
                return price

        raise ValueError("No valid prices found on the page")

    except requests.RequestException as e:
        logging.error(f"Error making request to {TARGET_URL}: {e}")
        raise
    except ValueError as e:
        logging.error(f"Error parsing price: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during scraping: {e}")
        raise

def test_scraper():
    """
    Test the scraper functionality.
    Returns True if successful, False otherwise.
    """
    try:
        price = scrape_price()
        logging.info(f"Test scrape successful. Price: {price}")
        return True
    except Exception as e:
        logging.error(f"Test scrape failed: {e}")
        return False

if __name__ == "__main__":
    # Set up basic logging for testing
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    test_scraper()
