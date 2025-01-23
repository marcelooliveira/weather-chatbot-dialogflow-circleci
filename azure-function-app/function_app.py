import azure.functions as func
import logging
import os
import re
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Helper function to parse standard latitude and longitude format
def parse_lat_lon(user_input):
    try:
        # Example input: "40°42′46″N 74°0′22″W"
        pattern = r"(\d+)°(\d+)′(\d+)″([NS])\s+(\d+)°(\d+)′(\d+)″([EW])"
        match = re.match(pattern, user_input)
        if not match:
            return None, None

        lat = int(match.group(1)) + int(match.group(2)) / 60 + int(match.group(3)) / 3600
        lon = int(match.group(5)) + int(match.group(6)) / 60 + int(match.group(7)) / 3600

        if match.group(4) == "S":
            lat = -lat
        if match.group(8) == "W":
            lon = -lon

        return lat, lon
    except:
        return None, None

# Azure Function App definition
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="webhook")
def webhook(req: func.HttpRequest) -> func.HttpResponse:

    if OPENWEATHERMAP_API_KEY is None:
        return "OPENWEATHERMAP_API_KEY must be provided!"

    logging.info('Processing webhook request.')

    try:
        # Parse the incoming request JSON
        req_body = req.get_json()
        
        intent = req_body['queryResult']['intent']['displayName']
        query_text = req_body['queryResult']['queryText']

        print(f"intent: {intent}")
        print(f"query_text: {json.dumps(req_body['queryResult'])}")

        # Handle "Greeting" intent
        if intent == "Greeting":
            return func.HttpResponse(
                "Hi! I am a weather bot. What location would you like to know the current weather for? "
                "Use the standard latitude and longitude format, which for Paris, for example, would be: 48°51′24″N 2°21′8″E.",
                status_code=200
            )

        # Handle "GetWeather" intent
        if intent == "GetWeather":
            lat, lon = parse_lat_lon(query_text)
            if lat is None or lon is None:
                return func.HttpResponse(
                    "Invalid latitude and longitude format. Please try again.",
                    status_code=200
                )

            # Call OpenWeatherMap API
            weather_url = "https://api.openweathermap.org/data/2.5/weather"
            response = requests.get(weather_url, params={"units": "metric", "lat": lat, "lon": lon, "appid": OPENWEATHERMAP_API_KEY})

            if response.status_code == 200:
                weather_data = response.json()
                weather_main = weather_data["weather"][0]["description"]
                temperature = weather_data["main"]["temp"]
                weather_message = f"The weather for the given location is {weather_main} with a temperature of {temperature}ºC."
                return func.HttpResponse(
                    json.dumps({
                        "fulfillmentText": weather_message
                    }),
                    status_code=200
                )                
            else:
                return func.HttpResponse(
                    "Failed to fetch weather data. Please try again later.",
                    status_code=500
                )

        # Default response for unhandled intents
        return func.HttpResponse(
            "I'm not sure how to handle that request.",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse(
            "An error occurred while processing the request.",
            status_code=500
        )
