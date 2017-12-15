from django.urls  import path

from  .import views

urlpatterns = [
    path('login-history.html',views.login_history,name="login_history"),
    path('password.html', views.password_update, name="password_update"),
    path('web-history.html', views.web_historys, name='web_history'),
    path('cmd-history.html', views.cmd_historys, name='cmd_history'),
]


app_name = "names"