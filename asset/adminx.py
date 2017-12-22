from   .models import asset,data_centers,system_users,performance,web_history

from djcelery.models import IntervalSchedule, CrontabSchedule,PeriodicTask,WorkerState,TaskState
import xadmin
from xadmin import views



@xadmin.sites.register(views.website.IndexView)
class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "Test Widget",
             "content": "<h3> Welcome to AutoOps </h3><p>Join Online Group: <br/>QQ Qun : </p>"},
            {"type": "chart", "model": "app.accessrecord", "chart": "user_count",
             "params": {"_p_date__gte": "2013-01-08", "p": 1, "_p_date__lt": "2013-01-29"}},
            {"type": "list", "model": "app.host", "params": {"o": "-guarantee_date"}},
        ],
    ]


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True










@xadmin.sites.register(asset)
class MainDashboard(object):
    search_fields = ('network_ip', 'manage_ip',)  ## 定义搜索框以哪些字段可以搜索
    list_display = ('model', 'network_ip', 'manage_ip', 'data_center', 'sn',)  # 每行的显示信息
    list_display_links = ('model',)
    list_filter = ("product_line",)

@xadmin.sites.register(data_centers)
class MainDashboard(object):
    pass




@xadmin.sites.register(system_users)
class MainDashboard(object):
    search_fields = ('name', 'username',)  ## 定义搜索框以哪些字段可以搜索
    list_display = ('name','username',)#  每行的显示信息
    list_display_links = ('name',)
    list_filter = ("product_line",)

@xadmin.sites.register(performance)
class MainDashboard(object):
        pass

@xadmin.sites.register(web_history)
class MainDashboard(object):
         pass


@xadmin.sites.register(IntervalSchedule)
class MainDashboard(object):
    pass


@xadmin.sites.register(CrontabSchedule)
class MainDashboard(object):
    pass





@xadmin.sites.register(PeriodicTask)
class MainDashboard(object):
    pass

@xadmin.sites.register(TaskState)
class MainDashboard(object):
    pass


@xadmin.sites.register(WorkerState)
class MainDashboard(object):
    pass



