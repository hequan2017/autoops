from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from  django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from asset.models import asset
from .models import history,toolsscript
import paramiko,json
from .form import ToolForm

tasks_active = "active"
cmd_active = "active"
histroy_active="active"
tools_active="active"


def ssh(ip, port, username, password, cmd):
    try:
        ssh = paramiko.SSHClient()  # 创建ssh对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=int(port), username=username, password=password, )
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
        result = stdout.read()
        result1 = result.decode()
        error = stderr.read().decode('utf-8')

        if not error:
            ret = {"ip": ip, "data": result1}
            ssh.close()
            return ret
    except Exception as e:
        error = "账号或密码错误,{}".format(e)
        ret = {"ip": ip, "data": error}
        return ret


def cmd(request):  ##命令行

    if request.method == "GET":
        obj = asset.objects.all()
        return render(request, 'tasks/cmd.html',{'asset_list': obj,"tasks_active":tasks_active,"cmd_active":cmd_active})

    if request.method == 'POST':
        ids = request.POST.getlist('id')
        cmd = request.POST.get('cmd', None)
        user = request.user
        idstring = ','.join(ids)
        if not ids:
            error_1 = "请选择主机"
            ret = {"error": error_1, "status": False}
            return HttpResponse(json.dumps(ret))
        elif not cmd:
            error_2 = "请输入命令"
            ret = {"error": error_2, "status": False}
            return HttpResponse(json.dumps(ret))

        obj = asset.objects.extra(where=['id IN (' + idstring + ')'])


        ret = {}
        ret['data'] = []
        ret['status'] = True
        for i in obj:
            s = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=i.system_user.password, cmd=cmd)
            historys = history.objects.create(ip=i.network_ip, root=i.system_user, port=i.port, cmd=cmd, user=user)
            ret['data'].append(s)
        return HttpResponse(json.dumps(ret))

def  historys(request):
    obj = history.objects.all()
    return  render(request,"tasks/history.html",{"historys":obj,"tasks_active":tasks_active,"history_active":histroy_active})


def  tools(request):
    obj = toolsscript.objects.all()
    return render(request, "tasks/tools.html",
                  {"tools": obj, "tasks_active": tasks_active, "tools_active": tools_active})

def  tools_add(request):

    if request.method == 'POST':
        form =  ToolForm(request.POST)
        if form.is_valid():
            tools_save = form.save()
            form =  ToolForm()
            return render(request, 'tasks/tools-add.html',
                          {'form': form, "tasks_active": tasks_active, "tools_active": tools_active,
                           "msg": "添加成功"})
    else:
        form =  ToolForm()
    return render(request, 'tasks/tools-add.html',
                  {'form': form, "tasks_active": tasks_active, "tools_active": tools_active,})


def  tools_update(request,nid):
    tool_id = get_object_or_404(toolsscript, id=nid)

    if request.method == 'POST':
        form = ToolForm(request.POST, instance=tool_id)
        if form.is_valid():
            asset_save = form.save()
            return redirect('tools.html')

    form = ToolForm(instance=tool_id)
    return render(request, 'tasks/tools-update.html',
                  {'form': form, 'nid': nid,  "tasks_active": tasks_active, "tools_active": tools_active,})


def  tools_delete(request):
    ret = {'status': True, 'error': None, }
    if request.method == "POST":
        try:
            id_1 = request.POST.get("nid", None)
            toolsscript.objects.get(id=id_1).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,{}'.format(e)
        return HttpResponse(json.dumps(ret))


def  tools_bulk_delte(request):
    ret = {'status': True, 'error': None, }
    if request.method == "POST":
        try:
            ids = request.POST.getlist('id', None)
            idstring = ','.join(ids)
            toolsscript.objects.extra(where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,{}'.format(e)
        return HttpResponse(json.dumps(ret))


