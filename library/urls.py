from django.conf.urls import url

from  .import views

urlpatterns = [
    url(r'^libray-add.html$', views.LibraryAdd.as_view(), name='libray_add'),
]
