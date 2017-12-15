from django.urls  import path

from  .import views

urlpatterns = [
    path('cmd.html', views.cmd, name='cmd'),
    path('sftp.html', views.sftp_file, name='sftp'),
    path('sftp_down.html', views.sftp_down, name='sftp_down'),
    path('tools.html', views.tools, name='tools'),
    path('tools-add.html', views.tools_add, name='tools_add'),
    path('tools-del.html', views.tools_delete, name='tools_delete'),
    path('tools-bulk-del.html', views.tools_bulk_delte, name='tools_bulk_delte'),
    path('tools-update-<int:nid>.html', views.tools_update, name='tools_update'),
    path('tools-script-<int:nid>.html', views.tools_script_get, name='tools_script_get'),
    path('tools-script.html', views.tools_script_post, name='tools_script_post'),
]

app_name="tasks"