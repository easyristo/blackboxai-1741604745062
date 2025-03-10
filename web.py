from flask import Flask, render_template
import sqlite3
from datetime import datetime
import json
from config import DATABASE_FILE

app = Flask(__name__)

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def format_datetime(dt_str):
    """Format datetime string for display."""
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return dt_str

def format_price(price):
    """Format price with 2 decimal places."""
    return f"{price:.2f}" if price is not None else "0.00"

@app.route('/')
def index():
    """Render the main page with price data."""
    conn = get_db_connection()
    try:
        # Get all prices ordered by time
        cursor = conn.execute('''
            SELECT * FROM prices 
            ORDER BY scrape_time DESC 
            LIMIT 48
        ''')
        prices = cursor.fetchall()
        
        # Initialize default values
        current_price = "0.00"
        average_price = "0.00"
        last_update = "Andmed puuduvad"
        timestamps = []
        price_data = []
        
        # Calculate statistics if we have data
        if prices:
            current_price = format_price(prices[0]['price'])
            last_update = format_datetime(prices[0]['scrape_time'])
            
            # Calculate average price
            cursor = conn.execute('SELECT AVG(price) as avg_price FROM prices')
            avg_result = cursor.fetchone()
            average_price = format_price(avg_result['avg_price'])
            
            # Prepare data for the chart (reverse for chronological order)
            chart_data = list(reversed(prices))
            timestamps = [format_datetime(row['scrape_time']) for row in chart_data]
            price_data = [float(format_price(row['price'])) for row in chart_data]

        # Format prices for display in the table
        formatted_prices = []
        for price in prices:
            formatted_prices.append({
                'scrape_time': format_datetime(price['scrape_time']),
                'price': format_price(price['price'])
            })

        return render_template('index.html',
                             current_price=current_price,
                             average_price=average_price,
                             last_update=last_update,
                             prices=formatted_prices,
                             timestamps=json.dumps(timestamps),
                             price_data=json.dumps(price_data))

    except Exception as e:
        return f"Viga andmete laadimisel: {str(e)}", 500
    finally:
        conn.close()

@app.template_filter('format_price')
def format_price_filter(price):
    """Template filter for formatting prices."""
    return format_price(price)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
