import pandas as pd
import pandas_ta as ta  # Fallback if TA-Lib isn’t installed

def analyze(coin, price_data):
    # Example: Check RSI and Bollinger Bands
    rsi = ta.rsi(price_data, length=14)
    bb = ta.bbands(price_data, length=20)
    
    if rsi[-1] < 30 and price_data[-1] < bb['BBL_20_2.0'][-1]:
        return "LONG"
    elif rsi[-1] > 70 and price_data[-1] > bb['BBU_20_2.0'][-1]:
        return "SHORT"
    return None