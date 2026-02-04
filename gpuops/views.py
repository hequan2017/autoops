from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from .models import GpuAllocation, GpuOffer, GpuOrder


@method_decorator(login_required, name='dispatch')
class GpuOfferList(View):
    template_name = 'gpuops/offer-list.html'

    def get(self, request):
        offers = GpuOffer.objects.filter(is_active=True).order_by('hourly_price')
        context = {
            'gpu_active': 'active',
            'gpu_offer_active': 'active',
            'offers': offers,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        offer_id = request.POST.get('offer_id')
        hours = request.POST.get('hours')
        if not offer_id or not hours:
            messages.error(request, '请选择套餐并填写购买时长。')
            return redirect('gpuops:offer_list')

        try:
            hours_value = int(hours)
        except ValueError:
            messages.error(request, '购买时长必须为整数。')
            return redirect('gpuops:offer_list')

        if hours_value <= 0:
            messages.error(request, '购买时长必须大于0。')
            return redirect('gpuops:offer_list')

        offer = get_object_or_404(GpuOffer, pk=offer_id, is_active=True)
        total_price = GpuOrder.calculate_total(offer, hours_value)
        order = GpuOrder.objects.create(
            user=request.user,
            offer=offer,
            hours=hours_value,
            total_price=total_price,
            status=GpuOrder.STATUS_PENDING,
        )
        GpuAllocation.objects.create(order=order)
        messages.success(request, '订单已创建，请在订单列表中完成支付/开通。')
        return redirect('gpuops:order_list')


@method_decorator(login_required, name='dispatch')
class GpuOrderList(View):
    template_name = 'gpuops/order-list.html'

    def get(self, request):
        orders = GpuOrder.objects.filter(user=request.user).select_related('offer').order_by('-ctime')
        context = {
            'gpu_active': 'active',
            'gpu_order_active': 'active',
            'orders': orders,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class GpuOrderActivate(View):
    def post(self, request, order_id):
        order = get_object_or_404(GpuOrder, pk=order_id, user=request.user)
        if order.status != GpuOrder.STATUS_PENDING:
            messages.info(request, '当前订单状态无法激活。')
            return redirect('gpuops:order_list')

        order.status = GpuOrder.STATUS_ACTIVE
        order.paid_at = timezone.now()
        order.start_at = order.paid_at
        order.end_at = order.start_at + timedelta(hours=order.hours)
        order.save(update_fields=['status', 'paid_at', 'start_at', 'end_at', 'utime'])
        messages.success(request, '订单已激活，GPU 使用时长已开始计费。')
        return redirect('gpuops:order_list')
