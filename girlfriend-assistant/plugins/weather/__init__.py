from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message,Event
from nonebot import require
from .weather import get_tody_weather_from_api,get_now_weather_from_api,get_warn_from_api
from .models import DefaultCityModel
require("nonebot_plugin_tortoise_orm")
from nonebot_plugin_tortoise_orm import add_model

from .notify import notify_weather
from nonebot_plugin_apscheduler import scheduler

add_model("girlfriend-assistant.plugins.weather.models")

weather = on_command("天气",rule=to_me(), aliases={"weather", "查天气","w"}, priority=10, block=True)


async def get_default_city(user_or_group_id,is_group)->str:
    if city := await DefaultCityModel.filter(user_or_group_id=user_or_group_id,is_group=is_group).first():
        return city.city_name
    else:
        return None
    

async def set_default_city(city_name:str,user_or_group_id:str,is_group:bool)->str:
    if city_name is None:
        return f"设置失败，使用“/天气 帮助”获取帮助"
    else:
        if city := await DefaultCityModel.filter(user_or_group_id=user_or_group_id,is_group=is_group).first():
            city.city_name = city_name
            await city.save()
        else:
            await DefaultCityModel.create(city_name = city_name,user_or_group_id=user_or_group_id,is_group=is_group)
        return "设置成功"
    
def get_help()->str:
    help_message = "使用方法：/天气 [命令] [城市]\n \
        可选命令有：\n \
        1.今日天气 [城市] ：查询对应城市的今日天气，不加城市则为默认城市  \n \
        2.实时天气 [城市] ：查询对应城市的今日天气，不加城市则为默认城市 \n \
        3.预警 [城市] : 查询对应城市的预警，不加城市则为默认城市 \n \
        4.设置默认天气 [城市] : 设置默认城市 \n \
        5.天气提醒 ['开启'或'关闭'] \
        6.帮助 : 显示帮助"
    
    return help_message

def get_now_weather(city)->str:
    if city is None:
        return "当前未设置默认城市"
    return get_now_weather_from_api(city)

def get_tody_weather(city):
    if city is None:
        return f"当前未设置默认城市"
    return get_tody_weather_from_api(city)

def get_warn(city)->str:
    if city is None:
        return "当前未设置默认城市"
    warn = get_warn_from_api(city)
    if warn is None:
        warn = f"{city}暂无气象预警"
    return warn


async def handle_params(params:str,user_or_group_id:str,is_group:bool):
    
    return params


async def set_remind(status:str,user_or_group_id:str,is_group:bool):
    if status != "开启"  and status != "关闭":
        return "设置失败，参数只能是'开启'或'关闭'"
    if obj := await DefaultCityModel.filter(user_or_group_id=user_or_group_id,is_group=is_group).first():
        if status == "开启":
            obj.need_notify = True
            await obj.save()
            return "已开启提醒"
        else:
            obj.need_notify = False
            await obj.save()
            return "已关闭提醒"
    else:
        return "未设置默认城市，无法开启提醒，请先设置默认城市"
    
@weather.handle()
async def handle_function(event:Event,args: Message = CommandArg(),):
    params = args.extract_plain_text()
    user_id = event.get_user_id()

    msg_type = event.type
    if msg_type == "GroupMessage":
        is_group = True
        group_id = event.sender.group.id
    else:
        is_group = False

    params = params.split(" ")
    if len(params) == 1: # 如果没有写默认城市，使用默认城市
        if is_group:
            params.append(await get_default_city(user_or_group_id=group_id,is_group=is_group)) 
        else:
            params.append(await get_default_city(user_or_group_id=user_id,is_group=is_group)) 

    command = params[0]
    if command in ("","今日","今日天气","tody","t"):
        result = get_tody_weather(city=params[1])
    elif command in ("实时天气","实时"):
        result = get_now_weather(city=params[1])
    elif command in ("预警","warn","w"):
        result = get_warn(city=params[1])
    elif command in ("设置默认城市"):
        msg_type = event.type
        if is_group == True:
            result = await set_default_city(city_name=params[1],user_or_group_id=group_id,is_group=True)
        else:
            result = await set_default_city(city_name=params[1],user_or_group_id=user_id,is_group=False)
    elif command in ("天气提醒"):
        if is_group == True:
            result = await set_remind(status=params[1],user_or_group_id=group_id,is_group=True)
        else:
            result = await set_remind(status=params[1],user_or_group_id=user_id,is_group=False)
    elif command in ("帮助","help"):
        result = get_help()
    else:
        result = "无法解析参数，使用 \"/天气 帮助\"来获取帮助"
    await weather.finish(result)


scheduler.add_job(notify_weather, 'cron', hour=8,replace_existing=True)