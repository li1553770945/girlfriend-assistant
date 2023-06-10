from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from .weather import get_tody_weather_from_api,get_now_weather_from_api,get_warn_from_api


weather = on_command("天气",rule=to_me(), aliases={"weather", "查天气"}, priority=10, block=True)


def get_default_city()->Message:
    return "南京"

def set_default_city(city:str)->Message:
    if city is None:
        return Message(MessageSegment.text(f"设置失败，使用“/天气 帮助”获取帮助"))
    else:
        return Message(MessageSegment.text(f"{city}的预警是XXX"))
    
def get_help(city:str)->Message:
    help_message = "使用方法：/天气 [命令] [城市]\n \
        可选命令有：\n \
        1.今日天气 [城市] ：查询对应城市的今日天气，不加城市则为默认城市  \n \
        2.实时天气 [城市] ：查询对应城市的今日天气，不加城市则为默认城市 \n \
        3.预警 [城市] : 查询对应城市的预警，不加城市则为默认城市 \n \
        4.设置默认天气[城市] : 设置默认城市 \n \
        5.帮助 : 显示帮助"
    
    return Message(MessageSegment.text(help_message))

def get_now_weather(city:str)->Message:
    if city is None:
        return Message(MessageSegment.text(f"当前未设置默认城市"))
    return Message(MessageSegment.text(get_now_weather_from_api(city)))

def get_tody_weather(city:str)->Message:
    if city is None:
        return Message(MessageSegment.text(f"当前未设置默认城市"))
    return Message(MessageSegment.text(get_tody_weather_from_api(city)))

def get_warn(city:str)->Message:
    if city is None:
        return Message(MessageSegment.text(f"当前未设置默认城市"))
    return Message(MessageSegment.text(get_warn_from_api(city)))





@weather.handle()
async def handle_function(args: Message = CommandArg()):
    params = args.extract_plain_text()
    params = params.split(" ")
    print(params)
    if params[0] == "":
        params[0] = "今日天气"
    if len(params) == 1:
        params.append(get_default_city()) 

    command_dict = {
        "帮助": get_help,
        "今日天气": get_tody_weather,
        "实时天气":get_now_weather,
        "预警": get_warn,
        "设置默认城市": set_default_city
    }

    if params[0] in command_dict:
        result = command_dict[params[0]](params[1])
        await weather.finish(result)
    else:
        await weather.finish("无法解析参数，使用 \"/天气 帮助\"来获取帮助")
