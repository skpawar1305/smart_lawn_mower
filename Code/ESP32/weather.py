# Python program to find current
# weather details of any city
# using openweathermap api

# import required modules
import json
import urequests as requests

class Weather():
    def current_weather(self):
        # Enter your API key here
        api_key = ""

        # Co-ordinates
        latitude = ""
        longitude = ""

        # weather_url variable to store url
        weather_url = "http://api.openweathermap.org/data/2.5/weather?lat=" + latitude + "&lon=" + longitude + "&appid=" + api_key

        # get method of requests module
        # return response object
        response = requests.get(weather_url)

        # json method of response object
        # convert json format data into
        # python format data
        x = response.json()

        # store the value of "main"
        # key in variable y
        y = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather = y[0]["main"]

        # print following values
        # print(weather_description)
                
        return weather
