import numpy as np
import pandas as pd

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return sma, upper_band, lower_band

def calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9):
    exp1 = prices.ewm(span=fast_period, adjust=False).mean()
    exp2 = prices.ewm(span=slow_period, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def calculate_volume_analysis(volume, period=20):
    # Volume Moving Average
    volume_ma = volume.rolling(window=period).mean()
    # Volume Spike (current volume > 2 * volume MA)
    volume_spike = volume.iloc[-1] > 2 * volume_ma.iloc[-1]
    return volume_ma, volume_spike

def analyze(coin, prices, volume):
    # Convert price_data and volume_data to pandas Series
    prices = pd.Series(prices)
    volume = pd.Series(volume)
    
    # Calculate RSI
    rsi = calculate_rsi(prices)
    
    # Calculate Bollinger Bands
    sma, upper_band, lower_band = calculate_bollinger_bands(prices)
    
    # Calculate MACD
    macd, signal, histogram = calculate_macd(prices)
    
    # Calculate Volume Analysis
    volume_ma, volume_spike = calculate_volume_analysis(volume)
    
    # Debug print
    print(f"{coin}: RSI = {rsi.iloc[-1]}, Price = {prices.iloc[-1]}, Lower Band = {lower_band.iloc[-1]}, Upper Band = {upper_band.iloc[-1]}")
    print(f"{coin}: MACD = {macd.iloc[-1]}, Signal = {signal.iloc[-1]}, Histogram = {histogram.iloc[-1]}")
    print(f"{coin}: Volume MA = {volume_ma.iloc[-1]}, Volume Spike = {volume_spike}")
    
    # Check for trade setups
    if (
        rsi.iloc[-1] < 30 and  # Oversold
        prices.iloc[-1] < lower_band.iloc[-1] and  # Price below lower band
        macd.iloc[-1] > signal.iloc[-1] and  # MACD above signal line
        histogram.iloc[-1] > 0 and  # MACD histogram positive
        volume_spike  # Volume spike
    ):
        return "LONG"
    elif (
        rsi.iloc[-1] > 70 and  # Overbought
        prices.iloc[-1] > upper_band.iloc[-1] and  # Price above upper band
        macd.iloc[-1] < signal.iloc[-1] and  # MACD below signal line
        histogram.iloc[-1] < 0 and  # MACD histogram negative
        volume_spike  # Volume spike
    ):
        return "SHORT"
    return None