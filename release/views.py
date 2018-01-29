from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import codebase
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .form import CodeBaseForm
from guardian.shortcuts import get_objects_for_user, get_objects_for_group
import json,os

from django.contrib.auth.models import User
from guardian.decorators import permission_required_or_403
from asset.models import asset
from guardian.core import ObjectPermissionChecker
from names.password_crypt import decrypt_p
from tasks.models import history

from   tasks.ansible_2420.runner import AdHocRunner
from  tasks.ansible_2420.inventory import BaseInventory


class ReleaseListAll(TemplateView):
    model = codebase
    template_name = 'release/release.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReleaseListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "release_active": "active",
            "release_list_active": "active",
            'codebase_list': codebase.objects.all(),
        }
        kwargs.update(context)
        return super(ReleaseListAll, self).get_context_data(**kwargs)



class ReleaseAdd(CreateView):
    model = codebase
    form_class = CodeBaseForm
    template_name = 'release/release-add.html'
    success_url = reverse_lazy('release:release_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReleaseAdd, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.asset_save = asset_save = form.save()
        return super(ReleaseAdd, self).form_valid(form)

    def get_success_url(self):
        return super(ReleaseAdd, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = {
            "release_active": "active",
            "release_list_active": "active",
        }
        kwargs.update(context)
        return super(ReleaseAdd, self).get_context_data(**kwargs)



class ReleaseUpdate(UpdateView):
    model = codebase
    form_class = CodeBaseForm
    template_name = 'release/release-update.html'
    success_url = reverse_lazy('release:release_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReleaseUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "release_active": "active",
            "release_list_active": "active",
        }
        kwargs.update(context)
        return super(ReleaseUpdate, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super(ReleaseUpdate, self).form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return super(ReleaseUpdate, self).form_valid(form)


    def get_success_url(self):
        return super(ReleaseUpdate, self).get_success_url()

class  ReleaseDel(View):
    model = codebase

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReleaseDel, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            id = request.POST.get('nid', None)
            print(id)
            c = codebase.objects.get(id=id)
            path = c.file.url
            print(path)
            path2 = path[1:]
            os.remove(path2)
            c.delete()

        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,代码名称不能是中文{}'.format(e)
            }
        finally:
            return HttpResponse(json.dumps(ret))

class ReleaseUpload(View):
    model = codebase

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReleaseUpload,self).dispatch(*args, **kwargs)

    def    get(self,request,pk):
        code_id = codebase.objects.filter(id=pk)
        obj = get_objects_for_user(self.request.user, 'asset.task_asset')
        return render(self.request, 'release/release-upload.html',
            { "release_active": "active",
            "release_list_active": "active",  "asset_list":obj, "code":code_id })

class ReleaseUploadPost(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
            return super(ReleaseUploadPost, self).dispatch(*args, **kwargs)

    def   post(self,request):  ##命令行
            ids = request.POST.getlist('id')
            code_id = request.POST.get('code_id', None)
            dest = request.POST.get('dest',None)
            user = User.objects.get(username=request.user)
            checker = ObjectPermissionChecker(user)
            ids1 = []

            for i in ids:
                assets = asset.objects.get(id=i)
                if checker.has_perm('task_asset', assets, ) == True:
                    ids1.append(i)
                else:
                    error_3 = "主机没有权限"
                    ret = {"error": error_3, "status": False}
                    return HttpResponse(json.dumps(ret))

            idstring = ','.join(ids1)
            if not ids:
                error_1 = "请选择主机"
                ret = {"error": error_1, "status": False}
                return HttpResponse(json.dumps(ret))

            obj = asset.objects.extra(where=['id IN (' + idstring + ')'])
            ret = {'data': []}
            tasks = []

            file = codebase.objects.get(id=code_id)


            for i in obj:
                try:
                    assets = [
                        {
                            "hostname": 'host',
                            "ip": i.network_ip,
                            "port": i.port,
                            "username": i.system_user.username,
                            "password": decrypt_p(i.system_user.password),
                        },
                    ]
                    tasks = [
                        {"action": {"module": "copy", "args": "src=./upload/{0}   {1}".format(file.file.name,dest)}, "name": "copy_code"},
                    ]

                    inventory = BaseInventory(assets)
                    runner = AdHocRunner(inventory)
                    retsult = runner.run(tasks, "all")

                    ret1 = []

                    try:
                        ret1.append("分发成功 {}      备注：如果前面返回值为 false，表示已经分发完成了，请不要重复分发。".format(retsult.results_raw['ok']['host']['copy_code']['changed']))
                    except Exception as e:
                        if retsult.results_summary['dark'] == {}   :
                                ret1.append("执行成功")
                        else:
                                ret1.append("命令有问题,{}".format(retsult.results_summary['dark']))

                    history.objects.create(ip=i.network_ip, root=i.system_user, port=i.port, cmd="上传 {} 到 {}".format(file.name,dest), user=user)

                    ret2 = {'ip': i.network_ip, 'data': '\n'.join(ret1)}
                    ret['data'].append(ret2)
                except Exception as e:
                    ret['data'].append({"ip": i.network_ip, "data": "账号密码不对,{}".format(e)})



            return HttpResponse(json.dumps(ret))