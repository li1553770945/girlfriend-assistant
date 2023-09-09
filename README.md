# girlfriend-assistant

使用[NoneBot2](https://github.com/nonebot/nonebot2)实现的一些生活和女朋友有关的消息辅助服务。


## 已经实现功能

1. 天气相关

使用方法：“/天气 帮助”

2. 定时提醒。

使用方法：“/提醒 帮助”

## 需要添加的配置项

HEFENG_KEY=[和风天气APIKEY](https://console.qweather.com/#/console)

HEFENG_BASE_URL=[和风天气API基础URL](https://dev.qweather.com/docs/api/weather/weather-now/) (免费用户与付费用户不同)

2. MIRAI 相关

VERIFY_KEY=xxx # MiraiApiHttp2 配置文件里的 token

MIRAI_HOST=127.0.0.1  # MiraiApiHttp2 的 ip

MIRAI_PORT=5700 # MiraiApiHttp2 的端口

MIRAI_QQ=["xxxxxxx"]  # Mirai 上已经登录的 qq 号

SUPERUSERS=[]  # nonebot2 的超管(也可理解为bot的主人什么的)

3. 数据库相关

db_url=sqlite://data//db.sqlite3

