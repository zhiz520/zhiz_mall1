from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Define User Model Class
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name_plural = '用户'
