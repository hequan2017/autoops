from django.shortcuts import render, redirect, HttpResponse
from    django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.generic import View
from  django.core.urlresolvers import reverse_lazy
# Create your views here.

@login_required(login_url=reverse_lazy('login_view'))
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

