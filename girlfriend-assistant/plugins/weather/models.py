from tortoise import fields
from tortoise.models import Model


class DefaultCityModel(Model):
    id = fields.IntField(pk=True)
    city_name = fields.CharField(max_length=20)   
    is_group = fields.BooleanField()
    user_or_group_id = fields.CharField(max_length=20)
    need_notify = fields.BooleanField(default=False)
    class Meta:
        table = "默认城市"
        table_description = "记录每个用户使用的默认城市以及是否需要提醒"
        indexes=("user_or_group_id","need_notify")

