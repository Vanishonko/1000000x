import time
import json
import logging
import winsound
from dotenv import load_dotenv
from plyer import notification
from utils.data_fetcher import fetch_historical_data
from utils.analyzer import analyze

# Set up logging
logging.basicConfig(
    filename='bot.log',  # Log file name
    level=logging.INFO,  # Log level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

# Load config
with open('config.json') as f:
    config = json.load(f)

def main():
    logging.info("Bot started.")
    while True:
        try:
            # Analyze each coin
            for coin in config['coins']:
                # Fetch historical data (e.g., last 200 seconds of 1-second candles)
                prices, volume = fetch_historical_data(coin, timeframe='1s', limit=200)
                if prices and volume:
                    logging.info(f"Fetched historical data for {coin}: Prices = {prices[-1]}, Volume = {volume[-1]}")
                    
                    # Analyze the data
                    signal = analyze(coin, prices, volume)
                    if signal:
                        logging.info(f"Alert: {signal} for {coin}!")
                        print(f"Alert: {signal} for {coin}!")
                        
                        # Trigger alerts
                        if config['alert_settings']['sound_alarm']:
                            winsound.Beep(2000, 1000)  # Loud beep
                        
                        if config['alert_settings']['desktop_notifications']:
                            notification.notify(
                                title="Trade Alert",
                                message=f"{coin}: {signal} opportunity!",
                                timeout=10
                            )
                else:
                    logging.warning(f"Failed to fetch historical data for {coin}.")
            # Wait 5 seconds before next check
            time.sleep(5)
        
        except Exception as e:
            logging.error(f"Error: {e}")
            print(f"Error: {e}")
            time.sleep(3)  # Retry after 10s

if __name__ == "__main__":
    main()