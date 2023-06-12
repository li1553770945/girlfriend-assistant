from nonebot import get_driver,require,get_bot

from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.adapters.onebot.v11 import Bot as OneBot

require("nonebot_plugin_apscheduler")
require("weather")
from ..weather.weather import get_warn_from_api,get_tody_weather_from_api
from ..weather import get_default_city
from nonebot_plugin_apscheduler import scheduler

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

notify_user = config.shedular_notify_user


async def notify_tody_weather():
    bot = get_bot()
    private_users = notify_user['weather_warn_private']
    for user in private_users:
        city = await get_default_city(user_id=user)
        if city is None:
            return
        weather_msg = "每日天气提醒:"+get_tody_weather_from_api(city)
        msg = Message(MessageSegment.text(weather_msg))    
        await bot.send_private_msg(user_id=int(user),message=msg)

async def notify_weather_warn():
    bot = get_bot()
    private_users = notify_user['weather_warn_private']
    for user in private_users:
        city = await get_default_city(user_id=user)
        if city is None:
            return
        warn = get_warn_from_api(city)
        if warn is None:
            return
        warn = "气象预警提示:"+warn
        msg = Message(MessageSegment.text(warn))    
        await bot.send_private_msg(user_id=int(user),message=msg)

def notify_slq():
    pass

scheduler.add_job(notify_tody_weather,"cron",hour=9)
scheduler.add_job(notify_slq,"cron",hour=9)
scheduler.add_job(notify_weather_warn,"interval",minutes=30)