from    django import forms
from .models import db_mysql,db_user
from	django.forms	import		ValidationError

# from django.utils.translation import gettext_lazy as _


class DbMysqlForm(forms.ModelForm):
    class Meta:
        model = db_mysql
        fields = '__all__'
        labels={
            "ip":"IP",
        }
        widgets = {
            'ps': forms.Textarea(
                attrs={'cols': 80, 'rows': 3}
            ),
        }
        help_texts = {
            'ip': '主机IP',
            'product_line': '必填项目,此产品线对应的为  admin/  后台用户组,请先建立后台用户权限组',
            'data_cente': '必填项目,此产品线对应的为  admin/  后台资产 数据中心,请先建立',
        }
        error_messages = {
            'model':{
                'max_length': ('太短了'),
            }
        }




class DbUsersForm(forms.ModelForm):
    class Meta:
        model = db_user
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(
            ),
            'ps': forms.Textarea(
                attrs={'cols': 80, 'rows': 3}
            ),
        }
        help_texts = {
            'password': '在更新页面,如果不想修改当前用户的密码,保持为空即可',
               'product_line': '必填项目,此产品线对应的为  admin/  后台用户组,请先建立后台用户权限组',
        }



