"""autoops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from names.views import index,login_view,logout
from django.conf.urls import handler404, handler500
from asset.views import  AssetUpload
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls,name="admin1"),
    url(r'^$', index),
    url(r'^login.html$', login_view,name="login_view"),
    url(r'^logout.html$', logout,name="logout"),
    url(r'^index.html$', index),
    url(r'^asset/', include('asset.urls', namespace="asset", app_name='asset'), ),
    url(r'^tasks/', include('tasks.urls', namespace="tasks", app_name='tasks'), ),
    url(r'^names/', include('names.urls', namespace="names", app_name='names'), ),
    url(r'^library/', include('library.urls', namespace="library", app_name='library'), ),
    url(r'^upload/',  AssetUpload.as_view()),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

