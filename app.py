import os
import re
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from dotenv import load_dotenv
import requests
import traceback

# Load environment variables from .env file
load_dotenv()

# Initialize Flask and Flask-RESTful
app = Flask(__name__)
api = Api(app)

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# # Define the resource class
# class WeatherResource(Resource):
def get(self):
    try:
        # Fetch API key from environment variable
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            return {"success": False, "error": "API key not found in environment variables"}, 500

        # Get latitude and longitude from query parameters
        lat = request.args.get('lat')
        lon = request.args.get('lon')

        if not lat or not lon:
            return {"success": False, "error": "Missing 'lat' or 'lon' query parameters"}, 400

        # Call OpenWeatherMap API
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        response = requests.get(weather_url, params={"lat": lat, "lon": lon, "appid": api_key})

        if response.status_code == 200:
            weather_data = response.json()
            return {"success": True, "data": weather_data}, 200
        else:
            return {"success": False, "error": response.json().get("message", "Failed to fetch weather data")}, response.status_code

    except Exception as e:
        return {"success": False, "error": str(e)}, 500

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
    except Exception:
        traceback.print_exc()
        return None, None

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Extract user input
    intent = req['queryResult']['intent']['displayName']

    # Handle Greeting Intent
    if intent == "Greeting":
        greeting_response = (
            "Hi! I am a weather bot. What location would you like to know the current weather for? "
            "Use the standard latitude and longitude format, which for New York City, for example, would be: 40°42′46″N 74°0′22″W."
        )
        return jsonify({"fulfillmentText": greeting_response})
            
    if intent == "GetWeather":
        user_input = req['queryResult']['queryText']
        lat, lon = parse_lat_lon(user_input)

        if lat is None or lon is None:
            return jsonify({"fulfillmentText": "Invalid latitude and longitude format. Please try again."})

        # Call OpenWeatherMap API
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        response = requests.get(weather_url, params={"units": "metric", "lat": lat, "lon": lon, "appid": OPENWEATHERMAP_API_KEY})

        if response.status_code == 200:
            weather_data = response.json()
            weather_main = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            weather_message = f"The weather for the given location is {weather_main} with a temperature of {temperature}ºC."
            return jsonify({"fulfillmentText": weather_message})
        else:
            return jsonify({"fulfillmentText": "Failed to fetch weather data. Please try again later."})

    return jsonify({"fulfillmentText": "I'm not sure how to handle that request."})


# # Add the resource to the API
# api.add_resource(WeatherResource, '/current-weather')

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)