from django.urls  import path

from  .import views

urlpatterns = [
    path('library.html', views.LibraryListAll.as_view(), name='library_list'),
    path('library-add.html', views.LibraryAdd.as_view(), name='library_add'),
    path('library-update-<int:pk>.html', views.LibraryUpdate.as_view(), name='library_update'),
    path('library-del.html',views.LibraryDel.as_view(),name='library_del'),
    path('library-detail-<int:pk>.html', views.LibraryDetail.as_view(), name='library_detail'),
]



app_name="library"