Here are the steps to create a simple Python app using Flask-RESTful for the specified functionality:

---

### Step 1: Set Up the Environment
1. **Install Required Packages**:
   Install Flask and Flask-RESTful:
   ```bash
   pip install flask flask-restful requests python-dotenv
   ```

2. **Create the Project Structure**:
   ```
   flask_app/
   ├── app.py                # Main application file
   ├── .env                  # Environment variables
   ├── requirements.txt      # Package dependencies
   └── README.md             # Optional documentation
   ```

3. **Set Up `.env` File**:
   Add the API key for OpenWeatherMap to the `.env` file:
   ```env
   $env:OPENWEATHERMAP_API_KEY=your_api_key_here
   ```

---

### Step 2: Implement the Flask Application
Create `app.py` with the following code:

```python
import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Initialize Flask and Flask-RESTful
app = Flask(__name__)
api = Api(app)

# Define the resource class
class WeatherResource(Resource):
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

# Add the resource to the API
api.add_resource(WeatherResource, '/current-weather')

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
```

---

### Step 3: Test the Application
1. **Start the Flask App**:
   Run the app:
   ```bash
   python app.py
   ```

2. **Send a Request to the API**:
   Use `curl`, Postman, or a browser to test the API:
   ```bash
   curl "http://127.0.0.1:5000/current-weather?lat=35.6895&lon=139.6917"
   ```

3. **Expected Response**:
   If the request is successful, you will receive:
   ```json
   {
       "success": True,
       "data": {
           "coord": {"lon": 139.6917, "lat": 35.6895},
           "weather": [...],
           ...
       }
   }
   ```

   If there’s an error:
   ```json
   {
       "success": False,
       "error": "Missing 'lat' or 'lon' query parameters"
   }
   ```

---

### Step 4: Freeze Requirements
Generate a `requirements.txt` file:
```bash
pip freeze > requirements.txt
```

---

### Step 5: Deploy the Application (Optional)
For deployment, consider using platforms like Heroku, AWS, or Azure, and ensure to set the `OPENWEATHERMAP_API_KEY` as an environment variable in the deployment settings.

