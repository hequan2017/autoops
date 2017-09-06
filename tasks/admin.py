from django.contrib import admin

# Register your models here.
from  .models import history,tools_script



admin.site.register(history)
admin.site.register(tools_script)