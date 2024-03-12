from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    groups = models.ManyToManyField('auth.Group', related_name='user_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_set')

    class Meta:
        db_table = 'tb_users'
        verbose_name_plural = '用户'
