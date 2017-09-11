from django.db import models


__all__ = ['login_log']

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

