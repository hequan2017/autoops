from django.conf.urls import url

from  .import views

urlpatterns = [
    url(r'^login-history.html$',views.login_history,name="login_history"),
    url(r'^password.html$', views.password_update, name="password_update"),
    url(r'^web-history.html$', views.web_historys, name='web_history'),
    url(r'^cmd-history.html$', views.cmd_historys, name='cmd_history'),
]
