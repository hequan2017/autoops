from django.urls  import path
from  .import views

urlpatterns = [
    path('db.html',views.DbListAll.as_view(),name='db_list'),
    path('db-add.html',views.DbAdd.as_view(),name='db_add'),
    path('db-del.html',views.DbDel.as_view(),name='db_del'),
    path('db-all-del.html',views.db_all_del,name='db_all_del'),
    path('db-update-<int:pk>.html', views.DbUpdate.as_view(), name='db_update'),
    path('asset-detail-<int:pk>.html',views.DbDetail.as_view(),name='db_detail'),




    path('db-user.html', views.DbUserListAll.as_view(), name='db_user_list'),
    path('db-user-add.html', views.DbUserAdd.as_view(), name='db_user_add'),
    path('db-user-update-<int:pk>.html', views.DbUserUpdate.as_view(), name='db_user_update'),
    path('db-user-del.html', views.DbUserDel.as_view(), name='db_del'),
    path('db-user-detail-<int:pk>.html', views.DbUserDetail.as_view(), name='db_user_detail'),
    path('db-user-db-<int:nid>.html', views.Db_user_db, name='db_user_db'),
]


app_name="db"