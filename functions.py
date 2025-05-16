import httpx
import os
from google import genai
from google.genai import types
import asyncio
from typing import Optional
def extract_current_weather_parameters(json_return):
    weather_dict = {}
    weather_dict['Place'] = json_return.get('location').get('name')
    weather_dict['Region'] = json_return.get('location').get('region')
    weather_dict['Country'] = json_return.get('location').get('country')

    weather_dict['Temperature (deg. C)'] = json_return.get('current').get('temp_c')
    weather_dict['Feels Like (deg. C)'] = json_return.get('current').get('feelslike_c')
    weather_dict['Last Updated'] = json_return.get('current').get('last_updated')

    weather_dict['Condition'] = json_return.get('current').get('condition').get('text')
    weather_dict['Wind Speed(kmph)'] = json_return.get('current').get('wind_kph')
    weather_dict['humidity'] = json_return.get('current').get('humidity')
    weather_dict['Pressure(mb)'] = json_return.get('current').get('pressure_mb')
    weather_dict['Visibility(km)'] = json_return.get('current').get('vis_km')
    weather_dict['Cloud'] = json_return.get('current').get('cloud')
    weather_dict['precip_mm'] = json_return.get('current').get('precip_mm')
    weather_dict['aqi'] = json_return.get('current').get('aqi')
    return weather_dict


async def get_weather_data(city, api_key: Optional[str]) -> dict:
    """
    Fetch weather data from the API for a given city.
    """
    url = "http://api.weatherapi.com/v1/current.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params = {'q': city, 'key':api_key})
        return response.json()



def generate(user_query):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_query),
            ],
        ),
    ]
    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        top_p=0.95,
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
        tools=tools,
        response_mime_type="text/plain",
    )
    r = []
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        r.append(chunk.text)
    response = "".join(r)
    return response


async def generate_async(user_query: str) -> str:
    return await asyncio.to_thread(generate, user_query)
