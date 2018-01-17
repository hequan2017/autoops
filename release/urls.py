from django.urls  import path

from  .import views

urlpatterns = [
    path('release.html',views.ReleaseListAll.as_view(),name='release_list'),
    path('release-add.html',views.ReleaseAdd.as_view(),name='release_add'),
    path('release-del.html',views.ReleaseDel.as_view(),name='release_del'),
    path('release-update-<int:pk>.html', views.ReleaseUpdate.as_view(), name='release_update'),




]


app_name="release"