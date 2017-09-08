from django.contrib import admin
from   .models import asset,product_lines,data_centers,system_users,performance,web_history
from guardian.admin import GuardedModelAdmin


class AssetAdmin(GuardedModelAdmin):
    search_fields = ('network_ip','manage_ip',) ## 定义搜索框以哪些字段可以搜索
    list_display = ('model','network_ip','manage_ip','data_center','sn',)#  每行的显示信息
    list_display_links = ('model',)
    list_filter = ("product_line",)


admin.site.register(asset,AssetAdmin)
admin.site.register(product_lines)
admin.site.register(data_centers)
admin.site.register(system_users)
admin.site.register(performance)
admin.site.register(web_history)