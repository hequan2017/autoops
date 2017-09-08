from django.db import models
from asset.models import product_lines
from django.contrib.auth.models import User, UserManager
from django.conf import settings


__all__ = ['name','login_log']


class name(models.Model):
    ROLE_CHOICES = (
        ('测试机', ('测试机')),
        ('云主机', ('云主机')),
    )


    users = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.CharField(choices=ROLE_CHOICES, max_length=12, null=True, blank=True, verbose_name=('用户权限'))


    class Meta:
        db_table = "name"
        verbose_name = "用户扩展"
        verbose_name_plural = '用户扩展'

    def __str__(self):
        return self.status



class login_log(models.Model):
    user = models.CharField(max_length=32, verbose_name='登录用户', null=True)
    ip = models.GenericIPAddressField(verbose_name='用户地址', null=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        db_table = "login_log"
        verbose_name = "平台登录"
        verbose_name_plural = '平台登录'

    def __str__(self):
        return self.user

