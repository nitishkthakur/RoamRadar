from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import requests
import os
import dotenv
import json
from functions import extract_current_weather_parameters

# Load Secrets from Environment Variables
dotenv.load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

# Start the App
app = FastAPI()

# Mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Make the Weather API call
    weather_response = httpx.get("https://api.weatherapi.com/v1/current.json", params = {'q': 'Thimphu', 'key': API_KEY, 'aqi':'yes'}).json()
    temperature_parameters = extract_current_weather_parameters(weather_response)

    context = {"request": request, "title": "Welcome", "user": "Nitish", "temperature": temperature_parameters['Temperature (deg. C)'], 
               "condition": temperature_parameters['Condition'], "place": temperature_parameters['Place'], 
               "region": temperature_parameters['Region'], "country": temperature_parameters['Country'],
               "feels_like": temperature_parameters['Feels Like (deg. C)'], "last_updated": temperature_parameters['Last Updated'],
               "windspeed": temperature_parameters['Wind Speed(kmph)'], "humidity": temperature_parameters['humidity'],
               "pressure": temperature_parameters['Pressure(mb)'], "visibility": temperature_parameters['Visibility(km)'],
               "cloud": temperature_parameters['Cloud'], "precip_mm": temperature_parameters['precip_mm']}
    
    # Render the HTML template with the context data
    return templates.TemplateResponse("index.html", context)
