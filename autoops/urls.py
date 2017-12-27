from django.conf.urls import include
from django.contrib import admin

from names.views import index,login_view,logout
from django.conf.urls import handler404, handler500
from asset.views import  AssetUpload
from django.conf import settings
from django.urls  import path


urlpatterns = [
    path('admin/', admin.site.urls,name="admin"),
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
]



if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

