
import requests
from langchain.tools import tool,ToolRuntime
api_key="3d7e7564fe6c69744e41efcfc5e72607"


@tool
def get_wether(City:str)->str:
    """Mendapatkan informasi cuaca berdasarkan nama kota."""
    try:
        data=requests.get("https://geocoding-api.open-meteo.com/v1/search",params={"name":City,"count":1}).json()
        lat=data['results'][0]['latitude']
        long=data['results'][0]["longitude"]
        wether_raw=requests.get("https://api.open-meteo.com/v1/forecast",params={'latitude':lat,'longitude':long,"current_weather": True}).json()
        cuaca=wether_raw["current_weather"]
        return f"kota:{City}\nsuhu:{cuaca['temperature']}°C\nangin:{cuaca['windspeed']}"   
    except :
        print('mungkini ada kesalahan di apii'),