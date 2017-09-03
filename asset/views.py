from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from asset.models import asset, product_lines, data_centers
from .form import PublisherForm


def index(request):
    return render(request, 'index.html')


def asset_info(request):
    obj = asset.objects.all()
    asset_active = "active"
    assetinfo_active = "active"
    return render(request, 'asset/asset.html', {'asset_list': obj,"asset_active":asset_active,"assetinfo_active":assetinfo_active})


def asset_add(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            return redirect('asset-add.html')
            # return	redirect('some	view	name')
    else:
        form = PublisherForm()
    asset_active = "active"
    assetadd_active = "active"
    return render(request, 'asset/asset-add.html', {'form': form,"asset_active":asset_active,"assetadd_active":assetadd_active})


def asset_update(request,nid):
    publisher = get_object_or_404(asset, id=nid)

    if request.method == 'POST':
        form = PublisherForm(request.POST,instance=publisher)
        if form.is_valid():
            publisher = form.save()
            return redirect('asset.html')


    form = PublisherForm(instance=publisher)
    asset_active = "active"
    assetinfo_active = "active"
    return render(request, 'asset/asset-update.html', {'form': form,'nid':nid,"asset_active":asset_active,"assetinfo_active":assetinfo_active})

def asset_del(request):
    if request.method == "POST":
        id = request.POST.get("nid",None)
        print(id,"----------------------")
        return HttpResponse(id)
