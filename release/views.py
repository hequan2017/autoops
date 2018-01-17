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
            c = codebase.objects.get(id=id)
            path = c.file.url
            path2 = path[1:]
            os.remove(path2)
            c.delete()

        except Exception as e:
            ret = {
                "static": False,
                "error": '删除请求错误,{}'.format(e)
            }
        finally:
            return HttpResponse(json.dumps(ret))