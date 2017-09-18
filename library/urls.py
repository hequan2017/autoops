from django.conf.urls import url

from  .import views

urlpatterns = [
    url(r'^library.html$', views.LibraryListAll.as_view(), name='library_list'),
    url(r'^library-add.html$', views.LibraryAdd.as_view(), name='library_add'),
    url(r'^library-update-(?P<pk>[0-9]+).html$', views.LibraryUpdate.as_view(), name='library_update'),
]
