import os
from datetime import datetime
import requests
from dotenv import load_dotenv
MY_LATITUDE = 41.157944
MY_LONGITUDE = -8.629105

load_dotenv()

api_key = os.getenv("API_KEY") # Get the API key from the .env file
bot_token = os.getenv("BOT_TOKEN") # Get the bot token from the .env file
chat_id = os.getenv("CHAT_ID") # Get the chat ID from the .env file
dir_path = os.path.dirname(os.path.realpath(__file__)) # Get the directory of the current script

def get_12_hour_forecast():
    """
    Get the 12-hour forecast for the current location
    :return:
    """
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={MY_LATITUDE}&lon={MY_LONGITUDE}&appid={api_key}") # get request
    response.raise_for_status() # raise an exception if the HTTP status code is not 200

    data = response.json() # convert the response to a JSON object

    return data["list"][0:12]
def get_code_each_forecast(response):
    """
    Get the weather id and temperature for each forecast
    :param response: API response
    :return: dictionary of weather id and temperature
    """
    info_dict = {}
    for forecast in response: # loop through the forecasts
        weather = forecast["weather"][0]
        weather_id = weather["id"]
        temp_k = forecast["main"]["temp"] # get the temperature in Kelvin
        temp_c = temp_k - 273.15 # convert Kelvin to Celsius

        info_dict[forecast["dt_txt"]] = {"code": weather_id, "temp_c": temp_c}

    return info_dict
def check_weather_conditions(forecasts):
    """
    Generate a message based on the weather conditions
    :param forecasts: dict {timestamp: {"code": int, "temp_c": float}}
    :return: a message string or ""
    """
    conditions = {
        "rain": [],
        "thunder": [],
        "drizzle": [],
        "snow": [],
        "fog": [],
        "heat": []
    }

    for timestamp, data in forecasts.items():
        code = data["code"]
        temp_c = data["temp_c"]
        hour = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")

        if 200 <= code <= 232:
            conditions["thunder"].append(hour)
        elif 300 <= code <= 321:
            conditions["drizzle"].append(hour)
        elif 500 <= code <= 531:
            conditions["rain"].append(hour)
        elif 600 <= code <= 622:
            conditions["snow"].append(hour)
        elif 701 <= code <= 781:
            conditions["fog"].append(hour)

        # calor forte (ajusta o limiar se quiseres)
        if temp_c >= 23:
            conditions["heat"].append((hour, round(temp_c, 1)))

    msg = "*🌤 Weather Alert for the next 12 hours*\n\n"
    added = False

    if conditions["thunder"]:
        added = True
        msg += "⛈ *Thunderstorm expected around:*\n"
        for h in conditions["thunder"]:
            msg += f"• {h}\n"
        msg += "\n"

    if conditions["drizzle"]:
        added = True
        msg += "🌦 *Light rain (drizzle) around:*\n"
        for h in conditions["drizzle"]:
            msg += f"• {h}\n"
        msg += "\n"

    if conditions["rain"]:
        added = True
        msg += "🌧 *Rain expected around:*\n"
        for h in conditions["rain"]:
            msg += f"• {h}\n"
        msg += "\n"

    if conditions["snow"]:
        added = True
        msg += "🌨 *Snow expected around:*\n"
        for h in conditions["snow"]:
            msg += f"• {h}\n"
        msg += "\n"

    if conditions["fog"]:
        added = True
        msg += "🌫 *Fog expected around:*\n"
        for h in conditions["fog"]:
            msg += f"• {h}\n"
        msg += "\n"

    if conditions["heat"]:
        added = True
        msg += "🔥 *High temperatures expected:*\n"
        for h, t in conditions["heat"]:
            msg += f"• {h} — {t}°C\n"
        msg += "\n"

    if not added:
        return ""

    msg += "📩 Stay safe and prepared!"
    return msg
def send_telegram_message(text):
    if not text: # if the text is empty
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"} # create the payload
    requests.post(url, data=payload)

forecast = get_12_hour_forecast() # call the function
weathers = get_code_each_forecast(forecast) # call the function

message = check_weather_conditions(weathers) # call the function
if message: # if the message is not empty
    send_telegram_message(message) # call the function