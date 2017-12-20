
from   .models import login_log
import xadmin

@xadmin.sites.register(login_log)
class MainDashboard(object):
    pass

