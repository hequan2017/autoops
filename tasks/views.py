from django.shortcuts import render, redirect, HttpResponse
from  django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from asset.models import asset
import paramiko,json

tasks_active = "active"
cmd_active = "active"

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
            # history = History.objects.create(ip=i.ip, root=i.username, port=i.port, cmd=cmd, user=i.username)
            ret['data'].append(s)
        return HttpResponse(json.dumps(ret))