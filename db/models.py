from django.db import models
from django.contrib.auth.models import Group



class db_mysql(models.Model):

    hostname = models.CharField(max_length=64, verbose_name='数据库名字',unique=True)
    ip = models.GenericIPAddressField(verbose_name='IP', null=True,blank=True)
    port = models.IntegerField(verbose_name='端口', null=True,blank=True,default="3306")
    model = models.CharField(max_length=128, verbose_name='数据库型号', null=True,blank=True)


    db_user = models.ForeignKey(to="db_user", to_field='id', on_delete=models.SET_NULL, null=True,
                                    verbose_name='数据库登陆用户', blank=True)


    product_line =  models.ForeignKey(to=Group,to_field='id',on_delete=models.SET_NULL,verbose_name='产品线',null=True)
    data_center = models.ForeignKey(to="asset.data_centers", to_field='id', on_delete=models.SET_NULL, null=True,
                                    verbose_name='数据中心',blank=True)



    is_active = models.BooleanField(default=True, verbose_name=('是否启用'))



    ps = models.CharField(max_length=1024,verbose_name="备注",null=True,blank=True)

    ctime= models.DateTimeField(auto_now_add=True,null=True,verbose_name='创建时间',blank=True)
    utime = models.DateTimeField(auto_now=True, null=True,verbose_name='更新时间',blank=True)


    class  Meta:
        db_table ="db_mysql"
        verbose_name="数据库管理"
        verbose_name_plural = '数据库管理'
        permissions = {
            ('read_db_mysql',u"只读数据库资产"),
            ('task_db_mysql', u"执行数据库资产"),
        }


    def __str__(self):
        return self.hostname



class  db_user(models.Model):

    name = models.CharField(max_length=128, unique=True,verbose_name='名称')
    username = models.CharField(max_length=64,null=True,blank=True, default='root',verbose_name=('登陆用户'))
    password =  models.CharField(max_length=255, blank=True,null=True,verbose_name=('登陆密码'))
    product_line = models.ForeignKey(to=Group, to_field='id', on_delete=models.SET_NULL, verbose_name='产品线',null=True)
    ps = models.CharField(max_length=1024,verbose_name="备注",null=True,blank=True)
    ctime= models.DateTimeField(auto_now_add=True,null=True,verbose_name='创建时间',blank=True)
    utime = models.DateTimeField(auto_now=True, null=True,verbose_name='更新时间',blank=True)



    def __str__(self):
        return self.name

    class  Meta:
        db_table ="db_user"
        verbose_name="数据库登陆用户"
        verbose_name_plural = '数据库登陆用户'
        permissions = {
            ('read_db_user',u"只读系统登陆用户"),
        }

