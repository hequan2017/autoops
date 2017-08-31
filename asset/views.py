from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from asset.models import asset, product_lines, data_centers
from .form import PublisherForm


def index(request):
    return render(request, 'index.html')


def asset_info(request):
    obj = asset.objects.all()
    return render(request, 'asset/asset.html', {'asset_list': obj})


def asset_add(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            return HttpResponse('Add	success1')
            # return	redirect('some	view	name')
    else:
        form = PublisherForm()
    return render(request, 'asset/asset-add.html', {'form': form})


def asset_update(request, nid):
    publisher = get_object_or_404(asset, id=nid)

    if request.method == 'POST':
        form = PublisherForm(request.POST,instance=publisher)
        if form.is_valid():
            publisher = form.save()
            return HttpResponse('update 	success')


    form = PublisherForm(instance=publisher)
    return render(request, 'asset/asset-update.html', {'form': form,'nid':nid})
