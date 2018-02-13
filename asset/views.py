from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from asset.models import asset, system_users, performance, web_history, data_centers
from .form import AssetForm, SystemUserForm
from names.password_crypt import encrypt_p, decrypt_p, pyecharts_add
from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm, get_perms
from guardian.core import ObjectPermissionChecker
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import get_objects_for_user, get_objects_for_group
from django.contrib.auth.models import Permission
from guardian.models import UserObjectPermission, GroupObjectPermission
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from tasks.views import ssh
from autoops import settings
from django.db.models import Q
import xlwt, time, json
from django.template import loader
from pyecharts import Gauge, Line
import threading, time, datetime


from   tasks.ansible_2420.runner import AdHocRunner, CommandRunner
from  tasks.ansible_2420.inventory import BaseInventory



class AssetListAll(TemplateView):
    template_name = 'asset/asset.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AssetListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
            "Webssh": getattr(settings, 'Webssh_ip'),
            "Webssh_port": getattr(settings, 'Webssh_port'),
            'asset_list': get_objects_for_user(self.request.user, 'asset.read_asset')
        }
        kwargs.update(context)
        return super(AssetListAll, self).get_context_data(**kwargs)

    def post(self, request):
        query = request.POST.get("name")

        user = User.objects.get(username=request.user)
        if user.is_superuser == 1:
            ret = asset.objects.filter(Q(network_ip=query) | Q(manage_ip=query) | Q(hostname=query) | Q(
                inner_ip=query) | Q(model=query) | Q(
                eth0=query) | Q(eth1=query) | Q(eth2=query) | Q(eth3=query) |
                                       Q(system=query) | Q(system_user__username=query) | Q(
                data_center__data_center_list=query) | Q(
                cabinet=query) |
                                       Q(position=query) | Q(sn=query)
                                       | Q(uplink_port=query) | Q(product_line__name=query)
                                       )
        else:
            product1 = Group.objects.get(user=user)

            ret = asset.objects.filter(Q(product_line__name=product1) &  Q(network_ip=query) | Q(manage_ip=query) | Q(hostname=query) | Q( inner_ip=query) | Q(model=query) | Q(eth0=query) | Q(eth1=query) | Q(eth2=query) | Q(eth3=query) |
                                       Q(system=query) | Q(system_user__username=query)
                                       | Q(data_center__data_center_list=query) | Q(cabinet=query) | Q(position=query) | Q(sn=query)| Q(uplink_port=query))

        return render(request, 'asset/asset.html',
                      {"Webssh": getattr(settings, 'Webssh_ip'),
                       "Webssh_port": getattr(settings, 'Webssh_port'),
                       "asset_active": "active",
                       "asset_list_active": "active", "asset_list": ret})




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

        myproduct = form.cleaned_data['product_line']
        mygroup = Group.objects.get(name=myproduct)

        GroupObjectPermission.objects.assign_perm("read_asset", mygroup, obj=asset_save)
        GroupObjectPermission.objects.assign_perm("add_asset", mygroup, obj=asset_save, )
        GroupObjectPermission.objects.assign_perm("change_asset", mygroup, obj=asset_save)
        GroupObjectPermission.objects.assign_perm("delete_asset", mygroup, obj=asset_save)
        GroupObjectPermission.objects.assign_perm("task_asset", mygroup, obj=asset_save)
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
        old_myproduct = asset.objects.get(id=pk).product_line
        old_mygroup = Group.objects.get(name=old_myproduct)
        new_mygroup = Group.objects.get(name=form.cleaned_data['product_line'])

        self.object = form.save()
        if old_mygroup != new_mygroup:
            GroupObjectPermission.objects.remove_perm("read_asset", old_mygroup, obj=self.object)
            GroupObjectPermission.objects.remove_perm("add_asset", old_mygroup, obj=self.object)
            GroupObjectPermission.objects.remove_perm("change_asset", old_mygroup, obj=self.object)
            GroupObjectPermission.objects.remove_perm("delete_asset", old_mygroup, obj=self.object)
            GroupObjectPermission.objects.remove_perm("task_asset", old_mygroup, obj=self.object)

            GroupObjectPermission.objects.assign_perm("read_asset", new_mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("add_asset", new_mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("change_asset", new_mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("delete_asset", new_mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("task_asset", new_mygroup, obj=self.object)
        return super(AssetUpdate, self).form_valid(form)

    def get_success_url(self):
        return super(AssetUpdate, self).get_success_url()



class AssetDetail(DetailView):
    model = asset
    template_name = 'asset/asset-detail.html'

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('asset.read_asset', (asset, 'id', 'pk')))
    def dispatch(self, *args, **kwargs):
        return super(AssetDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = asset.objects.get(id=pk)

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
            print(id)
            users= User.objects.get(username=request.user)
            print(users)
            checker = ObjectPermissionChecker(users)
            assets = asset.objects.get(id=id)
            print(assets)

            if checker.has_perm('delete_asset', assets, ) == True:
                assets.delete()
        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,没有权限{}'.format(e)
            }
        finally:
            return HttpResponse(json.dumps(ret))




class AssetAllDel(View):
    model = asset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AssetAllDel, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
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

        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,没有权限{}'.format(e)
        finally:
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
            password1 = obj.system_user.password

            password = decrypt_p(password1)
            assets = [
                {
                    "hostname": 'host',
                    "ip": ip,
                    "port": port,
                    "username": username,
                    "password": password,
                },
            ]



            inventory = BaseInventory(assets)
            runner = AdHocRunner(inventory)

            tasks = [
                {"action": {"module": "setup", "args": ""}, "name": "setup"},
            ]
            result = runner.run(tasks, "all")

            data = result.results_raw['ok']['host']['setup']['ansible_facts']




            hostname = data['ansible_nodename']
            system = data['ansible_distribution'] + " " + data['ansible_distribution_version']

            try:
                a2 = "parted -l  | grep   \"Disk \/dev\/[a-z]d\"  | awk -F\"[ ]\"  '{print $3}' | awk  -F\"GB\"  '{print $1}'"
                s = ssh(ip=ip, port=port, username=username, password=password, cmd=a2)
                disk1 = s['data']
                disk2 = disk1.rstrip().split("\n")
                disk = "+".join(map(str, disk2)) + "   共计:{} GB".format(round(sum(map(float, disk2))))
            except Exception  as  e:
                disk = " 共计{}".format(str(sum([int(data["ansible_devices"][i]["sectors"]) * \
                                               int(data["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024 \
                                               for i in data["ansible_devices"] if
                                               i[0:2] in ("vd", "ss", "sd")])) + str(" GB"))

            try:
                a1 = "dmidecode | grep -P -A5 \"Memory\ Device\"  | grep Size   | grep -v \"No Module Installed\" | grep -v \"0\"   | awk -F\":\" \'{print $2}\'  | awk -F\" \"  \'{print  $1}\'"
                s = ssh(ip=ip, port=port, username=username, password=password, cmd=a1)
                memory1 = s['data']

                if memory1 == "":
                    memory0 = []
                    memory0.append(int(round((data['ansible_memtotal_mb']) / 1000)))
                else:
                    memory2 = memory1.rstrip().split("\n")
                    memory0 = []

                    for i in range(len(memory2)):
                        memory0.append((int(int(memory2[i]) / 1024)))

                memory = "+".join(map(str, memory0)) + '    共计:{} GB'.format((sum(map(int, memory0))))

            except Exception as e:
                memory = '    共计:{} GB'.format(round((data['ansible_memtotal_mb'] / 1000)))

            sn = data['ansible_product_serial']
            model = data["ansible_system_vendor"] + " " + data['ansible_product_name']
            cpu = data['ansible_processor'][1] + "  {}核心".format(
                data['ansible_processor_count'] * data["ansible_processor_cores"])

            try:
                a = "ipmitool lan print | grep -w \"IP Address \"   | awk -F\":\" \ '{print $2}\'"
                s = ssh(ip=ip, port=port, username=username, password=password, cmd=a)
                manage = s['data']
            except Exception as e:
                manage = None

            net = data["ansible_interfaces"][1:]
            net.sort()

            try:
                eth0 = data['ansible_{}'.format(net[0])]['macaddress']
            except Exception as e:
                eth0 = None

            try:
                eth1 = data['ansible_{}'.format(net[1])]['macaddress']
            except Exception as e:
                eth1 = None

            try:
                eth2 = data['ansible_{}'.format(net[2])]['macaddress']
            except Exception as e:
                eth2 = None

            try:
                eth3 = data['ansible_{}'.format(net[3])]['macaddress']
            except Exception as e:
                eth3 = None

            ass = asset.objects.filter(id=id).first()
            ass.hostname = hostname
            ass.manage_ip = manage
            ass.system = system
            ass.memory = memory
            ass.disk = disk
            ass.sn = sn
            ass.model = model
            ass.cpu = cpu
            ass.eth0 = eth0
            ass.eth1 = eth1
            ass.eth2 = eth2
            ass.eth3 = eth3
            ass.save()

        except Exception as e:
            ret['status'] = False
            ret['error'] = '登陆账号权限不够| 请在被添加的主机安装  parted  ipmitool dmidecode  |    或者 删除  主服务器/root/.ssh/known_hosts  文件'.format(e)
        return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def asset_web_ssh(request):
    if request.method == 'POST':
        id = request.POST.get('id', None)
        obj = asset.objects.get(id=id)

        a = asset.objects.get(id=id)
        user = User.objects.get(username=request.user)
        checker = ObjectPermissionChecker(user)
        ret = {}
        try:
            if checker.has_perm('task_asset', a) == True:
                ip = obj.network_ip
                port = obj.port
                username = obj.system_user.username
                password = obj.system_user.password

                ret = {"ip": ip,'port':port,"username": username, 'password': password, "static": True}
                login_ip = request.META['REMOTE_ADDR']

                web_history.objects.create(user=request.user, ip=login_ip, login_user=obj.system_user.username, host=ip)
        except Exception as e:
            ret['status'] = False
            ret['error'] = '请求错误,{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))


def Gauge_cpumem(attr, data):
    bar = Gauge("", height=300)
    bar.add("", attr, data)
    return bar


def Line_network(d, title, title1, date, network_in, network_put):
    bar = Line(d, width=1600, height=500)
    bar.add(title, date, network_in,is_datazoom_show=True)
    bar.add(title1, date, network_put,is_datazoom_show=True)
    return bar


@login_required(login_url="/login.html")
@permission_required_or_403('asset.read_asset', (asset, 'id', 'nid'))
def asset_performance(request, nid):
    template = loader.get_template('asset/asset-performance.html')

    now = datetime.datetime.now()
    last_time = now + datetime.timedelta(days=-7)

    all = performance.objects.filter(cdate__gt=last_time)

    date, cpu_use, mem_use, in_use, out_use = [], [], [], [], []

    for i in all:
        if i.server_id == int(nid):
            date.append(i.cdate.strftime("%m-%d %H:%M"))
            cpu_use.append(i.cpu_use)
            mem_use.append(i.mem_use)
            in_use.append(i.in_use)
            out_use.append(i.out_use)

    if cpu_use:
        cpu_data = cpu_use[-1]
        mem_data = mem_use[-1]
    else:
        cpu_data = 0
        mem_data = 0

    cpu = Gauge_cpumem(attr="CPU", data=cpu_data)
    mem = Gauge_cpumem(attr="内存", data=mem_data)
    network = Line_network(d="kb/s", title="进流量", title1="出流量", date=date, network_in=in_use, network_put=mem_use)
    history_cpumem = Line_network(d="%", title="CPU", title1="内存", date=date, network_in=cpu_use, network_put=mem_use)
    context = dict(
        cpu=pyecharts_add(cpu.render_embed())[0],
        mem=pyecharts_add(mem.render_embed())[0],
        network=pyecharts_add(network.render_embed())[0],
        history_cpumem=pyecharts_add(history_cpumem.render_embed())[0],
        script_list=cpu.get_js_dependencies(),
        asset_active="active",
        asset_list_active="active",
        onresize=" <script>  window.onresize = function () {  %s %s  %s  %s };  </script>" % (
        pyecharts_add(cpu.render_embed())[1], pyecharts_add(mem.render_embed())[1],
        pyecharts_add(network.render_embed())[1], pyecharts_add(history_cpumem.render_embed())[1],)
    )

    return HttpResponse(template.render(context, request))


class SystemUserListAll(TemplateView):
    template_name = 'asset/system-user.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SystemUserListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "system_user_list_active": "active",
            'user_list': get_objects_for_user(self.request.user, 'asset.read_system_users')
        }
        kwargs.update(context)
        return super(SystemUserListAll, self).get_context_data(**kwargs)


@login_required(login_url="/login.html")
@permission_required_or_403('add_system_users')
def system_user_add(request):
    if request.method == 'POST':
        form = SystemUserForm(request.POST)
        if form.is_valid():
            system_save = form.save()

            password1 = encrypt_p(form.cleaned_data['password'])
            system_save.password = password1
            system_save.save()

            myproduct = system_users.objects.get(name=form.cleaned_data['name']).product_line
            mygroup = Group.objects.get(name=myproduct)
            GroupObjectPermission.objects.assign_perm("read_system_users", mygroup, obj=system_save)
            GroupObjectPermission.objects.assign_perm("add_system_users", mygroup, obj=system_save)
            GroupObjectPermission.objects.assign_perm("change_system_users", mygroup, obj=system_save)
            GroupObjectPermission.objects.assign_perm("delete_system_users", mygroup, obj=system_save)

            form = SystemUserForm()
            return render(request, 'asset/system-user.html',
                          {"asset_active": "active",
                           "system_user_list_active": "active",
                           'user_list': get_objects_for_user(request.user, 'asset.read_system_users')})
    else:
        form = SystemUserForm()
    return render(request, 'asset/system-user-add.html',
                  {'form': form, "asset_active": "active", "system_user_list_active": "active", })


@login_required(login_url="/login.html")
@permission_required_or_403('change_system_users', (system_users, 'id', 'nid'))
def system_user_update(request, nid):
    system_user = get_object_or_404(system_users, id=nid)

    if request.method == 'POST':
        form = SystemUserForm(request.POST, instance=system_user)
        old_product_line = system_users.objects.get(id=nid).product_line
        old_mygroup = Group.objects.get(name=old_product_line)

        if form.is_valid():
            password = form.cleaned_data['password']
            myproduct = form.cleaned_data['product_line']
            if password != None:

                system_save = form.save()
                password1 = encrypt_p(form.cleaned_data['password'])
                system_save.password = password1
                system_save.save()

                if old_product_line != myproduct:


                    mygroup = Group.objects.get(name=myproduct)

                    GroupObjectPermission.objects.remove_perm("read_system_users", old_mygroup, obj=system_save)
                    GroupObjectPermission.objects.assign_perm("add_system_users", old_mygroup, obj=system_save)
                    GroupObjectPermission.objects.assign_perm("change_system_users", old_mygroup, obj=system_save)
                    GroupObjectPermission.objects.assign_perm("delete_system_users", old_mygroup, obj=system_save)

                    GroupObjectPermission.objects.assign_perm("read_system_users", mygroup, obj=system_save)
                    GroupObjectPermission.objects.assign_perm("add_system_users", mygroup, obj=system_save)
                    GroupObjectPermission.objects.assign_perm("change_system_users", mygroup, obj=system_save)
                    GroupObjectPermission.objects.assign_perm("delete_system_users", mygroup, obj=system_save)

                    form = AssetForm()
            else:

                s = system_users.objects.get(id=nid)
                password_old = system_users.objects.get(id=nid).password
                old_product_line = system_users.objects.get(id=nid).product_line
                s = form.save()
                s.password = password_old
                s.save()

                if old_product_line != myproduct:


                    mygroup = Group.objects.get(name=myproduct)

                    GroupObjectPermission.objects.remove_perm("read_system_users", old_mygroup, obj=s)
                    GroupObjectPermission.objects.assign_perm("add_system_users", old_mygroup, obj=s)
                    GroupObjectPermission.objects.assign_perm("change_system_users", old_mygroup, obj=s)
                    GroupObjectPermission.objects.assign_perm("delete_system_users", old_mygroup, obj=s)

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


class SystemUserDelete(View):
    model = system_users

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SystemUserDelete, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            id = request.POST.get("nid", None)
            user = User.objects.get(username=request.user)
            checker = ObjectPermissionChecker(user)
            system_u = system_users.objects.get(id=id)

            if checker.has_perm('delete_system_users', system_u) == True:
                system_u.delete()


        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,没有权限{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
@permission_required_or_403('read_system_users', (system_users, 'id', 'nid'))
def system_user_detail(request, nid):
    detail = system_users.objects.get(id=nid)

    return render(request, "asset/system-user-detail.html",
                  {"system_users": detail, "nid": nid, "asset_active": "active",
                   "system_user_list_active": "active"})


@login_required(login_url="/login.html")
@permission_required_or_403('read_system_users', (system_users, 'id', 'nid'))
def system_user_asset(request, nid):
    obj = asset.objects.filter(system_user=nid)
    return render(request, "asset/system-user-asset.html", {"nid": nid, "asset_list": obj,
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


@login_required(login_url="/login.html")
@permission_required_or_403('asset.read_asset')
def export(request):
    if request.method == "GET":
        a = asset.objects.all()

        bt = ['主机名', '外网IP', '管理IP', '内网IP', 'ssh端口', '型号', '系统版本', "网卡1mac地址", "网卡2mac地址", "网卡3mac地址", "网卡4mac地址",
              '登陆用户', '数据中心', '机柜', '位置', '序列号', 'CPU', '内存', "硬盘", "上联端口", "出厂时间", "到保时间", '产品线', '是否启用', "备注"
            , '创建时间', '更新时间', ]

        wb = xlwt.Workbook(encoding='utf-8')
        sh = wb.add_sheet("详情")

        dateFormat = xlwt.XFStyle()
        dateFormat.num_format_str = 'yyyy/mm/dd'

        for i in range(len(bt)):
            sh.write(0, i, bt[i])

        for i in range(len(a)):
            sh.write(i + 1, 0, a[i].hostname)
            sh.write(i + 1, 1, a[i].network_ip)
            sh.write(i + 1, 2, a[i].manage_ip)
            sh.write(i + 1, 3, a[i].inner_ip)
            sh.write(i + 1, 4, a[i].port)
            sh.write(i + 1, 5, a[i].model)
            sh.write(i + 1, 6, a[i].system)
            sh.write(i + 1, 7, a[i].eth0)
            sh.write(i + 1, 8, a[i].eth1)
            sh.write(i + 1, 9, a[i].eth2)
            sh.write(i + 1, 10, a[i].eth3)
            sh.write(i + 1, 11, a[i].system_user.name)
            sh.write(i + 1, 12, a[i].data_center.data_center_list)
            sh.write(i + 1, 13, a[i].cabinet)
            sh.write(i + 1, 14, a[i].position)
            sh.write(i + 1, 15, a[i].sn)
            sh.write(i + 1, 16, a[i].cpu)
            sh.write(i + 1, 17, a[i].memory)
            sh.write(i + 1, 18, a[i].disk)
            sh.write(i + 1, 19, a[i].uplink_port)
            sh.write(i + 1, 20, a[i].ship_time, dateFormat)
            sh.write(i + 1, 21, a[i].end_time, dateFormat)
            sh.write(i + 1, 22, a[i].product_line.name)
            sh.write(i + 1, 23, a[i].is_active)
            sh.write(i + 1, 24, a[i].ps)
            sh.write(i + 1, 25, a[i].ctime, dateFormat)
            sh.write(i + 1, 26, a[i].utime, dateFormat)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=asset' + time.strftime('%Y%m%d', time.localtime(
            time.time())) + '.xls'
        wb.save(response)

        return response
