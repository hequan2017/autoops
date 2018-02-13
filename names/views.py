from django.shortcuts import render, redirect, HttpResponse
from    django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .models import login_log
from .form import UserPasswordForm
from django.contrib.auth.hashers import  check_password
from  asset.models import web_history
from  tasks.models import history
from django.contrib.auth.models import User, Group
from asset.models import asset,data_centers

from django.template import loader
from pyecharts import Bar
from .password_crypt import pyecharts_add





def Bard(product,products):
    attr = product
    v1 = products
    bar = Bar("",  height=300)
    bar.add("产品线", attr, v1)
    return bar

def Bard2(data,datas):
    attr = data
    v1 = datas
    bar = Bar("",  height=300)
    bar.add("数据中心", attr, v1)
    return bar


@login_required(login_url="/login.html")
def index(request):
    asse = Group.objects.all()
    product = []
    products = []
    for i  in asse:
        x = asset.objects.filter(product_line=i).count()
        product.append(i.name)
        products.append(x)

    da = data_centers.objects.all()
    data = []
    datas = []
    for i  in da:
        x = asset.objects.filter(data_center=i).count()
        data.append(i.data_center_list)
        datas.append(x)


    template = loader.get_template('index.html')
    pro = Bard(product=product,products=products)
    pro2 = Bard2(data=data,datas=datas)

    context = dict(
        myechart=pyecharts_add(pro.render_embed())[0],
        script_list=pro.get_js_dependencies(),
        myechart1=pyecharts_add(pro2.render_embed())[0],
        product=product,
        products= products,
        data=data,
        datas=datas,
        onresize = " <script>  window.onresize = function () {  %s %s   };  </script>" % (pyecharts_add(pro.render_embed())[1],pyecharts_add(pro2.render_embed())[1])
    )



    return HttpResponse(template.render(context, request))




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
def login_history(request):
    obj = login_log.objects.order_by('-ctime')
    return render(request, 'names/login-history.html',
                  {'login_log': obj, "autoops_active": "active", "login_log_active": "active", })

@login_required(login_url="/login.html")
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



@login_required(login_url="/login.html")
def web_historys(request):
    obj = web_history.objects.order_by('-ctime')
    return render(request, 'names/web-history.html',
                  {'web_historys': obj,"autoops_active": "active", "login_log_active": "active",   })


@login_required(login_url="/login.html")
def  cmd_historys(request):
    obj = history.objects.order_by('-ctime')
    return  render(request,"names/cmd-history.html",{"historys":obj,"autoops_active": "active", "login_log_active": "active", })