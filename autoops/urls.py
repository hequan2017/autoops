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
from django.urls  import path


urlpatterns = [
    path('admin/', admin.site.urls,name="admin1"),
    path('', index),
    path('login.html', login_view,name="login_view"),
    path('logout.html', logout,name="logout"),
    path('index.html', index),
    path('asset/', include('asset.urls', namespace="asset", ), ),
    path('tasks/', include('tasks.urls', namespace="tasks",), ),
    path('names/', include('names.urls', namespace="names",), ),
    path('library/', include('library.urls', namespace="library",), ),
    path('upload/',  AssetUpload.as_view()),
    path('ueditor/',include('DjangoUeditor.urls' )),
]



if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

