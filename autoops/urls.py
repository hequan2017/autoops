from django.conf.urls import include, handler404, handler500  # noqa: F401
from django.contrib import admin

from names.views import index, login_view, logout
from asset.views import AssetUpload
from django.conf import settings
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', index),
    path('login.html', login_view, name="login_view"),
    path('logout.html', logout, name="logout"),
    path('index.html', index),
    path('asset/', include('asset.urls', namespace="asset", ), ),
    path('db/', include('db.urls', namespace="db", ), ),
    path('tasks/', include('tasks.urls', namespace="tasks",), ),
    path('names/', include('names.urls', namespace="names",), ),
    path('library/', include('library.urls', namespace="library",), ),
    path('docker/', include('dockerops.urls', namespace="dockerops",), ),
    path('k8s/', include('k8sops.urls', namespace="k8sops",), ),
    path('gpu/', include('gpuops.urls', namespace="gpuops",), ),
    path('upload/', AssetUpload.as_view()),
    path('release/', include('release.urls', namespace="release")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
