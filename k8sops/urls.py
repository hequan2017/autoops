from django.urls import path

from .views import KubernetesOverview

app_name = 'k8sops'

urlpatterns = [
    path('overview/', KubernetesOverview.as_view(), name='overview'),
]
