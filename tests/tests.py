# test_weather_extraction.py
import pytest
from functions import extract_current_weather_parameters

# ========================================
# 1. UNIT TESTING WITH PYTEST
# ========================================
"""
PURPOSE: Test specific scenarios with known inputs and expected outputs
WHAT IT CATCHES: Logic errors, expected behavior validation, edge cases you think of
"""

class TestExtractWeatherParametersUnit:

    def test_extract_weather_parameters_complete_data(self):
        """Test with complete, valid weather API response"""
        # Arrange - Create realistic weather API response
        weather_response = {
            "location": {
                "name": "London",
                "region": "City of London, Greater London",
                "country": "United Kingdom"
            },
            "current": {
                "temp_c": 15.0,
                "feelslike_c": 13.2,
                "last_updated": "2025-05-30 14:30",
                "condition": {"text": "Partly cloudy"},
                "wind_kph": 12.9,
                "humidity": 72,
                "pressure_mb": 1013.0,
                "vis_km": 10.0,
                "cloud": 25,
                "precip_mm": 0.0,
                "aqi": 42
            }
        }

        # Act
        result = extract_current_weather_parameters(weather_response)

        # Assert - Verify each field is extracted correctly
        assert result['Place'] == "London"
        assert result['Region'] == "City of London, Greater London"
        assert result['Country'] == "United Kingdom"
        assert result['Temperature (deg. C)'] == 15.0
        assert result['Feels Like (deg. C)'] == 13.2
        assert result['Last Updated'] == "2025-05-30 14:30"
        assert result['Condition'] == "Partly cloudy"
        assert result['Wind Speed(kmph)'] == 12.9
        assert result['humidity'] == 72
        assert result['Pressure(mb)'] == 1013.0
        assert result['Visibility(km)'] == 10.0
        assert result['Cloud'] == 25
        assert result['precip_mm'] == 0.0
        assert result['aqi'] == 42

    def test_extract_weather_parameters_missing_nested_field(self):
        """Test behavior when nested fields are missing - reveals a bug!"""
        weather_response = {
            "location": {
                "name": "Paris",
                "region": "Ile-de-France",
                "country": "France"
            },
            "current": {
                "temp_c": 20.0,
                "feelslike_c": 18.5,
                "last_updated": "2025-05-30 15:00",
                # Missing 'condition' field - this will cause AttributeError!
                "wind_kph": 8.5,
                "humidity": 65,
                "pressure_mb": 1015.2,
                "vis_km": 12.0,
                "cloud": 15,
                "precip_mm": 0.2,
                "aqi": 35
            }
        }

        # This test will FAIL and reveal the function is fragile!
        with pytest.raises(AttributeError):
            extract_current_weather_parameters(weather_response)

    def test_extract_weather_parameters_zero_values(self):
        """Test with zero/minimal values"""
        weather_response = {
            "location": {"name": "Desert", "region": "", "country": "Nowhere"},
            "current": {
                "temp_c": 0, "feelslike_c": 0, "last_updated": "",
                "condition": {"text": ""}, "wind_kph": 0, "humidity": 0,
                "pressure_mb": 0, "vis_km": 0, "cloud": 0, "precip_mm": 0, "aqi": 0
            }
        }

        result = extract_current_weather_parameters(weather_response)
        assert result['Temperature (deg. C)'] == 0
        assert result['Region'] == ""
        assert result['Condition'] == ""
