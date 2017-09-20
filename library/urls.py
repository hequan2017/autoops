from django.conf.urls import url

from  .import views

urlpatterns = [
    url(r'^library.html$', views.LibraryListAll.as_view(), name='library_list'),
    url(r'^library-add.html$', views.LibraryAdd.as_view(), name='library_add'),
    url(r'^library-update-(?P<pk>[0-9]+).html$', views.LibraryUpdate.as_view(), name='library_update'),
    url(r'^library-del.html$',views.LibraryDel.as_view(),name='library_del'),
    url(r'^library-detail-(?P<pk>\d+).html$', views.LibraryDetail.as_view(), name='library_detail'),
]
