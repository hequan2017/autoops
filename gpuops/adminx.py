import xadmin

from .models import GpuAllocation, GpuOffer, GpuOrder, GpuUsageRecord


@xadmin.sites.register(GpuOffer)
class GpuOfferAdmin(object):
    list_display = ['name', 'gpu_model', 'gpu_memory_gb', 'hourly_price', 'is_active', 'ctime']
    search_fields = ['name', 'gpu_model']
    list_filter = ['gpu_model', 'is_active']


@xadmin.sites.register(GpuOrder)
class GpuOrderAdmin(object):
    list_display = ['user', 'offer', 'hours', 'total_price', 'status', 'ctime']
    search_fields = ['user__username', 'offer__name']
    list_filter = ['status', 'offer']


@xadmin.sites.register(GpuAllocation)
class GpuAllocationAdmin(object):
    list_display = ['order', 'container_id', 'gpu_uuid', 'status', 'bound_at', 'released_at']
    search_fields = ['order__user__username', 'container_id', 'gpu_uuid']
    list_filter = ['status']


@xadmin.sites.register(GpuUsageRecord)
class GpuUsageRecordAdmin(object):
    list_display = ['order', 'start_at', 'end_at', 'billed_hours', 'ctime']
    search_fields = ['order__user__username']
    list_filter = ['order']

