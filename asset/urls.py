from django.conf.urls import url
from . import api
from  .import views

urlpatterns = [
    url(r'^asset.html$',views.asset_list,name='asset_list'),
    url(r'^asset-add.html$',views.asset_add,name='asset_add'),
    url(r'^asset-del.html$',views.asset_del,name='asset_del'),
    url(r'^asset-all-del.html$',views.asset_all_del,name='asset_all_del'),
    url(r'^asset-detail-(?P<nid>\d+).html$',views.asset_detail,name='asset_detail'),
    url(r'^asset-update-(?P<nid>\d+).html$', views.asset_update, name='asset_update'),
    url(r'^asset-hardware-update.html$', views.asset_hardware_update, name='asset_hardware_update'),
    url(r'^asset-performance-(?P<nid>\d+).html$', views.asset_performance, name='asset_performance'),
    url(r'^asset-webssh.html$', views.asset_web_ssh, name='asset_web_ssh'),
    url(r'^web-history.html$', views.web_historys, name='web_history'),

    url(r'^system-user.html$', views.system_user_list, name='system_user'),
    url(r'^system-user-asset-(?P<nid>\d+).html$', views.system_user_asset, name='system_user_asset'),
    url(r'^system-user-add.html$', views.system_user_add, name='system_user_add'),
    url(r'^system-user-del.html$', views.system_user_del, name='system_user_del'),
    url(r'^system-user-detail-(?P<nid>\d+).html$', views.system_user_detail, name='system_user_detail'),
    url(r'^system-user-update-(?P<nid>\d+).html$', views.system_user_update, name='system_user_update'),
    
    url(r'^api/asset.html$',api.AssetList.as_view(),name='asset_api_list'),
    url(r'^api/asset-detail-(?P<pk>\d+).html$', api.AssetDetail.as_view(), name='asset_api_detail'),
]
