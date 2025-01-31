import time
import json
import winsound
from dotenv import load_dotenv
from plyer import notification
from utils.data_fetcher import fetch_prices
from utils.analyzer import analyze
from utils.alerts import send_phone_alert

# Load config
with open('config.json') as f:
    config = json.load(f)

def main():
    while True:
        try:
            # Fetch prices for all coins
            prices = fetch_prices(config['coins'])
            
            # Analyze each coin
            for coin in config['coins']:
                signal = analyze(coin, prices[coin])
                if signal:
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
                    
                    # Send phone alert (Pushover example)
                    if config['alert_settings']['pushover']['enabled']:
                        send_phone_alert(coin, signal)
            
            # Wait 60 seconds before next check
            time.sleep(60)
        
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)  # Retry after 10s

if __name__ == "__main__":
    main()