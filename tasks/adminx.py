

# Register your models here.
from  .models import history,toolsscript
import xadmin

@xadmin.sites.register(history)
class MainDashboard(object):
    pass

@xadmin.sites.register(toolsscript)
class MainDashboard(object):
    pass

