from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)


def notify_tody_weather():
    pass

def notify_weather_warn():
    pass

def notify_slq():
    pass