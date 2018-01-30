from django.db import models
import random


class codebase(models.Model):
    name = models.CharField(max_length=64, verbose_name='代码名称', null=True,blank=True)

    ps = models.CharField(max_length=1024,verbose_name="备注",null=True,blank=True)
    file = models.FileField(upload_to = 'codebase/%Y%m%d{}'.format(random.randint(0,99999)),verbose_name="代码文件",)


    ctime= models.DateTimeField(auto_now_add=True,null=True,verbose_name='创建时间',blank=True)
    utime = models.DateTimeField(auto_now=True, null=True,verbose_name='更新时间',blank=True)

    class  Meta:
        db_table ="codebase"
        verbose_name="代码"
        verbose_name_plural = '资产管理'

    def __str__(self):
        return self.name

