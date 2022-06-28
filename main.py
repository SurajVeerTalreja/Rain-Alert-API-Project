import requests
import os
from twilio.rest import Client

OWM_KEY = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
MY_NUMBER = os.environ.get("NUMBER")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")

parameters = {
    "lat": 47.497913,
    "lon": 19.040236,
    "appid": OWM_KEY,
    "exclude": "current,minutely,daily,alerts"
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()

it_will_rain = None

# Using List slicing
weather_data = response.json()["hourly"][:12]
for hour in weather_data:
    if hour["weather"][0]["id"] < 700:
        it_will_rain = True

# Another way
# weather_data = response.json()["hourly"]
# for i in range(0, 13):
#     if weather_data[i]["weather"][0]["id"] < 600:
#     it_will_rain = True


if it_will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body="It will Rain today. Don't forget your Umbrella",
            from_=TWILIO_NUMBER,
            to=MY_NUMBER
        )

    print(message.status)
