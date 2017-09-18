from django.db import models
import random



class librarys(models.Model):
    title = models.CharField(max_length=128, verbose_name='标题', null=True,unique=True)
    content = models.TextField(max_length=1024000,verbose_name="内容",null=True,blank=True)

    file = models.FileField(upload_to = '%Y%m%d{}'.format(random.randint(0,99999)),null=True,blank=True,default=None)
    classify = models.CharField(max_length=128, verbose_name='分类', null=True,blank=True)
    creater  = models.CharField(max_length=128, verbose_name='创建人', null=True,blank=True)
    ctime= models.DateTimeField(auto_now_add=True,null=True,verbose_name='创建时间',blank=True)
    utime = models.DateTimeField(auto_now=True, null=True,verbose_name='更新时间',blank=True)



    class  Meta:
        db_table ="librarys"
        verbose_name="技术文库"
        verbose_name_plural = '技术文库'
        permissions = {
            ('read_librarys',u"只读技术文库"),
        }
