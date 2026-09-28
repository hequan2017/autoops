from django.contrib import admin

from .models import GpuAllocation, GpuOffer, GpuOrder, GpuUsageRecord


@admin.register(GpuOffer)
class GpuOfferAdmin(admin.ModelAdmin):
    list_display = ['name', 'gpu_model', 'gpu_memory_gb', 'hourly_price', 'is_active', 'ctime']
    search_fields = ['name', 'gpu_model']
    list_filter = ['gpu_model', 'is_active']


@admin.register(GpuOrder)
class GpuOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'offer', 'hours', 'total_price', 'status', 'ctime']
    search_fields = ['user__username', 'offer__name']
    list_filter = ['status', 'offer']


@admin.register(GpuAllocation)
class GpuAllocationAdmin(admin.ModelAdmin):
    list_display = ['order', 'container_id', 'gpu_uuid', 'status', 'bound_at', 'released_at']
    search_fields = ['order__user__username', 'container_id', 'gpu_uuid']
    list_filter = ['status']


@admin.register(GpuUsageRecord)
class GpuUsageRecordAdmin(admin.ModelAdmin):
    list_display = ['order', 'start_at', 'end_at', 'billed_hours', 'ctime']
    search_fields = ['order__user__username']
    list_filter = ['order']
