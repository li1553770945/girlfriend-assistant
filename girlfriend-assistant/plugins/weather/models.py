from tortoise import fields
from tortoise.models import Model


class DefaultCityModel(Model):
    city_name = fields.CharField(max_length=20)    
    user_id = fields.CharField(max_length=20)
    class Meta:
        table = "默认城市"
        table_description = "记录每个用户使用的城市"