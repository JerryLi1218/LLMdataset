from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

class UserBirthday(models.Model):
    name = models.CharField(verbose_name="姓名",max_length=32)
    birthday = models.DateField(verbose_name="生日")

    birthday_choice = (
        (1,"公历生日"),
        (2,"农历生日")
    )

    isLunar = models.SmallIntegerField(verbose_name="生日类型",choices=birthday_choice)