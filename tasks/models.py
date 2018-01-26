from django.db import models


class history(models.Model):
    root = models.CharField(max_length=32, verbose_name='用户', null=True)
    ip = models.GenericIPAddressField(verbose_name='IP',null=True)
    port = models.CharField(max_length=32,verbose_name='端口',null=True)
    cmd = models.CharField(max_length=128,verbose_name='命令',null=True)
    user = models.CharField(max_length=32,verbose_name='操作者',null=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class  Meta:
        db_table ="history"
        verbose_name="历史命令"
        verbose_name_plural = '历史命令'


    def __str__(self):
        return self.ip





class toolsscript(models.Model):
    TOOL_RUN_TYPE = (
        (0, 'shell'),
        (1, 'python'),
        # (2, 'yml'),
    )

    name = models.CharField(max_length=255, verbose_name='工具名称',unique=True)
    tool_script = models.TextField(verbose_name='脚本',null=True, blank=True)
    tool_run_type = models.IntegerField(choices=TOOL_RUN_TYPE, verbose_name='脚本类型', default=0)
    comment = models.TextField(verbose_name='工具说明', null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    utime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "toolsscript"
        verbose_name = "工具"
        verbose_name_plural = verbose_name



