from decimal import Decimal

from django.conf import settings
from django.db import models


class GpuOffer(models.Model):
    name = models.CharField(max_length=128, verbose_name='套餐名称')
    gpu_model = models.CharField(max_length=64, verbose_name='GPU型号')
    gpu_memory_gb = models.PositiveIntegerField(verbose_name='显存(GiB)')
    hourly_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价(元/小时)')
    is_active = models.BooleanField(default=True, verbose_name='是否上架')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    ctime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', blank=True)
    utime = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间', blank=True)

    class Meta:
        db_table = 'gpu_offer'
        verbose_name = 'GPU套餐'
        verbose_name_plural = 'GPU套餐'

    def __str__(self):
        return self.name


class GpuOrder(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_ACTIVE = 'active'
    STATUS_FINISHED = 'finished'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = (
        (STATUS_PENDING, '待支付'),
        (STATUS_PAID, '已支付'),
        (STATUS_ACTIVE, '使用中'),
        (STATUS_FINISHED, '已结束'),
        (STATUS_CANCELED, '已取消'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='购买用户')
    offer = models.ForeignKey(GpuOffer, on_delete=models.PROTECT, verbose_name='套餐')
    hours = models.PositiveIntegerField(verbose_name='购买时长(小时)')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='订单金额')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name='订单状态')
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name='支付时间')
    start_at = models.DateTimeField(blank=True, null=True, verbose_name='开始时间')
    end_at = models.DateTimeField(blank=True, null=True, verbose_name='结束时间')
    ctime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', blank=True)
    utime = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间', blank=True)

    class Meta:
        db_table = 'gpu_order'
        verbose_name = 'GPU订单'
        verbose_name_plural = 'GPU订单'

    def __str__(self):
        return f"{self.user}-{self.offer}-{self.ctime}"

    @classmethod
    def calculate_total(cls, offer, hours):
        return (offer.hourly_price * Decimal(hours)).quantize(Decimal('0.01'))


class GpuAllocation(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_BOUND = 'bound'
    STATUS_RELEASED = 'released'

    STATUS_CHOICES = (
        (STATUS_PENDING, '待分配'),
        (STATUS_BOUND, '已分配'),
        (STATUS_RELEASED, '已释放'),
    )

    order = models.OneToOneField(GpuOrder, on_delete=models.CASCADE, verbose_name='订单')
    container_id = models.CharField(max_length=128, blank=True, null=True, verbose_name='容器ID')
    gpu_uuid = models.CharField(max_length=128, blank=True, null=True, verbose_name='GPU UUID')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name='分配状态')
    bound_at = models.DateTimeField(blank=True, null=True, verbose_name='分配时间')
    released_at = models.DateTimeField(blank=True, null=True, verbose_name='释放时间')
    ctime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', blank=True)
    utime = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间', blank=True)

    class Meta:
        db_table = 'gpu_allocation'
        verbose_name = 'GPU分配'
        verbose_name_plural = 'GPU分配'


class GpuUsageRecord(models.Model):
    order = models.ForeignKey(GpuOrder, on_delete=models.CASCADE, verbose_name='订单')
    start_at = models.DateTimeField(verbose_name='开始时间')
    end_at = models.DateTimeField(blank=True, null=True, verbose_name='结束时间')
    billed_hours = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='计费时长(小时)')
    ctime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', blank=True)

    class Meta:
        db_table = 'gpu_usage_record'
        verbose_name = 'GPU用量记录'
        verbose_name_plural = 'GPU用量记录'

