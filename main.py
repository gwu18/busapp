import os
import googlemaps
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import requests

import webbrowser
import threading

def open_browser():
    """Opens the frontend in a browser after Flask starts."""
    import time
    time.sleep(2)  # Give Flask a moment to start
    webbrowser.open("https://super-orbit-7x76vwwj44vhwpj6-5000.app.github.dev/send_location")

# Run Flask and open the browser in a separate thread


# load_dotenv()
# api_key = os.getenv('maps_api_key')
# maps = googlemaps.Client(key=api_key)

app = Flask(__name__, static_folder="static", template_folder="templates")
GOOGLE_MAPS_API_KEY = "AIzaSyD8GEn022ffV5ZsDpWabcQapaTd-k8EHOM"  # Replace with your API Key
CORS(app)

# Serve index.html when the backend starts
@app.route("/")
def home():
    return render_template("index.html")  # Loads index.html automatically

@app.route("/send_location", methods=["GET", "POST"])
def receive_location():
    print("🔹 Received Headers:", request.headers)  # Print all headers
    print("🔹 Content-Type Received:", request.content_type)  # Print received Content-Type
    print("🔹 Raw Body Received:", request.data)  # Print raw request body

    if request.content_type != "application/json":  # ✅ Ensure JSON request
        return jsonify({"error": "Unsupported Media Type, use application/json"}), 415  # 415 = Unsupported Media Type

    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude and longitude:
        # Get address using Google Maps Reverse Geocoding API
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_MAPS_API_KEY}"
        response = requests.get(url)
        address_data = response.json()

        if address_data["status"] == "OK":
            address = address_data["results"][0]["formatted_address"]
        else:
            address = "Address not found"

        return jsonify({
            "latitude": latitude,
            "longitude": longitude,
            "address": address
        })
    
    return jsonify({"error": "Invalid location data"}), 400

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    app.run(debug=True, host="0.0.0.0", port=5000)

# curl -X POST https://super-orbit-7x76vwwj44vhwpj6-5000.app.github.dev/send_location \
#      -H "Content-Type: application/json" \
#      -d '{"latitude": 37.7749, "longitude": -122.4194}'
