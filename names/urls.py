from django.conf.urls import url

from  .import views

urlpatterns = [
    url(r'^login-log.html$',views.login_logs,name="login-log"),
    url(r'^password.html$', views.password_update, name="password_update")
]
