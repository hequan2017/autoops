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


class LibraryAdd(CreateView):
    model = librarys
    form_class = LibrarysForm
    template_name = 'library/library-add.html'
    success_url = reverse_lazy('asset:asset_list')

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('library.add_library'))
    def dispatch(self, *args, **kwargs):
        return super(LibraryAdd, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.asset_save = asset_save = form.save()
        return super(LibraryAdd, self).form_valid(form)

    def get_success_url(self):
        return super(LibraryAdd, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = {
            "library_active": "active",
            "library_add_active": "active",
        }
        kwargs.update(context)
        return super(LibraryAdd, self).get_context_data(**kwargs)