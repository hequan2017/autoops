from django.conf.urls import url

from  .views import asset_info,asset_add

urlpatterns = [
    url(r'^asset.html$',asset_info,name='asset_info'),
    url(r'^asset-add.html$',asset_add,name='asset_add')
]
