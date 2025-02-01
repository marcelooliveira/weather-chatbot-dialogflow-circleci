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
    
def get_weather_for_coords_http_response(location, lat, lon):
    # Call OpenWeatherMap API
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(weather_url, params={"units": "metric", "lat": lat, "lon": lon, "appid": OPENWEATHERMAP_API_KEY})

    if response.status_code == 200:
        weather_data = response.json()
        weather_main = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        weather_message = f"The weather for {location} is {weather_main} with a temperature of {temperature}ºC."
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

    
def get_coords(city, state, country):
    # Call OpenWeatherMap API
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={OPENWEATHERMAP_API_KEY}"
    print(geo_url)
    response = requests.get(geo_url)

    geo_data = response.json()
    return geo_data

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
        
        query_result = req_body['queryResult']
        intent = query_result['intent']['displayName']
        print(f"intent: {intent}")

        if intent == "GetWeatherByCoordinates":
            query_text = query_result['queryText']
            print(f"query_text: {json.dumps(req_body['queryResult'])}")
            lat, lon = parse_lat_lon(query_text)
            if lat is None or lon is None:
                return func.HttpResponse(
                    "Invalid latitude and longitude format. Please try again.",
                    status_code=200
                )

            location_http_response = None

            location = f"lat {lat:.2f} lon {lon:.2f}"

            weather_response = get_weather_for_coords_http_response(location, lat, lon)

            return weather_response

        if intent == "GetCountryName":
            # Extracting values from the dictionary
            geo_city = None
            geo_state = None
            geo_country = None

            print(query_result["outputContexts"])

            # Loop through outputContexts to find the context containing all three parameters
            for context in query_result["outputContexts"]:
                params = context.get("parameters", {})
                if "geo-city" in params and "geo-state" in params and "geo-country" in params:
                    geo_city = params["geo-city.original"]
                    geo_state = params["geo-state.original"]
                    geo_country = params["geo-country.original"]
                    break

            # Print the extracted variables
            print("Geo-City:", geo_city)
            print("Geo-State:", geo_state)
            print("Geo-Country:", geo_country)

            coords = get_coords(geo_city, geo_state, geo_country)
            lat = coords[0]["lat"]
            lon = coords[0]["lon"]

            location = f"{geo_city} / {geo_state} / {geo_country}"

            weather_response = get_weather_for_coords_http_response(location, lat, lon)

            return weather_response

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
