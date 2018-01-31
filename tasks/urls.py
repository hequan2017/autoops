from django.urls  import path

from  .import views

urlpatterns = [
    path('cmd.html', views.cmd, name='cmd'),

    path('tools.html', views.ToolsListAll.as_view(), name='tools'),
    path('tools-add.html', views.tools_add, name='tools_add'),
    path('tools-del.html', views.tools_delete, name='tools_delete'),
    path('tools-bulk-del.html', views.tools_bulk_delte, name='tools_bulk_delte'),
    path('tools-update-<int:nid>.html', views.tools_update, name='tools_update'),
    path('tools-script-<int:nid>.html', views.tools_script_get, name='tools_script_get'),
    path('tools-script.html', views.tools_script_post, name='tools_script_post'),


    path('Inception.html', views.Inception, name='Inception'),
    path('Inception-exe.html', views.Inception_exe, name='Inception_exe'),
    path('Inception-rb.html', views.Inception_rb, name='Inception_rb'),
    path('Inception-query.html', views.Inception_query, name='Inception_query'),
    path('Inception-query-databases.html', views.Inception_query_databases, name='Inception_query_databases'),
]

app_name="tasks"