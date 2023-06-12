from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message,MessageSegment,Event
from nonebot import require
from .weather import get_tody_weather_from_api,get_now_weather_from_api,get_warn_from_api
from .models import DefaultCityModel
require("nonebot_plugin_tortoise_orm")
from nonebot_plugin_tortoise_orm import add_model
import asyncio

add_model("girlfriend-assistant.plugins.weather.models")

weather = on_command("天气",rule=to_me(), aliases={"weather", "查天气"}, priority=10, block=True)


async def get_default_city(**kwargs)->Message:
    user_id = kwargs['user_id']
    if city := await DefaultCityModel.filter(user_id=user_id).first():
        return city.city_name
    else:
        return None
    

async def set_default_city(**kwargs)->Message:
    city_name = kwargs['city']
    user_id = kwargs['user_id']
    if city_name is None:
        return Message(MessageSegment.text(f"设置失败，使用“/天气 帮助”获取帮助"))
    else:
        if city := await DefaultCityModel.filter(user_id=user_id).first():
            city.city_name = city_name
            await city.save()
        else:
            await DefaultCityModel.create(city_name = city_name,user_id=user_id)
        return Message(MessageSegment.text(f"设置成功"))
    
def get_help(**kwargs)->Message:
    help_message = "使用方法：/天气 [命令] [城市]\n \
        可选命令有：\n \
        1.今日天气 [城市] ：查询对应城市的今日天气，不加城市则为默认城市  \n \
        2.实时天气 [城市] ：查询对应城市的今日天气，不加城市则为默认城市 \n \
        3.预警 [城市] : 查询对应城市的预警，不加城市则为默认城市 \n \
        4.设置默认天气[城市] : 设置默认城市 \n \
        5.帮助 : 显示帮助"
    
    return Message(MessageSegment.text(help_message))

def get_now_weather(**kwargs)->Message:
    city = kwargs['city']
    if city is None:
        return Message(MessageSegment.text(f"当前未设置默认城市"))
    return Message(MessageSegment.text(get_now_weather_from_api(city)))

def get_tody_weather(**kwargs)->Message:
    city = kwargs['city']
    if city is None:
        return Message(MessageSegment.text(f"当前未设置默认城市"))
    return Message(MessageSegment.text(get_tody_weather_from_api(city)))

def get_warn(**kwargs)->Message:
    city = kwargs['city']
    if city is None:
        return Message(MessageSegment.text(f"当前未设置默认城市"))
    warn = get_warn_from_api(city)
    if warn is None:
        warn = "当前城市暂无预警"
    return Message(MessageSegment.text(warn))


async def handle_params(params:str,user_id:str):
    params = params.split(" ")
    if params[0] == "" or params[0] == "今日":
        params[0] = "今日天气"
    if params[0] == "实时":
        params[0] = "实时天气"
    if len(params) == 1:
        params.append(await get_default_city(user_id=user_id)) 
    return params

@weather.handle()
async def handle_function(event:Event,args: Message = CommandArg(),):
    params = args.extract_plain_text()
    user_id = event.get_user_id()
    params = await handle_params(params,user_id)
    command_dict = {
        "帮助": get_help,
        "今日天气": get_tody_weather,
        "实时天气":get_now_weather,
        "预警": get_warn,
        "设置默认城市": set_default_city
    }

    if params[0] in command_dict:
        func =  command_dict[params[0]]
        if asyncio.iscoroutinefunction(func):
            result = await func(city=params[1],user_id=user_id)
        else:
            result = func(city=params[1],user_id=user_id)
        await weather.finish(result)
    else:
        await weather.finish("无法解析参数，使用 \"/天气 帮助\"来获取帮助")
