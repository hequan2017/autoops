from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from    django.utils.decorators import method_decorator
from  library.models import  librarys
from .form import  LibrarysForm
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



class LibraryListAll(TemplateView):
    template_name = 'library/library.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LibraryListAll, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        obj = librarys.objects.all()
        context = {
            "library_active": "active",
            "library_list_active": "active",
            'library_list': obj,
        }
        kwargs.update(context)
        return super(LibraryListAll, self).get_context_data(**kwargs)





class LibraryAdd(CreateView,View):
    model = librarys
    form_class = LibrarysForm
    template_name = 'library/library-add.html'
    success_url = reverse_lazy('library:library_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LibraryAdd, self).dispatch(*args, **kwargs)

    def form_valid(self,form,):
        self.lib_save = lib_save = form.save()

        return super(LibraryAdd, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = {
            "library_active": "active",
            "library_list_active": "active",
            
        }
        kwargs.update(context)
        return super(LibraryAdd, self).get_context_data(**kwargs)
    
    
class LibraryUpdate(UpdateView):
    model = librarys
    form_class = LibrarysForm
    template_name = 'library/library-update.html'
    success_url = reverse_lazy('library:library_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LibraryUpdate, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        self.lib_save  = form.save()
        return super(LibraryUpdate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(LibraryUpdate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = {
            "library_active": "active",
            "library_list_active": "active",
        }
        kwargs.update(context)
        return super(LibraryUpdate, self).get_context_data(**kwargs)

    def get_success_url(self):
        return super(LibraryUpdate, self).get_success_url()

class LibraryDetail(DetailView):
    model = librarys
    template_name = 'library/library-detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LibraryDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = librarys.objects.get(id=pk)
        context = {
            "library_active": "active",
            "library_list_active": "active",
            "librarys": detail,
            "nid": pk,
        }
        kwargs.update(context)
        return super(LibraryDetail, self).get_context_data(**kwargs)












class LibraryDel(View):
    model = librarys
    form_class = LibrarysForm


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LibraryDel, self).dispatch(*args, **kwargs)

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            id = request.POST.get('nid', None)
            lib = librarys.objects.get(id=id)
            lib.delete()
            print(ret)
        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,{}'.format(e)
            }
        return HttpResponse(json.dumps(ret))
