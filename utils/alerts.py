import os
import requests

def send_phone_alert(coin, signal):
    api_key = os.getenv("PUSHOVER_API_KEY")
    user_key = os.getenv("PUSHOVER_USER_KEY")
    message = f"{coin}: {signal} signal detected!"
    
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": api_key,
        "user": user_key,
        "message": message
    })