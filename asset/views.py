from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from asset.models import asset, system_users
from .form import AssetForm, SystemUserForm
import json


def index(request):
    return render(request, 'index.html')



asset_active = "active"
asset_list_active = "active"
assetadd_active = "active"

def asset_list(request):
    obj = asset.objects.all()
    asset_active = "active"
    asset_list_active = "active"
    return render(request, 'asset/asset.html',
                  {'asset_list': obj, "asset_active": asset_active, "asset_list_active": asset_list_active})


def asset_add(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            form = AssetForm()
            return render(request, 'asset/asset-add.html',
                          {'form': form, "asset_active": asset_active, "assetadd_active": assetadd_active,
                           "msg": "添加成功"})
    else:
        form = AssetForm()
    return render(request, 'asset/asset-add.html',
                  {'form': form, "asset_active": asset_active, "assetadd_active": assetadd_active})


def asset_update(request, nid):
    publisher = get_object_or_404(asset, id=nid)

    if request.method == 'POST':
        form = AssetForm(request.POST, instance=publisher)
        if form.is_valid():
            publisher = form.save()
            return redirect('asset.html')

    form = AssetForm(instance=publisher)
    return render(request, 'asset/asset-update.html',
                  {'form': form, 'nid': nid, "asset_active": asset_active, "asset_list_active": asset_list_active})


def asset_del(request):
    ret = {'status': True, 'error': None, }
    if request.method == "POST":
        try:
            id = request.POST.get("nid", None)
            obj = asset.objects.get(id=id).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,{}'.format(e)
        return HttpResponse(json.dumps(ret))


def asset_detail(request, nid):
    publisher = get_object_or_404(asset, id=nid)
    detail = asset.objects.get(id=nid)

    return render(request, "asset/asset-detail.html", {"assets": detail, "nid": nid,
                                                       "asset_active": asset_active,
                                                       "asset_list_active": asset_list_active})


system_user_list_active = "active"
system_user_add_active = "active"


def system_user_list(request):
    obj = system_users.objects.all()
    return render(request, 'asset/system-user.html',
                  {'asset_list': obj, "asset_active": asset_active, "system_user_list_active": system_user_list_active})


def system_user_add(request):
    if request.method == 'POST':
        form = SystemUserForm(request.POST)
        if form.is_valid():
            assets_save = form.save()
            form = SystemUserForm()
            return render(request, 'asset/system-user-add.html',
                          {'form': form, "asset_active": asset_active, "system_user_add_active": system_user_add_active,
                           "msg": "添加成功"})
    else:
        form = SystemUserForm()
    return render(request, 'asset/system-user-add.html',
                  {'form': form, "asset_active": asset_active, "system_user_add_active": system_user_add_active, })


def system_user_update(request, nid):
    system_user = get_object_or_404(system_users, id=nid)

    if request.method == 'POST':
        form = SystemUserForm(request.POST, instance=system_user)
        if form.is_valid():
            system_user_save = form.save()
            return redirect('system-user.html')

    form = SystemUserForm(instance=system_user)
    return render(request, 'asset/system-user-update.html', {'form': form, 'nid': nid, "asset_active": asset_active,
                                                             "system_user_list_active": system_user_list_active})


def system_user_del(request):
    ret = {'status': True, 'error': None, }
    if request.method == "POST":
        try:
            id = request.POST.get("nid", None)
            obj = system_users.objects.get(id=id).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,{}'.format(e)
        return HttpResponse(json.dumps(ret))


def system_user_detail(request, nid):
    system_user = get_object_or_404(system_users, id=nid)
    detail = system_users.objects.get(id=nid)
    return render(request, "asset/system-user-detail.html",
                  {"system_users": detail, "nid": nid, "asset_active": asset_active,
                   "system_user_list_active": system_user_list_active})
