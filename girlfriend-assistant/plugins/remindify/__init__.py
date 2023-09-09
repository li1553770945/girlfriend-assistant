
from nonebot import get_driver,require,get_bot,on_command

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_tortoise_orm")

from nonebot_plugin_tortoise_orm import add_model
import nonebot_plugin_apscheduler
from nonebot.rule import to_me
from nonebot.adapters import Message,Event
from nonebot.params import CommandArg
from datetime import datetime,timedelta
from nonebot_plugin_apscheduler import scheduler
from .models import RemindModel
from .config import Config
import asyncio
import pytz



global_config = get_driver().config
config = Config.parse_obj(global_config)

remindify = on_command("提醒",rule=to_me(), aliases={"remind","r"}, priority=10, block=True)


add_model("girlfriend-assistant.plugins.remindify.models")




async def notify():
    while True:
        try:
            bot = get_bot()
            break
        except Exception as err:
            print(err)
            await asyncio.sleep(1)
    while (remind := await RemindModel.filter(have_notified=False).order_by("remind_time").first()) is not None:
        delta_time = remind.remind_time - datetime.now(pytz.timezone('Asia/Shanghai'))
        if delta_time.total_seconds() < 10:
            msg = f"小助手温馨提示:\n提醒id:{remind.id}\n时间:{remind.remind_time.strftime('%Y-%m-%d %H:%M:%S')}\n内容:{remind.remark}"

            if remind.group_id != "": # 群聊中创建的提醒
                await bot.send_group_message(target=int(remind.group_id),message_chain=[{"type": "At","target": int(remind.user_id)},{ "type":"Plain", "text":msg }])
            else:
                await bot.send_friend_message(target=int(remind.user_id),message_chain=[{ "type":"Plain", "text":msg }])

            remind.have_notified = True
            await remind.save()
        else:
            scheduler.add_job(notify, "date", run_date= remind.remind_time,id="remind_job",replace_existing=True)
            break

scheduler.add_job(notify, "date", run_date=datetime.now(),id="remind_job",replace_existing=True)

print(123)


help_str="""使用帮助:
/r [动作] [参数]
动作包括:add,remove,list,help
对应的参数为:
1.list和help不需要额外参数
2.add [时间] [事项]
时间可以为: "2021-02-13 13:14"、"13:14"、"13"三种.分别代表:日期时间，时间（默认今天）,几分钟之后
3.remove [提醒id]
如果私聊发给助手，则提醒会私聊发给发送者。如果在群里@助手，则提醒会在群里@发送者。
查询提醒，对每个人来说，私聊查询会显示所有提醒，在群里@只会显示本群本人创建的提醒。
"""

async def add_remind(user_id,remind_time:datetime,remark,group_id):
    remind = await RemindModel.create(user_id=user_id,remind_time=remind_time,remark=remark,group_id=group_id)
    await notify()
    result = f"成功添加{remind_time.strftime('%Y-%m-%d %H:%M:%S')}的提醒,id为{remind.id}"
    if group_id != "":
        result += ",提醒将在本群发送"
    return result

async def list_remind(user_id,group_id):
    remind_list = await RemindModel.filter(user_id=user_id,have_notified=False).all().order_by("remind_time")
    if len(remind_list) == 0:
        if group_id != "":
            return "当前暂无未完成提醒,当前仅显示您在本群创建的提醒"
        return "当前暂无未完成提醒"
    result = ""
    if group_id != "":
        result += "当前仅显示您在本群创建的提醒\n"
    for index,remind in enumerate(remind_list):
        if group_id != "" and group_id != remind.group_id: # 从群里发送仅显示本群的提醒
            continue
        result = result + str(index+1) + "、" + str(remind)
        if group_id == "" and remind.group_id != "": # 从群里创建，但是私聊查询的，会在每个提醒后加上一句话
            result += f",在群{remind.group_id}中创建"
        if index != len(remind_list) - 1:
            result += "\n"
    return result

async def remove_remind(user_id,remind_id):
    remind = await RemindModel.filter(user_id=user_id,id=remind_id).first()
    if remind is None:
        return "未查询到对应id的提醒"
    else:
        await remind.delete()
        return "删除成功"

def parse_datetime(input_str): # 把时间字符串，格式化成datetime
    try:
        if '-' in input_str:
            # 如果字符串包含'-'，则解析为具体日期时间
            dt = datetime.strptime(input_str, "%Y-%m-%d %H:%M")
        elif ':' in input_str:
            # 如果字符串包含':'，则解析为时间（日期为今天）
            current_date = datetime.now().date()
            time_str = input_str.split(':')
            hours = int(time_str[0])
            minutes = int(time_str[1])
            dt = datetime(current_date.year, current_date.month, current_date.day, hours, minutes)
        else:
            # 否则，解析为当前时间的几分钟之后
            minutes = int(input_str)
            dt = datetime.now() + timedelta(minutes=minutes)

        return dt
    except ValueError:
        raise ValueError("输入字符串不是有效的日期时间格式")
    
async def handle_command(user_id,params,group_id): # 处理命令
    params = params.split(' ')
    if params[0] in ("add","a"):
        if len(params) != 3 and len(params) != 4:
            return "添加失败,参数错误,使用参数h查看帮助"
        
        if len(params) == 4: # 日期和时间中间有空格，会被分成连个元素
            params = [params[0],params[1] + " " + params[2] ,params[3]]

        try:
            remind_time = parse_datetime(params[1])
        except:
            return "添加失败,参数错误,使用参数h查看帮助"
        
        result = await add_remind(user_id,remind_time,params[2],group_id)
        return result


    elif params[0] in ("list","l"):
        result = await list_remind(user_id,group_id)
        return result
    
    elif params[0] in ("remove","r"):
        if len(params) == 1:
            return "删除失败,请在remove命令后添加' {提醒id}'(包括空格)"
        
        try:
            remind_id = int(params[1])
        except:
            return "删除失败,无法获取正确提醒id"
        result = await remove_remind(user_id,remind_id)
        return result
    
    elif params[0] in ("help","h","帮助"):
        return help_str

    else:
        return "无法解析的命令，使用h命令查看帮助"

@remindify.handle()
async def handle_function(event:Event,args: Message = CommandArg(),):
    params = args.extract_plain_text()
    user_id = event.get_user_id()

    msg_type = event.type
    if msg_type == "GroupMessage":
        group_id = str(event.sender.group.id)
    else:
        group_id = ""

    result = await handle_command(user_id,params,group_id)
    print(result)
    await remindify.finish(result)