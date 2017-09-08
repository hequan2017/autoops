from django.contrib import admin

# Register your models here.

from   .models import login_log


admin.site.register(login_log)
