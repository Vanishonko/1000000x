import ccxt

def fetch_prices(coins):
    exchange = ccxt.binance()
    prices = {}
    for coin in coins:
        try:
            # Fetch latest price
            ticker = exchange.fetch_ticker(f"{coin}/USDT")
            prices[coin] = ticker['last']  # Latest price
        except Exception as e:
            print(f"Failed to fetch {coin}: {e}")
            prices[coin] = None
    return prices

def fetch_historical_data(coin, timeframe='1s', limit=200):
    exchange = ccxt.binance()
    try:
        # Fetch historical candles
        candles = exchange.fetch_ohlcv(f"{coin}/USDT", timeframe=timeframe, limit=limit)
        # Extract closing prices and volume
        prices = [candle[4] for candle in candles]  # Index 4 is the closing price
        volume = [candle[5] for candle in candles]  # Index 5 is the volume
        return prices, volume
    except Exception as e:
        print(f"Failed to fetch historical data for {coin}: {e}")
        return None, None   