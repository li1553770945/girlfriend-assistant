from nonebot import get_driver,require,get_bot
from nonebot.adapters import Message

require("nonebot_plugin_apscheduler")
require("weather")

from nonebot_plugin_apscheduler import scheduler
from ..weather.weather import get_tody_weather_from_api
from ..weather import get_default_city

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
        msg = weather_msg
        await bot.send_private_msg(user_id=int(user),message=msg)



