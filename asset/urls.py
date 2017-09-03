from django.conf.urls import url

from  .import views

urlpatterns = [
    url(r'^asset.html$',views.asset_info,name='asset_info'),
    url(r'^asset-add.html$',views.asset_add,name='asset_add'),
    
    url(r'^asset-del.html$',views.asset_del,name='asset_del'),
    url(r'^asset-update-(?P<nid>\d+).html$', views.asset_update, name='asset_update')
]
