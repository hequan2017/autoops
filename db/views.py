from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from db.models import db_user,db_mysql
from .form import DbMysqlForm,DbUsersForm
from names.password_crypt import encrypt_p,decrypt_p

from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm, get_perms
from guardian.core import ObjectPermissionChecker
from guardian.decorators import permission_required_or_403

from guardian.shortcuts import get_objects_for_user, get_objects_for_group
from guardian.models import UserObjectPermission, GroupObjectPermission
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy


from django.db.models import Q
import xlwt, time, json




class DbListAll(TemplateView):
    template_name = 'db/db.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DbListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "db_active": "active",
            "db_list_active": "active",
            'db_list': get_objects_for_user(self.request.user, 'db.read_db_mysql')
        }
        kwargs.update(context)
        return super(DbListAll, self).get_context_data(**kwargs)



class DbDetail(DetailView):
    model = db_mysql
    template_name = 'db/db-detail.html'

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('db.read_db_mysql', (db_mysql, 'id', 'pk')))
    def dispatch(self, *args, **kwargs):
        return super(DbDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = db_mysql.objects.get(id=pk)

        context = {
            "db_active": "active",
            "db_list_active": "active",
            "dbs": detail,
            "nid": pk,
        }
        kwargs.update(context)
        return super(DbDetail, self).get_context_data(**kwargs)



class DbAdd(CreateView):
    model = db_mysql
    form_class =  DbMysqlForm
    template_name = 'db/db-add.html'
    success_url = reverse_lazy('db:db_list')

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('db.add_db_mysql'))
    def dispatch(self, *args, **kwargs):
        return super(DbAdd, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.db = db =  form.save()

        myproduct = form.cleaned_data['product_line']
        mygroup = Group.objects.get(name=myproduct)
        GroupObjectPermission.objects.assign_perm("read_db_mysql", mygroup, obj=db)
        GroupObjectPermission.objects.assign_perm("add_db_mysql", mygroup, obj=db)
        GroupObjectPermission.objects.assign_perm("change_db_mysql", mygroup, obj=db)
        GroupObjectPermission.objects.assign_perm("delete_db_mysql", mygroup, obj=db)
        GroupObjectPermission.objects.assign_perm("task_db_mysql", mygroup, obj=db)
        return super(DbAdd, self).form_valid(form)

    def get_success_url(self):
        return super(DbAdd, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = {
            "db_active": "active",
            "db_list_active": "active",
        }
        kwargs.update(context)
        return super(DbAdd, self).get_context_data(**kwargs)



class DbUpdate(UpdateView):
    model = db_mysql
    form_class = DbMysqlForm
    template_name = 'db/db-update.html'
    success_url = reverse_lazy('db:db_list')

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('db.change_db_mysql', (db_mysql, 'id', 'pk')))
    def dispatch(self, *args, **kwargs):
        return super(DbUpdate, self).dispatch(*args, **kwargs)



    def get_context_data(self, **kwargs):
        context = {
            "db_active": "active",
            "db_list_active": "active",
        }
        kwargs.update(context)
        return super(DbUpdate, self).get_context_data(**kwargs)


    def form_invalid(self, form):
        print(form.errors)
        return super(DbUpdate, self).form_invalid(form)



    def form_valid(self, form):

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        old_myproduct = db_mysql.objects.get(id=pk).product_line
        old_mygroup = Group.objects.get(name=old_myproduct)
        new_mygroup = Group.objects.get(name=form.cleaned_data['product_line'])

        self.object = form.save()
        if old_mygroup != new_mygroup:
            GroupObjectPermission.objects.remove_perm("read_db_mysql", old_mygroup, obj=self.object)
            GroupObjectPermission.objects.remove_perm("add_db_mysql", old_mygroup, obj=self.object)
            GroupObjectPermission.objects.remove_perm("change_db_mysql", old_mygroup, obj=self.object)
            GroupObjectPermission.objects.remove_perm("delete_db_mysql", old_mygroup, obj=self.object)
            GroupObjectPermission.objects.remove_perm("task_db_mysql",old_mygroup, obj=self.object)


            GroupObjectPermission.objects.assign_perm("read_db_mysql", new_mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("add_db_mysql", new_mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("change_db_mysql", new_mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("delete_db_mysql", new_mygroup, obj=self.object)
            GroupObjectPermission.objects.assign_perm("task_db_mysql",new_mygroup, obj=self.object)

        return super(DbUpdate, self).form_valid(form)

    def get_success_url(self):
        return super(DbUpdate, self).get_success_url()




class DbDel(View):
    model = db_mysql

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DbDel, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            id = request.POST.get('nid', None)
            dbs = db_mysql.objects.get(id=id)
            user = User.objects.get(username=request.user)

            checker = ObjectPermissionChecker(user)
            if checker.has_perm('delete_asset', dbs) == True:
                dbs.delete()

        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,{}'.format(e)
            }
        finally:
             return HttpResponse(json.dumps(ret))



@login_required(login_url="/login.html")
def db_all_del(request):
    ret = {'status': True, 'error': None, }
    if request.method == "POST":
        try:
            ids = request.POST.getlist('id', None)
            ids1 = []
            for i in ids:
                user = User.objects.get(username=request.user)
                checker = ObjectPermissionChecker(user)
                assets = db_mysql.objects.get(id=i)
                if checker.has_perm('delete_db', assets, ) == True:
                    ids1.append(i)

            idstring = ','.join(ids1)
            db_mysql.objects.extra(where=['id IN (' + idstring + ')']).delete()


        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,{}'.format(e)
        finally:
              return HttpResponse(json.dumps(ret))

class DbUserListAll(TemplateView):
    template_name = 'db/db-user.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DbUserListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "db_active": "active",
            "db_user_active": "active",
            'db_user_list': get_objects_for_user(self.request.user, 'db.read_db_user')
        }
        kwargs.update(context)
        return super(DbUserListAll, self).get_context_data(**kwargs)



class DbUserAdd(CreateView):
    model = db_user
    form_class =  DbUsersForm
    template_name = 'db/db-user-add.html'
    success_url = reverse_lazy('db:db_user_list')

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('db.add_db_user'))
    def dispatch(self, *args, **kwargs):
        return super(DbUserAdd, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.db = db = form.save()

        password1 = encrypt_p(form.cleaned_data['password'])
        db.password = password1
        db.save()

        myproduct =form.cleaned_data['product_line']
        mygroup = Group.objects.get(name=myproduct)
        GroupObjectPermission.objects.assign_perm("read_db_user", mygroup, obj=db)
        GroupObjectPermission.objects.assign_perm("add_db_user", mygroup, obj=db)
        GroupObjectPermission.objects.assign_perm("change_db_user", mygroup, obj=db)
        GroupObjectPermission.objects.assign_perm("delete_db_user", mygroup, obj=db)

        return super(DbUserAdd, self).form_valid(form)

    def get_success_url(self):
        return super(DbUserAdd, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = {
            "db_active": "active",
            "db_user_active": "active",
        }
        kwargs.update(context)
        return super(DbUserAdd, self).get_context_data(**kwargs)


class DbUserUpdate(UpdateView):
    model = db_user
    form_class = DbUsersForm
    template_name = 'db/db-user-update.html'
    success_url = reverse_lazy('db:db_user_list')

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('db.change_db_user', (db_user, 'id', 'pk')))
    def dispatch(self, *args, **kwargs):
        return super(DbUserUpdate, self).dispatch(*args, **kwargs)



    def get_context_data(self, **kwargs):
        context = {
            "db_active": "active",
            "db_user_active": "active",
        }
        kwargs.update(context)
        return super(DbUserUpdate, self).get_context_data(**kwargs)


    def form_invalid(self, form):
        print(form.errors)
        return super(DbUserUpdate, self).form_invalid(form)

    def form_valid(self, form):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        new_password = form.cleaned_data['password']

        old_pro=db_user.objects.get(id=pk).product_line
        myproduct = form.cleaned_data['product_line']


        if new_password != None:
                self.db = db_save = form.save()

                db_save.password = encrypt_p(new_password)
                db_save.save()

                if old_pro != myproduct:

                    old_mygroup = Group.objects.get(name=old_pro)
                    mygroup = Group.objects.get(name=myproduct)
                    GroupObjectPermission.objects.remove_perm("read_db_user", old_mygroup, obj=db_save)
                    GroupObjectPermission.objects.remove_perm("add_db_user", old_mygroup, obj=db_save)
                    GroupObjectPermission.objects.remove_perm("change_db_user", old_mygroup, obj=db_save)
                    GroupObjectPermission.objects.remove_perm("delete_db_user", old_mygroup, obj=db_save)

                    GroupObjectPermission.objects.assign_perm("read_db_user", mygroup, obj=db_save)
                    GroupObjectPermission.objects.assign_perm("add_db_user", mygroup, obj=db_save)
                    GroupObjectPermission.objects.assign_perm("change_db_user", mygroup, obj=db_save)
                    GroupObjectPermission.objects.assign_perm("delete_db_user", mygroup, obj=db_save)


        else:

                password_old = db_user.objects.get(id=pk).password
                self.db = db = form.save()
                db.password = password_old
                db.save()

                if old_pro != myproduct:

                    old_mygroup = Group.objects.get(name=old_pro)
                    mygroup = Group.objects.get(name=myproduct)
                    GroupObjectPermission.objects.remove_perm("read_db_user", old_mygroup, obj=db)
                    GroupObjectPermission.objects.remove_perm("add_db_user", old_mygroup, obj=db)
                    GroupObjectPermission.objects.remove_perm("change_db_user", old_mygroup, obj=db)
                    GroupObjectPermission.objects.remove_perm("delete_db_user", old_mygroup, obj=db)

                    GroupObjectPermission.objects.assign_perm("read_db_user", mygroup, obj=db)
                    GroupObjectPermission.objects.assign_perm("add_db_user", mygroup, obj=db)
                    GroupObjectPermission.objects.assign_perm("change_db_user", mygroup, obj=db)
                    GroupObjectPermission.objects.assign_perm("delete_db_user", mygroup, obj=db)




        return super(DbUserUpdate, self).form_valid(form)

    def get_success_url(self):
        return super(DbUserUpdate, self).get_success_url()


class DbUserDel(View):
    model = db_mysql

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DbUserDel, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            id = request.POST.get('nid', None)
            db = db_user.objects.get(id=id)
            user = User.objects.get(username=request.user)
            checker = ObjectPermissionChecker(user)


            if checker.has_perm('delete_system_users', db) == True:
                db.delete()


        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,{}'.format(e)
            }
        finally:
            return HttpResponse(json.dumps(ret))




class DbUserDetail(DetailView):
    model = db_user
    template_name = 'db/db-user-detail.html'

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('db.read_db_user', (db_user, 'id', 'pk')))
    def dispatch(self, *args, **kwargs):
        return super(DbUserDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = db_user.objects.get(id=pk)
        context = {
            "db_active": "active",
            "db_user_active": "active",
            "dbusers": detail,
            "nid": pk,
        }
        kwargs.update(context)
        return super(DbUserDetail, self).get_context_data(**kwargs)


@login_required(login_url="/login.html")
@permission_required_or_403('db.read_db_user',(db_user, 'id', 'nid'))
def Db_user_db(request, nid):
    obj = db_mysql.objects.filter(db_user=nid)
    return render(request, "db/db-user-db.html", {"nid": nid, "db_list": obj,
                                                            "db_active": "active","db_user_active": "active",})

