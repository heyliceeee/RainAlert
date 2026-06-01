import json
import os
import requests
from dotenv import load_dotenv
MY_LATITUDE = 41.157944
MY_LONGITUDE = -8.629105

load_dotenv()

api_key = os.getenv("API_KEY") # Get the API key from the .env file
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
    Get the weather id and description for each forecast
    :param response: API response
    :return: dictionary of weather id and description
    """
    info_dict = {}
    for forecast in response: # loop through the forecasts
        weather = forecast["weather"][0]
        weather_id = weather["id"]

        info_dict[forecast["dt_txt"]] = weather_id

    return info_dict
def check_rain(forecasts):
    """
    Check if any forecast has rain
    :param forecasts: dictionary of weather time and code
    :return: true if any forecast has rain, false otherwise
    """
    for timestamp, weather_code in forecasts.items(): # loop through the forecasts
        if weather_code < 700: # rain
            return "Bring an umbrella!"
    return ""

forecast = get_12_hour_forecast() # call the function
weathers = get_code_each_forecast(forecast) # call the function
print(check_rain(weathers))