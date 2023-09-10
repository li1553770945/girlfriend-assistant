
from nonebot import get_bot

from nonebot_plugin_apscheduler import scheduler
from .models import DefaultCityModel
from .weather import get_tody_weather_from_api
import asyncio


async def notify_weather():
    while True:
        try:
            bot = get_bot()
            break
        except Exception as err:
            print(err)
            await asyncio.sleep(1)
    notify_list = await DefaultCityModel.filter(need_notify=True).all()
    for notify in notify_list:
        msg = f"每日天气提醒:"+get_tody_weather_from_api(notify.city_name)
        if notify.is_group: # 群聊中创建的提醒
            await bot.send_group_message(target=int(notify.user_or_group_id),message_chain=[{ "type":"Plain", "text":msg }])
        else:
            await bot.send_friend_message(target=int(notify.user_or_group_id),message_chain=[{ "type":"Plain", "text":msg }])



