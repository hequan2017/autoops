from django.conf.urls import url

from  .import views

urlpatterns = [
    url(r'^cmd.html$', views.cmd, name='cmd'),
]
