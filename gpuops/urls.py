from django.urls import path

from .views import GpuOfferList, GpuOrderActivate, GpuOrderList

app_name = 'gpuops'

urlpatterns = [
    path('offers/', GpuOfferList.as_view(), name='offer_list'),
    path('orders/', GpuOrderList.as_view(), name='order_list'),
    path('orders/<int:order_id>/activate/', GpuOrderActivate.as_view(), name='order_activate'),
]

