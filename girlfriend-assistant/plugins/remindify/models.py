from tortoise import fields
from tortoise.models import Model


class RemindModel(Model):
    id = fields.IntField(pk=True)
    remark = fields.CharField(max_length=20)    
    remind_time = fields.DatetimeField()
    user_id = fields.CharField(max_length=20)
    have_notified=fields.BooleanField(default=False)
    group_id = fields.CharField(max_length=20,default="")
    class Meta:
        table = "提醒"
        table_description = "记录每个用户的提醒"
        indexes=("user_id","remind_time")

    def __str__(self) -> str:
        end = "......" if len(self.remark) > 20 else ""
        return f"提醒id:{self.id},时间:{self.remind_time.strftime('%Y-%m-%d %H:%M')},事项:{self.remark[0:20] + end}"