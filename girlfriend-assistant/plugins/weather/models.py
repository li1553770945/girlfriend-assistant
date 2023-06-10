from tortoise import fields
from tortoise.models import Model


class CityForm(Model):
    city = fields.CharField()    

    class Meta:
        table = "城市"
        table_description = "记录当前使用的城市"