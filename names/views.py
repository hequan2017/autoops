from django.shortcuts import render, redirect, HttpResponse
from    django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.generic import View
from  django.core.urlresolvers import reverse_lazy
from .models import login_log
from .form import UserPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password




@login_required(login_url="/login.html")
def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == "GET":
        error_msg = "请登录"
        return render(request, 'names/login.html', {'error_msg': error_msg, })
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(username=u, password=p)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['is_login'] = True
                login_ip = request.META['REMOTE_ADDR']
                login_log.objects.create(user=request.user, ip=login_ip)
                return redirect('/index.html')
            else:
                error_msg1 = "用户名或密码错误,或者被禁用,请重试"
                return render(request, 'names/login.html', {'error_msg': error_msg1, })
        else:
            error_msg1 = "用户名或密码错误,请重试"
            return render(request, 'names/login.html', {'error_msg': error_msg1, })


def logout(requset):  # 退出
    requset.session.clear()
    return redirect('/login.html')


@login_required(login_url="/login.html")
def error(request):  ##错误页面
    return render(request, 'names/login.html')


@login_required(login_url="/login.html")
def login_logs(request):
    obj = login_log.objects.all()
    return render(request, 'names/login-log.html',
                  {'login_log': obj, "autoops_active": "active", "login_log_active": "active", })


def password_update(request):
    if request.method == 'POST':
        form = UserPasswordForm(request.POST)
        if form.is_valid():
            old = User.objects.get(username=request.user)
            old_pass=old.password
            input_pass =form.cleaned_data['old_password']
            check = check_password(input_pass,old_pass)
         #   ps = make_password(old_p, None, 'pbkdf2_sha256')
            if  check  is True:
                if  form.cleaned_data['new_password']  == form.cleaned_data['confirm_password'] :
                    password=form.cleaned_data['new_password']
                    old.set_password(password)
                    old.save()
                    msg= "修改成功"
                else:
                    msg="两次输入的密码不一致"
                form = UserPasswordForm()
                return render(request, 'names/password.html',{'form': form, "msg": msg})
            else:
                form = UserPasswordForm()
                return render(request, 'names/password.html',{'form': form, "msg": "旧密码不对,请重新输入"})

    else:
        form = UserPasswordForm()
    return render(request, 'names/password.html',{'form': form, })
