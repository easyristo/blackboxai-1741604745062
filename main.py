import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from config import SCRAPE_HOUR, SCRAPE_MINUTE, LOG_FILE
from scraper import scrape_price
from db import init_db, insert_price

def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

def scheduled_scrape():
    """
    The main job function that will be scheduled.
    Scrapes the price and saves it to the database.
    """
    try:
        # Get the current timestamp
        scrape_time = datetime.now().isoformat()
        
        # Scrape the price
        price = scrape_price()
        
        # Save to database
        insert_price(price, scrape_time)
        
        logging.info(f"Successfully completed scheduled scrape at {scrape_time}")
        
    except Exception as e:
        logging.error(f"Error in scheduled scrape: {e}")

def calculate_next_run():
    """Calculate the next run time based on current time and scheduled hour/minute."""
    now = datetime.now()
    next_run = now.replace(hour=SCRAPE_HOUR, minute=SCRAPE_MINUTE, second=0, microsecond=0)
    
    # If the scheduled time has already passed today, set for tomorrow
    if next_run <= now:
        next_run += timedelta(days=1)
    
    return next_run

def main():
    """Main function to set up and start the scheduler."""
    try:
        # Set up logging
        setup_logging()
        logging.info("Starting electricity price scraper")
        
        # Initialize the database
        init_db()
        
        # Create the scheduler
        scheduler = BlockingScheduler()
        
        # Add the job to run at specified time
        scheduler.add_job(
            scheduled_scrape,
            trigger=CronTrigger(hour=SCRAPE_HOUR, minute=SCRAPE_MINUTE),
            id='price_scraper',
            name='Scrape electricity prices',
            misfire_grace_time=60
        )
        
        # Calculate and log the next run time
        next_run = calculate_next_run()
        logging.info(f"Next scheduled run at: {next_run}")
        
        # Start the scheduler
        logging.info("Starting scheduler...")
        scheduler.start()
        
    except Exception as e:
        logging.error(f"Error in main function: {e}")
        raise

if __name__ == "__main__":
    main()
