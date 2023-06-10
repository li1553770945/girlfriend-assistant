import requests
from nonebot import get_driver
from .config import Config


global_config = get_driver().config
print(global_config)
config = Config.parse_obj(global_config)

base_url = config.hefeng_base_url
key = config.hefeng_key

def get_tody_weather_from_api(city:str):
    url = f"https://geoapi.qweather.com/v2/city/lookup?location={city}&key={key}&number=1"
    result = requests.get(url)

    city_code = 0
    city_name = ""
    if result.status_code != 200:
        return f"查询地理位置失败,http状态码:{result.status_code}"
    
    response = result.json()
    if response['code'] != "200":
        return f"查询地理位置失败,API状态码:{response['code']}"
    
    city_code = response['location'][0]['id']
    city_name = response['location'][0]['name']

    url = f"https://{base_url}/v7/weather/3d?key={key}&location={city_code}"
    result = requests.get(url)
    if result.status_code != 200:
        return f"查询天气失败,http状态码:{result.status_code}"
    
    response = result.json()
    if response['code'] != "200":
        return f"查询天气失败,API状态码:{response['code']}"
    
    weather = response['daily'][0]
    message = f"{city_name}{weather['fxDate']}白天{weather['textDay']},夜间{weather['textNight']},最高气温{weather['tempMax']}°C,最低气温{weather['tempMin']}°C,风力{weather['windScaleDay']}级,预计今日降水量{weather['precip']}毫米，紫外线强度指数{weather['uvIndex']}"
    return message



def get_now_weather_from_api(city:str):
    url = f"https://geoapi.qweather.com/v2/city/lookup?location={city}&key={key}&number=1"
    result = requests.get(url)

    city_code = 0
    city_name = ""
    if result.status_code != 200:
        return f"查询地理位置失败,http状态码:{result.status_code}"
    
    response = result.json()
    if response['code'] != "200":
        return f"查询地理位置失败,API状态码:{response['code']}"
    
    city_code = response['location'][0]['id']
    city_name = response['location'][0]['name']

    url = f"https://{base_url}/v7/weather/now?key={key}&location={city_code}"
    result = requests.get(url)
    if result.status_code != 200:
        return f"查询天气失败,http状态码:{result.status_code}"
    
    response = result.json()
    if response['code'] != "200":
        return f"查询天气失败,API状态码:{response['code']}"
    
    weather = response['now']
    message = f"{city_name}当前天气{weather['text']},{weather['windDir']}{weather['windScale']}级,温度{weather['temp']}°C,体感温度{weather['feelsLike']}°C,相对湿度{weather['humidity']}%,当前小时累计降水量{weather['precip']}毫米"
    return message


def get_warn_from_api(city:str):
    url = f"https://geoapi.qweather.com/v2/city/lookup?location={city}&key={key}&number=1"
    result = requests.get(url)

    city_code = 0
    city_name = ""
    if result.status_code != 200:
        return f"查询地理位置失败,http状态码:{result.status_code}"
    
    response = result.json()
    if response['code'] != "200":
        return f"查询地理位置失败,API状态码:{response['code']}"
    
    city_code = response['location'][0]['id']
    city_name = response['location'][0]['name']

    url = f"https://{base_url}/v7/warning/now?key={key}&location={city_code}"
    result = requests.get(url)
    if result.status_code != 200:
        return f"查询预警失败,http状态码:{result.status_code}"
    
    response = result.json()
    if response['code'] != "200":
        return f"查询预警失败,API状态码:{response['code']}"
    
    warns = response['warning']
    messages = ""
    for warn in warns:

        sender = warn['sender'] if warn['sender'] != "" else "未知发布者"

        message = f"{sender}发布{warn['title']}:{warn['text']}\n"
        messages  += message

    return messages if messages != "" else f"{city_name}暂无气象预警信息"


    
        