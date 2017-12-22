from  .models import db_mysql,db_users
import xadmin

@xadmin.sites.register(db_mysql)
class MainDashboard(object):
    pass

@xadmin.sites.register(db_users)
class MainDashboard(object):
    pass

