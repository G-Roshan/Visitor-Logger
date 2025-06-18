from flask import Flask, request
import requests
from datetime import datetime
import pytz
import csv

app = Flask(__name__)

@app.route('/')
def log_visitor():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        data = response.json()
        city = data.get('city', 'N/A')
        country = data.get('country_name', 'N/A')
        timezone_str = data.get('timezone', 'UTC')

        tz = pytz.timezone(timezone_str)
        timestamp = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    except:
        city, country, timezone_str = 'N/A', 'N/A', 'UTC'
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    with open('visitors.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ip, city, country, timezone_str, timestamp])

    return f"Visitor from {city}, {country} logged at {timestamp}"
