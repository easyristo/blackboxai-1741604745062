import sqlite3
import logging
from config import DATABASE_FILE

def init_db():
    """Initialize the database and create the prices table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Create the prices table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scrape_time TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        
        conn.commit()
        logging.info("Database initialized successfully")
    except sqlite3.Error as e:
        logging.error(f"Database initialization error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def insert_price(price, scrape_time):
    """Insert a new price record into the database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO prices (price, scrape_time) VALUES (?, ?)",
            (price, scrape_time)
        )
        
        conn.commit()
        logging.info(f"Price {price} at {scrape_time} inserted successfully")
    except sqlite3.Error as e:
        logging.error(f"Error inserting price into database: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_latest_price():
    """Retrieve the most recent price from the database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT price, scrape_time FROM prices ORDER BY id DESC LIMIT 1"
        )
        result = cursor.fetchone()
        
        return result if result else None
    except sqlite3.Error as e:
        logging.error(f"Error retrieving latest price: {e}")
        raise
    finally:
        if conn:
            conn.close()
