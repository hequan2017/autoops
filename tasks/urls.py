from django.conf.urls import url

from  .import views

urlpatterns = [
    url(r'^cmd.html$', views.cmd, name='cmd'),
    url(r'^history.html$', views.historys, name='history'),
    url(r'^tools.html$', views.tools, name='tools'),
    url(r'^tools-add.html$', views.tools_add, name='tools_add'),
    url(r'^tools-del.html$', views.tools_delete, name='tools_delete'),
    url(r'^tools-bulk-del.html$', views.tools_bulk_delte, name='tools_bulk_delte'),
    url(r'^tools-update-(?P<nid>\d+).html$', views.tools_update, name='tools_update'),
    url(r'^tools-script-(?P<nid>\d+).html$', views.tools_script_get, name='tools_script_get'),
    url(r'^tools-script.html$', views.tools_script_post, name='tools_script_post'),
]
