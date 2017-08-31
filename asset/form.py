from    django import forms
from .models import asset


# from django.utils.translation import gettext_lazy as _


class PublisherForm(forms.ModelForm):
    class Meta:
        model = asset
        fields = [
            'network_ip', 'manage_ip', 'model', 'data_center', 'cabinet', 'position',
            'sn', 'cpu', 'memory', 'disk', 'port', 'ship_time', 'end_time', 'product_line', 'ps'
        ]
        widgets = {
            'data_center': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': ('数据中心')}),
            'ship_time': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'end_time': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'ps': forms.Textarea(
                attrs={'cols': 80, 'rows': 3}
            )
        }
        help_texts = {
            # 'network_ip': '必填项目',
            'model': ('必填项目,请输入产品型号,如:DELL R620 '),
        }
