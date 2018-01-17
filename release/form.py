from    django import forms
from .models import codebase

class CodeBaseForm(forms.ModelForm):
    class Meta:
        model =  codebase
        fields = '__all__'

        labels={

            "file":"上传文件"
        }
        widgets = {
            'ps': forms.Textarea(
                attrs={'cols': 80, 'rows': 3}
            ),

        }






