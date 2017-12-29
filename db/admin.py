from django.contrib import admin
from .models import db_users,db_mysql





admin.site.register(db_mysql)
admin.site.register(db_users)