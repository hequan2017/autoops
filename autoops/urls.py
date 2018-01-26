from django.conf.urls import include,url
from django.contrib import admin

from names.views import index,login_view,logout
from django.conf.urls import handler404, handler500
from asset.views import  AssetUpload
from django.conf import settings
from django.urls  import path

import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()


urlpatterns = [
    path('admin/', xadmin.site.urls, name="xadmin"),
    path('dadmin/', admin.site.urls,name="dadmin"),
    path('', index),
    path('login.html', login_view,name="login_view"),
    path('logout.html', logout,name="logout"),
    path('index.html', index),
    path('asset/', include('asset.urls', namespace="asset", ), ),
    path('db/', include('db.urls', namespace="db", ), ),
    path('tasks/', include('tasks.urls', namespace="tasks",), ),
    path('names/', include('names.urls', namespace="names",), ),
    path('library/', include('library.urls', namespace="library",), ),
    path('upload/',  AssetUpload.as_view()),
    path('ueditor/',include('DjangoUeditor.urls' )),
    path('release/', include('release.urls', namespace="release")),
]



if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

