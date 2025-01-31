import ccxt

def fetch_prices(coins):
    exchange = ccxt.binance()
    prices = {}
    for coin in coins:
        try:
            ticker = exchange.fetch_ticker(f"{coin}/USDT")
            prices[coin] = ticker['last']  # Latest price
        except Exception as e:
            print(f"Failed to fetch {coin}: {e}")
            prices[coin] = None
    return prices