from django.urls import path

from .views import DockerContainerList

app_name = 'dockerops'

urlpatterns = [
    path('containers/', DockerContainerList.as_view(), name='container_list'),
]
