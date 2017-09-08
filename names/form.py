
from    django import forms


class UserPasswordForm(forms.Form):
    old_password = forms.CharField(
        max_length=128, widget=forms.PasswordInput,label='旧密码')
    new_password = forms.CharField(
        min_length=5, max_length=128, widget=forms.PasswordInput,label='新密码',)
    confirm_password = forms.CharField(
        min_length=5, max_length=128, widget=forms.PasswordInput,label='重复输入新密码',)
