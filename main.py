# import libraries that we will use

import requests
from datetime import datetime
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient


# get today's date and time & my name
now = datetime.now()
day_now = now.strftime("%m/%d/%Y")
time_now = now.strftime("%H:%M:%S")
NAME = "Dimitris"

# Api Keys that we will use for Open Weather API along with Boston coordinates
api_key = "*******************"
lat = 42.339905
lon = -71.089890
account_sid = "*******************"
auth_token = "*******************"

# Request to the API to get live weather data
parameters = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()

# Beginning of message with a good morning wish
gm = f"Good morning {NAME}. Here is the weather forcast for today, {day_now}:"
weather = [gm]

# Loop that pulls live weather data from the API for the next 12 hours
for hour in weather_data["hourly"][0:12]:
    id = (hour['weather'][0]["id"])
    main = (hour['weather'][0]["main"])
    description = (hour['weather'][0]["description"])
    hour_now = hour["dt"]
    hour_ft = datetime.fromtimestamp(hour_now).strftime('%H:%M:%S')
    feel_like_kavlin = (hour["feels_like"])
    feel_like_celcius = round(feel_like_kavlin - 273.15, 0)
    # For every hour, data is added on a variable and then to list for the upcoming weather
    message = f" . At: {hour_ft}, weather: {description}, temp: C {feel_like_celcius}"
    weather.append(message)

# Create Message variable that includes components of the list on a new line
message_ready = '\n '.join(weather)

# Send Text Message and print message delivery status
proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
client = Client(account_sid, auth_token, http_client=proxy_client)

message = client.messages \
    .create(
    body=message_ready,
    from_='*******************',
    to='*******************'
print(message.status)
