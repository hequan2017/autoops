from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from  django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from asset.models import asset
from .models import history,toolsscript
import paramiko,json,os
from .form import ToolForm


from   tasks.ansible_runner.runner      import AdHocRunner,PlayBookRunner
from   tasks.ansible_runner.callback    import CommandResultCallback


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

@login_required(login_url="/login.html")
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

        for i in obj:
            s = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=i.system_user.password, cmd=cmd)
            historys = history.objects.create(ip=i.network_ip, root=i.system_user, port=i.port, cmd=cmd, user=user)
            ret['data'].append(s)

        ret['status'] = True
        print(ret)

        return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def  historys(request):
    obj = history.objects.all()
    return  render(request,"tasks/history.html",{"historys":obj,"tasks_active":tasks_active,"history_active":histroy_active})

@login_required(login_url="/login.html")
def  tools(request):
    obj = toolsscript.objects.all()
    return render(request, "tasks/tools.html",
                  {"tools": obj, "tasks_active": tasks_active, "tools_active": tools_active})


@login_required(login_url="/login.html")
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



@login_required(login_url="/login.html")
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

@login_required(login_url="/login.html")
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

@login_required(login_url="/login.html")
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


@login_required(login_url="/login.html")
def  tools_script_post(request):
    ret = {'data': None}

    if request.method == 'POST':
        try:
            host_ids = request.POST.getlist('id', None)
            sh_id = request.POST.get('shid', None)
            user = request.user

            if not host_ids:
                error1 = "请选择主机"
                ret = {"error": error1, "status": False}
                return HttpResponse(json.dumps(ret))

            idstring = ','.join(host_ids)

            host = asset.objects.extra(where=['id IN (' + idstring + ')'])
            sh = toolsscript.objects.filter(id=sh_id)

            for s in sh:
                if s.tool_run_type == 0:
                    with  open('tasks/script/test.sh', 'w+') as f:
                        f.write(s.tool_script)
                        a = 'tasks/script/{}.sh'.format(s.id)
                    os.system("sed 's/\r//'  tasks/script/test.sh >  {}".format(a))

                elif s.tool_run_type == 1:
                    with  open('tasks/script/test.py', 'w+') as f:
                        f.write(s.tool_script)
                        p = 'tasks/script/{}.py'.format(s.id)
                    os.system("sed 's/\r//'  tasks/script/test.py >  {}".format(p))
                elif s.tool_run_type == 2:
                    with  open('tasks/script/test.yml', 'w+') as f:
                        f.write(s.tool_script)
                        y = 'tasks/script/{}.yml'.format(s.id)
                    os.system("sed 's/\r//'  tasks/script/test.yml >  {}".format(y))
                else:
                    ret['status'] = False
                    ret['error'] = '脚本类型错误,只能是shell、yml、python'
                    return HttpResponse(json.dumps(ret))

                data1 = []
                for h in host:
                    try:
                        data2 = {}
                        assets = [
                            {
                                "hostname": h.hostname,
                                "ip": h.network_ip,
                                "port": h.port,
                                "username": h.system_user.username,
                                "password": h.system_user.password,
                            },
                        ]

                        history.objects.create(ip=h.network_ip, root=h.system_user.username, port=h.port, cmd=s.name, user=user)
                        if   s.tool_run_type == 0:
                            task_tuple = (('script', a),)
                            hoc = AdHocRunner(hosts=assets)
                            hoc.results_callback = CommandResultCallback()
                            r = hoc.run(task_tuple)
                            data2['ip'] = h.network_ip
                            data2['data'] = r['contacted'][h.hostname]['stdout']
                            data1.append(data2)
                            print(data1)


                        elif s.tool_run_type == 1:
                            task_tuple = (('script', p),)
                            hoc = AdHocRunner(hosts=assets)
                            hoc.results_callback = CommandResultCallback()
                            r = hoc.run(task_tuple)
                            data2['ip'] = h.network_ip
                            data2['data'] = r['contacted'][h.hostname]['stdout']
                            data1.append(data2)
                        elif s.tool_run_type == 2:
                            play = PlayBookRunner(assets, playbook_path=y)
                            b = play.run()
                            data2['ip'] = h.network_ip
                            data2['data'] = b['plays'][0]['tasks'][1]['hosts'][h.hostname]['stdout'] + \
                                            b['plays'][0]['tasks'][1]['hosts'][h.hostname]['stderr']
                            data1.append(data2)
                        else:
                            data2['ip'] = "脚本类型错误"
                            data2['data'] = "脚本类型错误"
                    except  Exception as  e:
                        data2['ip'] = h.network_ip
                        data2['data'] = "账号密码不对,请修改{}".format(e)
                        data1.append(data2)

                ret['data'] = data1
                ret['status'] = True
                return HttpResponse(json.dumps(ret))
        except Exception as e:
            ret['status'] = False
            ret['error'] = '未知错误 {}'.format(e)
            return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def   tools_script_get(request, nid):
    if request.method == "GET":
        obj = asset.objects.filter(id__gt=0)
        sh = toolsscript.objects.filter(id=nid)
        return render(request, 'tasks/tools-script.html', {"asset_list": obj, "sh": sh})