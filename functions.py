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