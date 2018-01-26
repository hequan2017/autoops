from   .models import asset,data_centers,system_users,performance,web_history
from db.models import db_mysql,db_user
from library.models import librarys
from names.models import login_log
from  release.models import codebase
from  tasks.models import toolsscript,history
from djcelery.models import IntervalSchedule, CrontabSchedule,PeriodicTask,WorkerState,TaskState
import xadmin
from xadmin import views





@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True



@xadmin.sites.register(asset)
class assets(object):
    search_fields = ('network_ip', 'manage_ip',)  ## 定义搜索框以哪些字段可以搜索
    list_display = ('model', 'network_ip', 'manage_ip', 'data_center', 'sn',)  # 每行的显示信息
    list_display_links = ('model',)
    list_filter = ("product_line",)

@xadmin.sites.register(data_centers)
class datacenters(object):
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


@xadmin.sites.register(db_mysql)
class MainDashboard(object):
    pass
@xadmin.sites.register(db_user)
class MainDashboard(object):
    pass
@xadmin.sites.register(librarys)
class MainDashboard(object):
    pass
@xadmin.sites.register(login_log)
class MainDashboard(object):
    pass
@xadmin.sites.register(codebase)
class MainDashboard(object):
    pass
@xadmin.sites.register(toolsscript)
class MainDashboard(object):
    pass

@xadmin.sites.register(history)
class MainDashboard(object):
    pass

