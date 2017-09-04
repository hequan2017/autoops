from django.conf.urls import url

from  .import views

urlpatterns = [
    url(r'^asset.html$',views.asset_list,name='asset_list'),
    url(r'^asset-add.html$',views.asset_add,name='asset_add'),
    url(r'^asset-del.html$',views.asset_del,name='asset_del'),
    url(r'^asset-all-del.html$',views.asset_all_del,name='asset_all_del'),
    url(r'^asset-detail-(?P<nid>\d+).html$',views.asset_detail,name='asset_detail'),
    url(r'^asset-update-(?P<nid>\d+).html$', views.asset_update, name='asset_update'),

    url(r'^system-user.html$', views.system_user_list, name='system_user'),
    url(r'^system-user-asset-(?P<nid>\d+).html$', views.system_user_asset, name='system_user_asset'),
    url(r'^system-user-add.html$', views.system_user_add, name='system_user_add'),
    url(r'^system-user-del.html$', views.system_user_del, name='system_user_del'),
    url(r'^system-user-detail-(?P<nid>\d+).html$', views.system_user_detail, name='system_user_detail'),
    url(r'^system-user-update-(?P<nid>\d+).html$', views.system_user_update, name='system_user_update')
]
