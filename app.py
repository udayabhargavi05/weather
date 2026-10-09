
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city):
    try:
        location_response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )
        location_response.raise_for_status()
        locations = location_response.json().get("results", [])

        if not locations:
            return None, f"City '{city}' was not found."

        place = locations[0]

        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,is_day,precipitation,"
                    "weather_code,wind_speed_10m"
                ),
                "daily": (
                    "weather_code,temperature_2m_max,"
                    "temperature_2m_min,precipitation_probability_max"
                ),
                "timezone": "auto",
                "forecast_days": 7
            },
            timeout=10
        )
        weather_response.raise_for_status()
        data = weather_response.json()

        return {
            "city": place["name"],
            "country": place.get("country", ""),
            "current": data["current"],
            "daily": data["daily"]
        }, None

    except (requests.RequestException, ValueError, KeyError) as error:
        app.logger.warning("Weather lookup failed: %s", error)
        return None, "Weather data is temporarily unavailable."


def weather_description(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Heavy thunderstorm with hail"
    }
    return descriptions.get(code, "Unknown conditions")


@app.template_filter("weather_description")
def describe_weather(code):
    return weather_description(code)


@app.route("/")
def home():
    city = request.args.get("city", "Hyderabad").strip()
    weather, error = get_weather(city) if city else (None, "Enter a city name.")
    return render_template(
        "index.html", weather=weather, error=error, city=city
    )


@app.route("/forecast")
def forecast():
    city = request.args.get("city", "Hyderabad").strip()
    weather, error = get_weather(city) if city else (None, "Enter a city name.")
    return render_template(
        "forecast.html", weather=weather, error=error, city=city
    )


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
