import nonebot
from nonebot.adapters.mirai2 import Adapter as MIRAI2Adapter 
# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(MIRAI2Adapter)

# 在这里加载插件
nonebot.load_builtin_plugins("echo")  # 内置插件
nonebot.load_plugins("girlfriend-assistant\plugins") 

if __name__ == "__main__":
    nonebot.run()