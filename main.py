from fastapi import FastAPI, Request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import requests
import os
import dotenv
import json
from functions import extract_current_weather_parameters, get_weather_data
from google import genai
from google.genai import types
from functions import generate
from pydantic import BaseModel
import  diskcache as dc
import markdown
import logging
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)   # or INFO
logger.info('Started')
class SearchInput(BaseModel):
    query: str
cache = dc.Cache("cache")  # 1 kb cache
logger.info('Cache created')
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


# Get weather


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, city:str = "Thimphu"):
    # Make the Weather API call
    #weather_response = httpx.get("https://api.weatherapi.com/v1/current.json", params = {'q': 'Thimphu', 'key': API_KEY, 'aqi':'yes'}).json()
    temperature_parameters = await get_weather_data(city, API_KEY)
    temperature_parameters = extract_current_weather_parameters(temperature_parameters)
    #temperature_parameters = extract_current_weather_parameters(weather_response)

    context = {"request": request, "title": "RoamRadar", "user": "Nitish", "temperature": temperature_parameters['Temperature (deg. C)'], 
               "condition": temperature_parameters['Condition'], "place": temperature_parameters['Place'], 
               "region": temperature_parameters['Place'] + ', ' + temperature_parameters['Region'] + ', ' + temperature_parameters['Country'], "country": temperature_parameters['Country'],
               "feels_like": temperature_parameters['Feels Like (deg. C)'], "last_updated": temperature_parameters['Last Updated'],
               "windspeed": temperature_parameters['Wind Speed(kmph)'], "humidity": temperature_parameters['humidity'],
               "pressure": temperature_parameters['Pressure(mb)'], "visibility": temperature_parameters['Visibility(km)'],
               "cloud": temperature_parameters['Cloud'], "precip_mm": temperature_parameters['precip_mm']}
    
    context_minus_request = {k: v for k, v in context.items() if k != "request"}
    cache.set("weather_data", context_minus_request, expire=60*60*24)
    logger.info('Cache Set')

    # Render the HTML template with the context data
    return templates.TemplateResponse("index.html", context)


@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    # Get the search query from the form
    #form_data = data
    print(query)
    search_query = query
    
    # Call the generate function to get the response
    response = generate(search_query)
    logger.info('Getting from cache')
    weather_data_ = cache.get("weather_data")
    logger.info(f'Loaded from cache: {weather_data_}')
    print(weather_data_)
    weather_data_['response'] = response
    weather_data_['request'] = request
    
    # Render the HTML template with the response data
    r#eturn templates.TemplateResponse("index.html", weather_data_)
    return templates.TemplateResponse("templates/llm_response.html", {"request": request, "response": response})
