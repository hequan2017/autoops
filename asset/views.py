from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from    django.utils.decorators import method_decorator
from asset.models import asset, system_users, performance, web_history
from .form import AssetForm, SystemUserForm
import json
from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm, get_perms
from guardian.core import ObjectPermissionChecker
from guardian.decorators import permission_required_or_403
from tasks.views import ssh
from guardian.shortcuts import get_objects_for_user, get_objects_for_group
from guardian.models import UserObjectPermission, GroupObjectPermission
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from tasks.views import ssh

# from common.mixins import JSONResponseMixin

from  tasks.ansible_runner.runner import AdHocRunner
from django.db.models import Q


class AssetListAll(TemplateView):
    template_name = 'asset/asset.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AssetListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
            'asset_list': get_objects_for_user(self.request.user, 'asset.read_asset')
        }
        kwargs.update(context)
        return super(AssetListAll, self).get_context_data(**kwargs)

    def post(self, request):
        query = request.POST.get("name")
        print(query)
        a = asset.objects.filter(
            Q(network_ip=query) | Q(manage_ip=query) | Q(hostname=query) | Q(inner_ip=query) | Q(model=query) | Q(
                eth0=query) | Q(eth1=query) | Q(eth2=query) | Q(eth3=query) |
            Q(system=query) | Q(system_user__username=query) | Q(data_center__data_center_list=query) | Q(
                cabinet=query) |
            Q(position=query) | Q(sn=query)
            | Q(uplink_port=query) |
            Q(product_line__name=query))

        return render(request, 'asset/asset.html',
                      {"asset_active": "active", "asset_list_active": "active", "asset_list": a})


class AssetAdd(CreateView):
    model = asset
    form_class = AssetForm
    template_name = 'asset/asset-add.html'
    success_url = reverse_lazy('asset:asset_list')

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('asset.add_asset'))
    def dispatch(self, *args, **kwargs):
        return super(AssetAdd, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.asset_save = asset_save = form.save()
        myproduct = asset.objects.get(network_ip=form.cleaned_data['network_ip']).product_line
        mygroup = Group.objects.get(name=myproduct)
        GroupObjectPermission.objects.assign_perm("read_asset", mygroup, obj=asset_save)
        GroupObjectPermission.objects.assign_perm("add_asset", mygroup, obj=asset_save)
        GroupObjectPermission.objects.assign_perm("change_asset", mygroup, obj=asset_save)
        GroupObjectPermission.objects.assign_perm("delete_asset", mygroup, obj=asset_save)
        return super(AssetAdd, self).form_valid(form)

    def get_success_url(self):
        return super(AssetAdd, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(AssetAdd, self).get_context_data(**kwargs)


class AssetUpdate(UpdateView):
    model = asset
    form_class = AssetForm
    template_name = 'asset/asset-update.html'
    success_url = reverse_lazy('asset:asset_list')

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('asset.add_asset', (asset, 'id', 'pk')))
    def dispatch(self, *args, **kwargs):
        return super(AssetUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(AssetUpdate, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super(AssetUpdate, self).form_invalid(form)

    def form_valid(self, form):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        oldmyproduct = asset.objects.get(id=pk).product_line
        oldmygroup = Group.objects.get(name=oldmyproduct)
        self.object = form.save()
        myproduct = asset.objects.get(id=pk).product_line
        mygroup = Group.objects.get(name=myproduct)

        if oldmygroup != mygroup:
            GroupObjectPermission.objects.filter(object_pk=pk).delete()
            GroupObjectPermission.objects.assign_perm("read_asset", mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("add_asset", mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("change_asset", mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("delete_asset", mygroup, obj=self.object)
        return super(AssetUpdate, self).form_valid(form)

    def get_success_url(self):
        return super(AssetUpdate, self).get_success_url()


class AssetDetail(DetailView):
    model = asset
    template_name = 'asset/asset-detail.html'

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('asset.change_asset', (asset, 'id', 'pk')))
    def dispatch(self, *args, **kwargs):
        return super(AssetDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = asset.objects.get(id=pk)
        print(detail.file)
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
            "assets": detail,
            "nid": pk,
        }
        kwargs.update(context)
        return super(AssetDetail, self).get_context_data(**kwargs)


class AssetDel(View):
    model = asset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AssetDel, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            id = request.POST.get('nid', None)
            user = User.objects.get(username=request.user)
            checker = ObjectPermissionChecker(user)
            assets = asset.objects.get(id=id)
            if checker.has_perm('delete_asset', assets, ) == True:
                assets.delete()
                GroupObjectPermission.objects.filter(object_pk=id).delete()
        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,{}'.format(e)
            }
        return   HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def asset_all_del(request):
    ret = {'status': True, 'error': None, }
    if request.method == "POST":
        try:
            ids = request.POST.getlist('id', None)
            ids1 = []
            for i in ids:
                user = User.objects.get(username=request.user)
                checker = ObjectPermissionChecker(user)
                assets = asset.objects.get(id=i)
                if checker.has_perm('delete_asset', assets, ) == True:
                    ids1.append(i)

            idstring = ','.join(ids1)
            asset.objects.extra(where=['id IN (' + idstring + ')']).delete()
            GroupObjectPermission.objects.extra(where=['object_pk IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,{}'.format(e)
        return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def asset_hardware_update(request):
    ret = {'status': True, 'error': None, 'data': None}

    if request.method == 'POST':
        try:
            id = request.POST.get('nid', None)
            obj = asset.objects.get(id=id)
            ip = obj.network_ip
            port = obj.port
            username = obj.system_user.username
            password = obj.system_user.password
            assets = [
                {
                    "hostname": 'host',
                    "ip": ip,
                    "port": port,
                    "username": username,
                    "password": password,
                },
            ]


            task_tuple = (('setup', ''),)
            runner = AdHocRunner(assets)
            result = runner.run(task_tuple=task_tuple, pattern='all', task_name='Ansible Ad-hoc')

            data = result['contacted']['host'][0]['ansible_facts']

            hostname = data['ansible_nodename']
            system = data['ansible_distribution'] + " " + data['ansible_distribution_version']


            try:
                a2 = "parted -l  | grep   \"Disk \/dev\/[a-z]d\"  | awk -F\"[ ]\"  '{print $3}' | awk  -F\"GB\"  '{print $1}'"
                s = ssh(ip=ip, port=port, username=username, password=password, cmd=a2)
                disk1 = s['data']
                disk2 = disk1.rstrip().split("\n")
                disk = "+".join(map(str, disk2)) + "   共计:{} GB".format(round(sum(map(float, disk2))))
            except Exception  as  e:

                disk =  " 共计{}".format(str(sum([int(data["ansible_devices"][i]["sectors"]) * \
                             int(data["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024 \
                          for i in data["ansible_devices"] if i[0:2] in ("vd", "ss", "sd")])) + str(" GB"))


            try:
                a1 = "dmidecode | grep -P -A5 \"Memory\ Device\"  | grep Size   | grep -v \"No Module Installed\" | grep -v \"0\"   | awk -F\":\" \'{print $2}\'  | awk -F\" \"  \'{print  $1}\'"
                s = ssh(ip=ip, port=port, username=username, password=password, cmd=a1)
                memory1 = s['data']

                if memory1  ==   "" :
                    memory0 = []
                    memory0.append(int(round((data['ansible_memtotal_mb']) / 1000)))
                else:
                    memory2 = memory1.rstrip().split("\n")
                    memory0 = []

                    for i in range(len(memory2)):
                        memory0.append((int(int(memory2[i]) / 1024)))

                memory = "+".join(map(str, memory0)) + '    共计:{} GB'.format((sum(map(int, memory0))))

            except Exception as e:
                memory =  '    共计:{} GB'.format(round((data['ansible_memtotal_mb']/ 1000)))


            sn = data['ansible_product_serial']
            model =data["ansible_system_vendor"] + " " +data['ansible_product_name']
            cpu = data['ansible_processor'][1] + "  {}核心".format(data['ansible_processor_count']*data["ansible_processor_cores"])


            try:
                a = "ipmitool lan print | grep -w \"IP Address \"   | awk -F\":\" \ '{print $2}\'"
                s = ssh(ip=ip, port=port, username=username, password=password, cmd=a)
                manage = s['data']
            except Exception as e:
                manage = None

            net =  data["ansible_interfaces"][1:]

            net.sort()

            try:
                 eth0= data['ansible_{}'.format(net[0])]['macaddress']
                 eth1 = data['ansible_{}'.format(net[1])]['macaddress']
                 eth2 = data['ansible_{}'.format(net[2])]['macaddress']
                 eth3 = data['ansible_{}'.format(net[3])]['macaddress']
            except Exception as e:
                 eth0,eth1,eth2,eth3 = None,None,None,None

            ass = asset.objects.filter(id=id).update(hostname=hostname, manage_ip=manage, system=system,
                                                     memory=memory,disk=disk, sn=sn, model=model, cpu=cpu, eth0=eth0,eth1=eth1,eth2=eth2,eth3=eth3)

        except Exception as e:
            ret['status'] = False
            ret['error'] = '登陆账号权限不够，请在被添加的主机安装parted  ipmitool dmidecode 或更新错误{}'.format(e)
        return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def asset_web_ssh(request):
    if request.method == 'POST':
        id = request.POST.get('id', None)
        obj = asset.objects.get(id=id)
        ip = obj.network_ip + ":" + str(obj.port)
        username = obj.system_user.username
        password = obj.system_user.password
        ret = {"ip": ip, "username": username, 'password': password, "static": True}

        login_ip = request.META['REMOTE_ADDR']

        web_history.objects.create(user=request.user, ip=login_ip, login_user=obj.system_user.username, host=ip)
        return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def asset_performance(request, nid):
    try:
        # i = asset.objects.get(id=nid)
        # cpu_1 = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=i.system_user.password,
        #             cmd=" top -bn 1 -i -c | grep Cpu   ")
        # cpu_2 = cpu_1['data'].split()
        # cpu = cpu_2[1].split('%')[0]
        #
        # total = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=i.system_user.password,
        #             cmd=" free | grep  Mem:  ")
        # list = total['data'].split(" ")
        # while '' in list:
        #     list.remove('')
        # mem = float('%.2f' % (float('%.3f' % (int(list[2]) / int(list[1]))) * 100))




        all = performance.objects.all()
        date, cpu_use, mem_use, in_use, out_use = [], [], [], [], []

        for i in all:
            if i.server_id == int(nid):
                date.append(i.cdate.strftime("%m-%d %H:%M"))
                cpu_use.append(i.cpu_use)
                mem_use.append(i.mem_use)
                in_use.append(i.in_use)
                out_use.append(i.out_use)
        if  cpu_use :
            cpu = cpu_use[-1]
            mem = mem_use[-1]
        else:
            cpu = 0
            mem = 0


        return render(request, 'asset/asset-performance.html', {'cpu': cpu, 'mem': mem, "asset_id": id,
                                                                'date': date, 'cpu_use': cpu_use, 'mem_use': mem_use,
                                                                'in_use': in_use, 'out_use': out_use,
                                                                "asset_active": "active",
                                                                "asset_list_active": "active"})

    except Exception as e:
        obj = asset.objects.all()
        error = "  错误, {}".format(e)
        return render(request, 'asset/asset.html',
                      {'asset_list': obj, "asset_active": "active", "asset_list_active": "active",
                       "error_performance": error})


@login_required(login_url="/login.html")
def system_user_list(request):
    obj = system_users.objects.all()
    user = User.objects.get(username=request.user)
    checker = ObjectPermissionChecker(user)
    l = []

    for i in obj:
        system_u = system_users.objects.get(id=i.id)
        if checker.has_perm('read_system_users', system_u) == True:
            l.append(i)
    return render(request, 'asset/system-user.html',
                  {'asset_list': l, "asset_active": "active", "system_user_list_active": "active"})


@login_required(login_url="/login.html")
def system_user_add(request):
    if request.method == 'POST':
        form = SystemUserForm(request.POST)
        if form.is_valid():
            system_save = form.save()
            myproduct = system_users.objects.get(name=form.cleaned_data['name']).product_line
            mygroup = Group.objects.get(name=myproduct)
            GroupObjectPermission.objects.assign_perm("read_system_users", mygroup, obj=system_save)
            GroupObjectPermission.objects.assign_perm("add_system_users", mygroup, obj=system_save)
            GroupObjectPermission.objects.assign_perm("change_system_users", mygroup, obj=system_save)
            GroupObjectPermission.objects.assign_perm("delete_system_users", mygroup, obj=system_save)

            form = SystemUserForm()
            return render(request, 'asset/system-user-add.html',
                          {'form': form, "asset_active": "active",
                           "system_user_list_active": "active",
                           "msg": "添加成功"})
    else:
        form = SystemUserForm()
    return render(request, 'asset/system-user-add.html',
                  {'form': form, "asset_active": "active", "system_user_list_active": "active", })


@login_required(login_url="/login.html")
def system_user_update(request, nid):
    system_user = get_object_or_404(system_users, id=nid)

    if request.method == 'POST':
        form = SystemUserForm(request.POST, instance=system_user)
        old_password = system_users.objects.get(id=nid).password
        if form.is_valid():
            password = form.cleaned_data['password']
            if password:
                if system_users.objects.get(id=nid).product_line == form.cleaned_data['product_line']:
                    system_user_pasword = form.save()
                else:
                    system_save = form.save()
                    myproduct = system_users.objects.get(name=form.cleaned_data['name']).product_line
                    mygroup = Group.objects.get(name=myproduct)
                    GroupObjectPermission.objects.filter(object_pk=nid).delete()

                    GroupObjectPermission.objects.assign_perm("read_system_users", mygroup, obj=system_save)
                    GroupObjectPermission.objects.assign_perm("add_system_users", mygroup, obj=system_save)
                    GroupObjectPermission.objects.assign_perm("change_system_users", mygroup, obj=system_save)
                    GroupObjectPermission.objects.assign_perm("delete_system_users", mygroup, obj=system_save)
                    form = AssetForm()
            else:
                s = system_users.objects.get(id=nid)
                s.name = form.cleaned_data['name']
                s.username = form.cleaned_data['username']
                s.password = old_password
                s.product_line = form.cleaned_data['product_line']
                s.ps = form.cleaned_data['ps']
                if system_users.objects.get(id=nid).product_line == form.cleaned_data['product_line']:
                    s.save()
                else:
                    s.save()
                    myproduct = system_users.objects.get(name=form.cleaned_data['name']).product_line
                    mygroup = Group.objects.get(name=myproduct)
                    GroupObjectPermission.objects.filter(object_pk=nid).delete()

                    GroupObjectPermission.objects.assign_perm("read_system_users", mygroup, obj=s)
                    GroupObjectPermission.objects.assign_perm("add_system_users", mygroup, obj=s)
                    GroupObjectPermission.objects.assign_perm("change_system_users", mygroup, obj=s)
                    GroupObjectPermission.objects.assign_perm("delete_system_users", mygroup, obj=s)
                    form = AssetForm()

            return redirect('system-user.html')

    form = SystemUserForm(instance=system_user)
    return render(request, 'asset/system-user-update.html', {'form': form, 'nid': nid, "asset_active": "active",
                                                             "system_user_list_active": "active",
                                                             })


@login_required(login_url="/login.html")
def system_user_del(request):
    ret = {'status': True, 'error': None, }
    if request.method == "POST":
        try:
            id = request.POST.get("nid", None)
            user = User.objects.get(username=request.user)
            checker = ObjectPermissionChecker(user)
            system_u = system_users.objects.get(id=id)
            if checker.has_perm('delete_system_users', system_u, ) == True:
                system_u.delete()
                GroupObjectPermission.objects.filter(object_pk=id).delete()

        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,{}'.format(e)
        return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
@permission_required_or_403('change_system_users', (system_users, 'id', 'nid'))
def system_user_detail(request, nid):
    system_user = get_object_or_404(system_users, id=nid)
    detail = system_users.objects.get(id=nid)
    return render(request, "asset/system-user-detail.html",
                  {"system_users": detail, "nid": nid, "asset_active": "active",
                   "system_user_list_active": "active"})


@login_required(login_url="/login.html")
def system_user_asset(request, nid):
    sys = system_users.objects.get(id=nid)
    obj = asset.objects.filter(system_user=nid)
    return render(request, "asset/system-user-asset.html", {"system_users": sys, "nid": nid, "asset_list": obj,
                                                            "asset_active": "active",
                                                            "system_user_list_active": "active"})


class AssetUpload(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AssetUpload, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        with open('{}'.format(request.path[1:]), 'rb')  as f:
            url = request.path
            urls = url.split("/")[-1]
            response = HttpResponse(f, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment;	filename={}'.format(urls)
            return response
