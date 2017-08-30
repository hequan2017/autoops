from django.conf.urls import url

from  .import views

urlpatterns = [
    url(r'^asset.html$',views.asset_info,name='asset_info'),
    url(r'^asset-add.html$',views.asset_add,name='asset_add')
]
