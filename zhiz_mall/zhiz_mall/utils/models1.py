from django.db import models


class BaseModel(models.Model):
    '''为模型补充字段'''

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间') 
    update_time = models.DateField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        abstarct = True # 说明是抽象类， 模型迁移时不会创建BaseModel表

# print(secrets.token_hex(32))