import os
import requests
from dotenv import load_dotenv

load_dotenv()

class MCPServer:
    def __init__(self):
        # ✅ THIS WAS MISSING
        self.api_key = os.getenv("WEATHER_API_KEY")

    def weather(self, city: str):
        if not self.api_key:
            return {"error": "WEATHER_API_KEY not set"}

        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if response.status_code != 200:
                return {
                    "error": data.get("message", "Weather API error"),
                    "status_code": response.status_code
                }

            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"]
            }

        except Exception as e:
            return {"error": str(e)}

    def calculator(self, expression: str):
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return {"error": "Invalid characters"}

        try:
            result = eval(expression, {"__builtins__": {}})
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}
