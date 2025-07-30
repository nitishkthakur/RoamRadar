from fastapi import FastAPI, Request      # FastAPI-specific imports
from fastapi import Form                  # FastAPI-specific
from fastapi.responses import HTMLResponse  # FastAPI-specific
from fastapi.staticfiles import StaticFiles  # FastAPI-specific
from fastapi.templating import Jinja2Templates # FastAPI-specific
import os
import dotenv
from functions import extract_current_weather_parameters, get_weather_data
from functions import generate_async   # Note: generate_async is async/threading-related
from pydantic import BaseModel
import  diskcache as dc
import markdown
import logging

# Set some settings




logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)   # or INFO
logger.info('Started')




class SearchInput(BaseModel):     # Pydantic model for type validation, FastAPI-friendly
    query: str

cache = dc.Cache("cache")  # Diskcache for caching, not async, but thread-safe
logger.info('Cache created')

# Load Secrets from Environment Variables
dotenv.load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
if API_KEY is None:
    raise RuntimeError("WEATHER_API_KEY environment variable not set")
API_URL = "https://api.openai.com/v1/chat/completions"

# Start the App
app = FastAPI()          # FastAPI-specific: create the main app instance

# Mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")   # FastAPI-specific static mounting

# Setup Jinja templates
templates = Jinja2Templates(directory="templates")   # FastAPI/Jinja integration

# -------- ASYNC HANDLER: GET WEATHER & MAIN PAGE --------
@app.get("/", response_class=HTMLResponse)     # FastAPI-specific route decorator
async def read_root(request: Request, city:str = "Thimphu"):   # ASYNC HANDLER!
    # Make the Weather API call
    #weather_response = httpx.get("...")       # If you used httpx.get here, you’d need to await and make it async!
    temperature_parameters = await get_weather_data(city, API_KEY)    # ASYNC: await non-blocking I/O call
    temperature_parameters = extract_current_weather_parameters(temperature_parameters)

    context = {"request": request, "title": "RoamRadar", "user": "Nitish", "temperature": temperature_parameters['Temperature (deg. C)'],
               "condition": temperature_parameters['Condition'], "place": temperature_parameters['Place'],
               "region": temperature_parameters['Place'] + ', ' + temperature_parameters['Region'] + ', ' + temperature_parameters['Country'],
               "country": temperature_parameters['Country'],
               "feels_like": temperature_parameters['Feels Like (deg. C)'], "last_updated": temperature_parameters['Last Updated'],
               "windspeed": temperature_parameters['Wind Speed(kmph)'], "humidity": temperature_parameters['humidity'],
               "pressure": temperature_parameters['Pressure(mb)'], "visibility": temperature_parameters['Visibility(km)'],
               "cloud": temperature_parameters['Cloud'], "precip_mm": temperature_parameters['precip_mm']}

    context_minus_request = {k: v for k, v in context.items() if k != "request"}
    cache.set("weather_data", context_minus_request, expire=60*60*24)
    logger.info('Cache Set')

    # Render the HTML template with the context data (FastAPI template response)
    return templates.TemplateResponse("index.html", context)    # FastAPI-specific

# -------- ASYNC HANDLER: WEATHER PARTIAL FOR HTMX --------
@app.get("/weather-cards", response_class=HTMLResponse)    # FastAPI route decorator
async def read_weather(request: Request, city:str = "Thimphu"):    # ASYNC HANDLER!
    temperature_parameters = await get_weather_data(city, API_KEY)    # ASYNC: await!
    temperature_parameters = extract_current_weather_parameters(temperature_parameters)

    context = {"request": request, "title": "RoamRadar", "user": "Nitish", "temperature": temperature_parameters['Temperature (deg. C)'],
               "condition": temperature_parameters['Condition'], "place": temperature_parameters['Place'],
               "region": temperature_parameters['Place'] + ', ' + temperature_parameters['Region'] + ', ' + temperature_parameters['Country'],
               "country": temperature_parameters['Country'],
               "feels_like": temperature_parameters['Feels Like (deg. C)'], "last_updated": temperature_parameters['Last Updated'],
               "windspeed": temperature_parameters['Wind Speed(kmph)'], "humidity": temperature_parameters['humidity'],
               "pressure": temperature_parameters['Pressure(mb)'], "visibility": temperature_parameters['Visibility(km)'],
               "cloud": temperature_parameters['Cloud'], "precip_mm": temperature_parameters['precip_mm']}

    context_minus_request = {k: v for k, v in context.items() if k != "request"}
    cache.set("weather_data", context_minus_request, expire=60*60*24)
    logger.info('Cache Set')

    # Render the HTML template with the context data (FastAPI template response)
    return templates.TemplateResponse("weather_partial.html", context)   # FastAPI-specific

# -------- ASYNC HANDLER: LLM QUERY (NON-BLOCKING via THREAD) --------
@app.post("/search", response_class=HTMLResponse)      # FastAPI route decorator
async def search(request: Request, query: str = Form(...)):    # ASYNC HANDLER!
    print(query)
    search_query = query

    # Call the generate function to get the response (non-blocking: runs in separate thread)
    response = await generate_async(search_query)      # ASYNC/TRHEADING: this is an async wrapper over the blocking LLM API call

    logger.info('Getting from cache')
    weather_data_ = cache.get("weather_data")
    logger.info(f'Loaded from cache: {weather_data_}')
    print(weather_data_)
    weather_data_['response'] = response
    weather_data_['request'] = request

    # Convert response to markdown
    markdown_response = markdown.markdown(response)
    # Render the HTML template with the response data
    #return templates.TemplateResponse("index.html", weather_data_)
    #return templates.TemplateResponse("templates/llm_response.html", {"request": request, "response": response})
    #return HTMLResponse(f"<div class='p-2 border rounded'>{markdown_response }</div>")
    return HTMLResponse(f"<div class='markdown-body'>{markdown_response }</div>")  # FastAPI r esponse
