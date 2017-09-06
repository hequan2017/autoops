from    django import forms
from .models import toolsscript


class ToolForm(forms.ModelForm):
    class Meta:
        model = toolsscript
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(
                attrs={'cols': 80, 'rows': 3}
            ),
            'tool_script': forms.Textarea(

            ),
            # 'product_line': forms.SelectMultiple(
            #     attrs={'class': 'select2',
            #            'data-placeholder': ('选择产品线')}),
            # 'admin_user': forms.Select(
            #     attrs={'class': 'select2',
            #            'data-placeholder': ('Select asset admin user')}),
        }
        help_texts = {
            # 'network_ip': '必填项目',
            'name': ('必填项目,名字不可以重复'),
        }


