from    django import forms
from .models import codebase

class CodeBaseForm(forms.ModelForm):
    class Meta:
        model =  codebase
        fields = '__all__'

        labels={

            "file":"上传文件",

        }
        help_texts = {
            "file": "文件名称不能是中文,必填项目",

        }

        widgets = {
            'ps': forms.Textarea(
                attrs={'cols': 80, 'rows': 3}
            ),

        }






