import requests
from django.core.management.base import BaseCommand
from stocks.models import StockData
from datetime import datetime
from django.db.utils import IntegrityError
import time

API_KEY = 'YD94ZVG7UAB1JMNO'  
BASE_URL = 'https://www.alphavantage.co/query'

class Command(BaseCommand):
    help = 'Fetch stock data from Alpha Vantage API and store in the database'

    def __init__(self):
        super().__init__()
        self.MAX_RETRIES = 5
        self.RETRY_DELAY = 60  # 60 seconds between retries

    def fetch_with_retry(self, url):
        """Helper method to handle API calls with retry logic"""
        retry_count = 0  # Move retry_count here to reset for each fetch attempt
        
        while retry_count < self.MAX_RETRIES:
            try:
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Log the entire response for debugging
                    self.stdout.write(f"API Response: {data}")  # Updated line
                    
                    # Check for API error messages
                    if "Error Message" in data:
                        self.stdout.write(self.style.ERROR(f"API Error: {data['Error Message']}"))
                        return None
                    
                    # Check for rate limit message
                    if "Note" in data and "call frequency" in data["Note"]:
                        self.stdout.write(self.style.WARNING(f"Rate limit reached. Waiting {self.RETRY_DELAY} seconds..."))
                        time.sleep(self.RETRY_DELAY)
                        retry_count += 1
                        continue
                    
                    return data
                    
                elif response.status_code == 429:  # Too Many Requests
                    self.stdout.write(self.style.WARNING(f"Rate limit hit. Retrying in {self.RETRY_DELAY} seconds..."))
                    time.sleep(self.RETRY_DELAY)
                    retry_count += 1
                    
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to fetch data: HTTP {response.status_code}"))
                    return None
                    
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Network error: {str(e)}"))
                time.sleep(self.RETRY_DELAY)
                retry_count += 1

        self.stdout.write(self.style.ERROR(f"Max retries ({self.MAX_RETRIES}) exceeded"))
        return None



    def handle(self, *args, **kwargs):
        symbol = 'AAPL'  # You can parameterize this later
        function = 'TIME_SERIES_DAILY'  # Use the free endpoint
        
        self.stdout.write(self.style.SUCCESS(f"Starting data fetch for {symbol}..."))
        
        url = f'{BASE_URL}?function={function}&symbol={symbol}&apikey={API_KEY}&outputsize=full'
        
        data = self.fetch_with_retry(url)
        if not data:
            return

        time_series = data.get('Time Series (Daily)', {})
        
        success_count = 0
        error_count = 0
        skip_count = 0

        for date, values in time_series.items():
            try:
                stock_entry = StockData(
                    symbol=symbol,
                    timestamp=datetime.strptime(date, '%Y-%m-%d'),
                    open_price=values['1. open'],
                    close_price=values['4. close'],
                    high_price=values['2. high'],
                    low_price=values['3. low'],
                    volume=values['5. volume']  # Change from '6. volume' to '5. volume'
                )
                stock_entry.save()
                success_count += 1
                
                # Print progress every 100 records
                if success_count % 100 == 0:
                    self.stdout.write(f"Processed {success_count} records...")
                
            except IntegrityError:
                skip_count += 1
                self.stdout.write(self.style.WARNING(f'Skipping duplicate entry for {symbol} on {date}'))
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'Error saving data for {symbol} on {date}: {e}'))

        # Print final statistics
        self.stdout.write(self.style.SUCCESS(f"""
        Fetch completed for {symbol}:
        - Successfully saved: {success_count} records
        - Skipped duplicates: {skip_count} records
        - Errors: {error_count} records
        """))

