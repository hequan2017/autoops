from django.contrib import admin
from .models import db_user,db_mysql
from guardian.admin import GuardedModelAdmin

class MysqlAdmin(GuardedModelAdmin):
   pass

class UsersAdmin(GuardedModelAdmin):
    pass


admin.site.register(db_mysql,MysqlAdmin)
admin.site.register(db_user,UsersAdmin)