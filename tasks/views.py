from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from asset.models import asset
from .models import history, toolsscript
import paramiko, json, os, pymysql
from .form import ToolForm
from guardian.shortcuts import get_objects_for_user, get_objects_for_group
from django.contrib.auth.models import User
from guardian.core import ObjectPermissionChecker
from  db.models import db_mysql, db_user
from guardian.decorators import permission_required_or_403
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView, DeleteView, DetailView
import datetime
import decimal


from   tasks.ansible_2420.runner import AdHocRunner, CommandRunner
from  tasks.ansible_2420.inventory import BaseInventory


from  autoops import settings
from names.password_crypt import decrypt_p




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
        obj = get_objects_for_user(request.user, 'asset.change_asset')
        return render(request, 'tasks/cmd.html', {'asset_list': obj, "tasks_active": "active", "cmd_active": "active"})

    if request.method == 'POST':
        ids = request.POST.getlist('id')
        args = request.POST.getlist('args', None)
        module =request.POST.getlist('module', None)

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
        elif   args == ['']   :
            error_2 = "请输入命令"
            ret = {"error": error_2, "status": False}
            return HttpResponse(json.dumps(ret))
        obj = asset.objects.extra(where=['id IN (' + idstring + ')'])
        ret = {'data':[]}
        tasks=[]

        for   x  in range(len(module)):
           tasks.append({"action": {"module": module[x], "args": args[x]}, "name": 'task{}'.format(x)},)


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
                inventory = BaseInventory(assets)
                runner = AdHocRunner(inventory)
                retsult = runner.run(tasks, "all")

                ret1=[]

                for c  in range(len(module)):

                    try:
                        ret1.append(retsult.results_raw['ok']['host']['task{}'.format(c)]['stdout'])
                    except Exception as e:
                        if retsult.results_summary['dark'] == [''] :
                            ret1.append("执行成功")
                        else:
                            ret1.append("命令有问题,{}".format(retsult.results_summary['dark']))

                history.objects.create(ip=i.network_ip, root=i.system_user, port=i.port, cmd=args, user=user)

                ret2={'ip':i.network_ip,'data':'\n'.join(ret1)}
                ret['data'].append(ret2)

            except Exception as e:
                ret['data'].append({"ip": i.network_ip, "data": "账号密码不对,{}".format(e)})

        return HttpResponse(json.dumps(ret))


class ToolsListAll(TemplateView):
    template_name = 'tasks/tools.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ToolsListAll, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        obj = toolsscript.objects.all()
        context = {
            "tasks_active": "active",
            "tools_active": "active",
            'tools': obj
        }
        kwargs.update(context)
        return super(ToolsListAll, self).get_context_data(**kwargs)




@login_required(login_url="/login.html")
@permission_required_or_403('tasks.add_toolsscript')
def tools_add(request):
    obj = toolsscript.objects.all()
    if request.method == 'POST':
        form = ToolForm(request.POST)
        if form.is_valid():
            tools_save = form.save()
            form = ToolForm()
            return render(request, 'tasks/tools.html',
                          {'form': form, "tasks_active": "active", "tools_active": "active",'tools': obj })
    else:
        form = ToolForm()
    return render(request, 'tasks/tools-add.html',{'form': form, "tasks_active": "active", "tools_active": "active", })


@login_required(login_url="/login.html")
def tools_update(request, nid):
    tool_id = toolsscript.objects.get(id=nid)

    if request.method == 'POST':
        form = ToolForm(request.POST, instance=tool_id)
        if form.is_valid():
            asset_save = form.save()
            return redirect('tools.html')

    form = ToolForm(instance=tool_id)
    return render(request, 'tasks/tools-update.html',{'form': form, 'nid': nid, "tasks_active": "active", "tools_active": "active", })


@login_required(login_url="/login.html")
def tools_delete(request):
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
def tools_bulk_delte(request):
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
def tools_script_post(request):
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

            user = User.objects.get(username=request.user)
            checker = ObjectPermissionChecker(user)
            ids1 = []
            for i in host_ids:
                assets = asset.objects.get(id=i)
                if checker.has_perm('task_asset', assets, ) == True:
                    ids1.append(i)
                else:
                    error2 = "主机没有权限"
                    ret = {"error": error2, "status": False}
                    return HttpResponse(json.dumps(ret))


            idstring = ','.join(ids1)

            host = asset.objects.extra(where=['id IN (' + idstring + ')'])
            sh = toolsscript.objects.filter(id=sh_id)

            for s in sh:
                if s.tool_run_type == 0:
                    with  open('tasks/script/test.sh', 'w+') as f:
                        f.write(s.tool_script)
                        a = 'tasks/script/{}.sh'.format(s.id)
                    os.system("sed  's/\r//'  tasks/script/test.sh >  {}".format(a))
                elif s.tool_run_type == 1:
                    with  open('tasks/script/test.py', 'w+') as f:
                        f.write(s.tool_script)
                        p = 'tasks/script/{}.py'.format(s.id)
                        os.system("sed 's/\r//'  tasks/script/test.py >  {}".format(p))
                # elif s.tool_run_type == 2:
                #     with  open('tasks/script/test.yml', 'w+') as f:
                #         f.write(s.tool_script)
                #         y = 'tasks/script/{}.yml'.format(s.id)
                #     os.system("sed 's/\r//'  tasks/script/test.yml >  {}".format(y))
                else:
                    ret['status'] = False
                    ret['error'] = '脚本类型错误,只能是shell、python'
                    return HttpResponse(json.dumps(ret))

                data1 = []
                for h in host:
                    try:
                        password = decrypt_p(h.system_user.password)
                        assets = [
                            {
                                "hostname": 'host',
                                "ip": h.network_ip,
                                "port": h.port,
                                "username": h.system_user.username,
                                "password": password,
                            },
                        ]

                        history.objects.create(ip=h.network_ip, root=h.system_user.username, port=h.port, cmd=s.name,
                                               user=user)

                        if s.tool_run_type == 0:
                            tasks1 = [{"action": {"module": "script", "args": "{}".format(a)}, "name": "1"},]
                        elif s.tool_run_type == 1:
                            tasks1 = [{"action": {"module": "script", "args": "{}".format(p)}, "name": "1"}, ]



                        inventory = BaseInventory(assets)
                        runner = AdHocRunner(inventory)

                        retsu = runner.run(tasks1, "all")



                        try:
                            data2 = {'ip': h.network_ip, 'data': retsu.results_raw['ok']['host']['1']['stdout']}
                        except Exception as e:
                            if retsu.results_summary['dark'] == ['']:
                                data2 = {'ip': h.network_ip, 'data': "执行成功"}
                            else:
                                data2 = {'ip': h.network_ip, 'data':"命令有问题,{}".format(retsu.results_summary['dark'])}

                        data1.append(data2)
                    except  Exception as  e:
                        data2['ip'] = h.network_ip
                        data2['data'] = "账号密码不对,或没有权限,请修改  {},  ".format(e)
                        data1.append(data2)
                ret['data'] = data1
                return HttpResponse(json.dumps(ret))

        except Exception as e:
            ret['error'] = '未知错误 {}'.format(e)
            return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def tools_script_get(request, nid):
    if request.method == "GET":
        obj = get_objects_for_user(request.user, 'asset.task_asset')
        sh = toolsscript.objects.filter(id=nid)
        return render(request, 'tasks/tools-script.html', {"asset_list": obj, "sh": sh, "tools_active": "active"})


a = getattr(settings, 'Inception_ip'),
In_ip = str(a[0])
b = getattr(settings, 'Inception_port')
In_port = int(b)


def sql(user, password, host, port, databases, sqls):  ## 审核
    sql = '/*--user={0};--password={1};--host={2};--enable-check;--disable-remote-backup;--port={3};*/\
    inception_magic_start; \
    use {4}; \
    {5}\
    inception_magic_commit;'.format(user, password, host, port,databases, sqls)

    print("----------------审核----------------------")

    try:
        ret = {"ip": host, "data": None}

        conn = pymysql.connect(host=In_ip, user='', passwd='', db='', port=In_port)
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        column_name_max_size = max(len(i[0]) for i in cursor.description)
        row_num = 0

        data = []

        for result in results:
            row_num = row_num + 1
            data.append('*'.ljust(27, '*') + str(row_num) + '.row' + '*'.ljust(27, '*') + '\n')

            row = map(lambda x, y: (x, y), (i[0] for i in cursor.description), result)
            for each_column in row:
                if each_column[0] != 'errormessage':
                    data.append(
                        str(each_column[0].rjust(column_name_max_size)) + " " + ":" + " " + str(each_column[1]) + '\n')
                else:
                    data.append(str(each_column[0].rjust(column_name_max_size)) + " " + ":" + " " + str(
                        each_column[1].replace('\n', '\n'.ljust(column_name_max_size + 4))) + '\n')

        ret['data'] = data

        cursor.close()
        conn.close()
        return ret
    except pymysql.Error as e:
        data = "Mysql Error %d: %s" % (e.args[0], e.args[1])
        ret = {"ip": host, "data": data}
        return ret


def sql_exe(user, password, host, port,databases, sqls):  ## 执行
    sql = '/*--user={0};--password={1};--host={2};--execute=1;--enable-execute;--enable-ignore-warnings;--port={3};*/\
    inception_magic_start;\
    use {4}  ; \
    {5}\
    inception_magic_commit;'.format(user, password, host, port,databases, sqls)

    print("----------------执行----------------------")
    try:
        ret = {"ip": host, "data": None}

        conn = pymysql.connect(host=In_ip, user='', passwd='', db='', port=In_port)
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        column_name_max_size = max(len(i[0]) for i in cursor.description)
        row_num = 0

        data = []

        for result in results:
            row_num = row_num + 1
            data.append('*'.ljust(27, '*') + str(row_num) + '.row' + '*'.ljust(27, '*') + '\n')

            row = map(lambda x, y: (x, y), (i[0] for i in cursor.description), result)
            for each_column in row:
                if each_column[0] != 'errormessage':
                    data.append(
                        str(each_column[0].rjust(column_name_max_size)) + " " + ":" + " " + str(each_column[1]) + '\n')
                else:
                    data.append(str(each_column[0].rjust(column_name_max_size)) + " " + ":" + " " + str(
                        each_column[1].replace('\n', '\n'.ljust(column_name_max_size + 4))) + '\n')

        ret['data'] = data
        cursor.close()
        conn.close()
        return ret

    except pymysql.Error as e:
        data = "Mysql Error %d: %s" % (e.args[0], e.args[1])
        ret = {"ip": host, "data": data}
        return ret


inception_password = getattr(settings, 'inception_remote_system_password'),
inception_user = getattr(settings, 'inception_remote_system_user'),
inception_port = getattr(settings, 'inception_remote_backup_port'),
inception_host = getattr(settings, 'inception_remote_backup_host'),

inception_remote_system_password = str(inception_password[0])
inception_remote_system_user = str(inception_user[0])
inception_remote_backup_port = str(inception_port[0])
inception_remote_backup_host = str(inception_host[0])


def sql_rb(user, password, host, port, sequence, backup_dbname):  ##   查询回滚语句的表格

    port_a = int(port)
    connection = pymysql.connect(host=host, port=port_a, user=user, password=password, db=backup_dbname, charset="utf8",
                                 cursorclass=pymysql.cursors.DictCursor)
    connection1 = pymysql.connect(host=host, port=port_a, user=user, password=password, db=backup_dbname,
                                  charset="utf8",
                                  cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:

            sql = " select  tablename   from  {0}.{1}  where opid_time ='{2}' ;".format(backup_dbname,  '$_$inception_backup_information$_$',sequence)
            cursor.execute(sql)
            result = cursor.fetchone()
            connection.commit()
            connection.close()
        table = result['tablename']

        try:
            with connection1.cursor() as cursor1:
                sql = " select rollback_statement  from  {0}.{1}  where opid_time = '{2}' ;".format(backup_dbname, table,sequence)
                cursor1.execute(sql)
                result1 = cursor1.fetchone()
                connection1.commit()
                connection1.close()


            ret = {"data": result1['rollback_statement']}
            return ret

        except Exception as e:
            data = "Mysql Error %d: %s" % (e.args[0], e.args[1])
            ret = {"data": data}
            return ret

    except Exception as e:
        data = "Mysql Error %d: %s" % (e.args[0], e.args[1])
        ret = data
        return ret



class DateEncoder(json.JSONEncoder ):  ## 格式化查询返回的内容
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, datetime.date):
                return obj.strftime('%Y-%m-%d')
            elif isinstance(obj, decimal.Decimal):
                return str(obj)
            else:
                return json.JSONEncoder.default(self, obj)


class  sql_query(object):  ## 查询接口
    def __init__(self,host,port,user,password,db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db


    def connectmysql(self,sql):# 查询数据库 库名字
        self.conn = pymysql.connect(host=self.host,port=self.port,password=self.password,db=self.db,charset='utf8')
        self.cursor = self.conn.cursor(pymysql.cursors.SSCursor)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.conn.commit()
        self.conn.close()
        desc = self.cursor.description
        return result

    def connectmysql_select(self, sql):# 查询数据库
        self.conn = pymysql.connect(host=self.host, port=self.port, password=self.password, db=self.db, charset='utf8')
        self.cursor = self.conn.cursor(pymysql.cursors.SSCursor)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.conn.commit()
        self.conn.close()
        # desc = self.cursor.description

        column_name_max_size = max(len(i[0]) for i in self.cursor.description)
        data = []

        for result in result:
            row = map(lambda x, y: (x, y), (i[0] for i in self.cursor.description), result)
            for each_column in row:
                    data.append(str(each_column[0].rjust(column_name_max_size)) + " " + ":" + " " + str(
                        each_column[1]))
        return data



@login_required(login_url="/login.html")
def Inception_query_databases(request):  ##Inception 查询 数据库 名字

    if request.method == 'POST':
        ids = request.POST.getlist('id')
        user = User.objects.get(username=request.user)
        checker = ObjectPermissionChecker(user)
        ids1 = []
        for i in ids:
            assets = db_mysql.objects.get(id=i)
            if checker.has_perm('task_db_mysql', assets, ) == True:
                ids1.append(i)
            else:
                error_3 = "数据库没有权限"
                ret = {"error": error_3, "status": False}
                return HttpResponse(json.dumps(ret))



        user = request.user
        idstring = ','.join(ids1)
        if not ids:
            error_1 = "请选择数据库"
            ret = {"error": error_1, "status": False}
            return HttpResponse(json.dumps(ret))


        obj = db_mysql.objects.extra(where=['id IN (' + idstring + ')'])
        ret = {}
        ret['data'] = []

        for i in obj:
            try:
                history.objects.create(ip=i.ip, root=i.db_user.username, port=i.port,
                                                  cmd="查询数据库库名字".format(), user=user)

                password = decrypt_p(i.db_user.password)

                a = sql_query(user=i.db_user.username, password=password, host=i.ip, port=i.port,db='mysql')
                s1 = a.connectmysql(sql="select SCHEMA_NAME from information_schema.SCHEMATA;")

                s2 = []
                for  z  in  s1:
                        s2.append(z[0])

                s = {'ip':i.ip,'data':s2}
                ret['data'].append(s)

            except Exception as e:
                ret['data'].append({"ip": i.ip, "data": "账号密码不对,{}".format(e)})
        return HttpResponse(json.dumps(ret))




@login_required(login_url="/login.html")
def Inception_query(request):  ##查询数据库

    if request.method == 'POST':
        ids = request.POST.getlist('id')

        sqls = request.POST.get('sql')
        db = request.POST.get('databases')


        sqls1= sqls.split(';')

        for s in sqls1:
            if '' in sqls1:
                sqls1.remove('')

        for j in range(len(sqls1)):
            j1 = sqls1[j].strip()[:4]
            if j1 == 'show'   or j1 == 'sele'  or j1 == 'desc' :
                break
            else:
                rets = {"error": "输入的命令有误，禁止使用非 select , show,desc", "status": False}
                return HttpResponse(json.dumps(rets))


        user = User.objects.get(username=request.user)
        checker = ObjectPermissionChecker(user)
        ids1 = []
        for i in ids:
            assets = db_mysql.objects.get(id=i)
            if checker.has_perm('task_db_mysql', assets, ) == True:
                ids1.append(i)
            else:
                error_3 = "数据库没有权限"
                ret = {"error": error_3, "status": False}
                return HttpResponse(json.dumps(ret))
        user = request.user
        idstring = ','.join(ids1)


        if not ids:
            error_1 = "请选择数据库"
            ret = {"error": error_1, "status": False}
            return HttpResponse(json.dumps(ret))
        elif    not sqls:
            error_2 = "请输入要查询的语句"

            ret = {"error": error_2, "status": False}
            return HttpResponse(json.dumps(ret))


        obj = db_mysql.objects.extra(where=['id IN (' + idstring + ')'])
        ret = {}
        ret['data'] = []

        for i in obj:
            try:
                history.objects.create(ip=i.ip, root=i.db_user.username, port=i.port,cmd="查询:{}".format(sqls), user=user)

                password = decrypt_p(i.db_user.password)

                query = sql_query(user=i.db_user.username, password=password, host=i.ip, port=i.port,db=db)
                re = query.connectmysql_select(sql=sqls)

                re2 = json.dumps(re, cls=DateEncoder)
                re4 = re2.split(",")
                re5 = {'ip':i.ip,'data': '\n'.join(re4)}
                ret['data'].append(re5)

            except Exception as e:
                ret['data'].append({"ip": i.ip, "data": "账号密码不对,查询失败{}".format(e)})
        return HttpResponse(json.dumps(ret))



@login_required(login_url="/login.html")
def Inception(request):  ##Inception 审核

    if request.method == "GET":
        obj = get_objects_for_user(request.user, 'db.change_db_mysql')
        return render(request, 'tasks/Inception.html',
                      {'sql_list': obj, "tasks_active": "active", "sql_active": "active"})

    if request.method == 'POST':
        ids = request.POST.getlist('id')
        sql_db = request.POST.get('sql', None)
        databases = request.POST.get('databases', None)

        user = User.objects.get(username=request.user)
        checker = ObjectPermissionChecker(user)
        ids1 = []
        for i in ids:
            assets = db_mysql.objects.get(id=i)
            if checker.has_perm('task_db_mysql', assets, ) == True:
                ids1.append(i)
            else:
                error_3 = "数据库没有权限"
                ret = {"error": error_3, "status": False}
                return HttpResponse(json.dumps(ret))



        user = request.user
        idstring = ','.join(ids1)
        if not ids:
            error_1 = "请选择数据库"
            ret = {"error": error_1, "status": False}
            return HttpResponse(json.dumps(ret))
        elif not sql_db:
            error_2 = "请输入命令"
            ret = {"error": error_2, "status": False}
            return HttpResponse(json.dumps(ret))

        obj = db_mysql.objects.extra(where=['id IN (' + idstring + ')'])
        ret = {}
        ret['data'] = []

        for i in obj:
            try:
                history.objects.create(ip=i.ip, root=i.db_user.username, port=i.port,
                                                  cmd="审核:{0}".format(sql_db), user=user)

                password = decrypt_p(i.db_user.password)

                s = sql(user=i.db_user.username, password=password, host=i.ip, port=i.port,databases=databases,sqls=sql_db)

                if s == None or s['data'] == '':
                    s = {}
                    s['ip'] = i.ip
                    s['data'] = "返回值为空,可能是权限不够。"
                ret['data'].append(s)
            except Exception as e:

                ret['data'].append({"ip": i.ip, "data": "账号密码不对,{0}".format(e)})
        return HttpResponse(json.dumps(ret))









@login_required(login_url="/login.html")
def Inception_exe(request):  ##Inception 执行

    if request.method == 'POST':
        ids = request.POST.getlist('id')
        sql_db = request.POST.get('sql', None)
        databases = request.POST.get('databases', None)




        user = User.objects.get(username=request.user)
        checker = ObjectPermissionChecker(user)
        ids1 = []
        for i in ids:
            assets = db_mysql.objects.get(id=i)
            if checker.has_perm('task_db_mysql',assets, ) == True:
                ids1.append(i)

            else:
                error_3 = "数据库没有权限"
                ret = {"error": error_3, "status": False}
                return HttpResponse(json.dumps(ret))



        user = request.user
        idstring = ','.join(ids1)
        if not ids:
            error_1 = "请选择数据库"
            ret = {"error": error_1, "status": False}
            return HttpResponse(json.dumps(ret))
        elif not sql_db:
            error_2 = "请输入命令"
            ret = {"error": error_2, "status": False}
            return HttpResponse(json.dumps(ret))

        obj = db_mysql.objects.extra(where=['id IN (' + idstring + ')'])
        ret = {}
        ret['data'] = []

        for i in obj:
            try:
                history.objects.create(ip=i.ip, root=i.db_user.username, port=i.port,
                                                  cmd="执行:{}".format(sql_db), user=user)

                password = decrypt_p(i.db_user.password)
                s = sql_exe(user=i.db_user.username, password=password, host=i.ip, port=i.port, databases=databases,sqls=sql_db)

                if s == None or s['data'] == '':
                    s = {}
                    s['ip'] = i.ip
                    s['data'] = "返回值为空,可能是权限不够。"
                ret['data'].append(s)
            except Exception as e:
                ret['data'].append({"ip": i.ip, "data": "账号密码不对,{}".format(e)})
        return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
def Inception_rb(request):  ##Inception  回滚


    if request.method == 'POST':
        sequence = request.POST.get('sequence', None)
        backup_dbname = request.POST.get('backup_dbname', None)

        if not sequence or not backup_dbname:
            error_2 = "请输入  sequence  or backup_dbname  "
            ret = {"error": error_2, "status": False}
            return HttpResponse(json.dumps(ret))

        try:

            s = sql_rb(user=inception_remote_system_user, password=inception_remote_system_password,
                       host=inception_remote_backup_host, port=inception_remote_backup_port,
                       sequence=sequence, backup_dbname=backup_dbname)

            if s == None or s['data'] == '':
                s = {}
                s['data'] = "返回值为空"

            ret = s

        except Exception as e:
            ret = {}
            ret['error'] = "错误： {}".format(e)
        finally:
            return HttpResponse(json.dumps(ret))
