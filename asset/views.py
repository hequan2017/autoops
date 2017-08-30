from  django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import permission_required, login_required
from  asset.models import asset,product_lines,data_centers
import json


def  index(request):
    return   render(request,'index.html')

def  asset_info(request):
    obj = asset.objects.all()
    return   render(request,'asset/asset.html',{'asset_list':obj})



def  asset_add(request):
    if request.method == "POST":
        network_ip = request.POST.get('network_ip', None)
        manage_ip = request.POST.get('manage_ip', None)
        model = request.POST.get('model', None)
        data_center = request.POST.get('data_center', None)
        cabinet = request.POST.get('cabinet', None)
        position = request.POST.get('position', None)
        sn = request.POST.get('sn', None)
        cpu = request.POST.get('cpu', None)
        memory = request.POST.get('memory', None)
        disk = request.POST.get('disk', None)
        port = request.POST.get('port', None)
        use = request.POST.get('use', None)
        ship_time = request.POST.get('ship_time', None)
        end_time = request.POST.get('end_time', None)
        product_line = request.POST.get('product_line', None)
        ps = request.POST.get('ps', None)


        try:
             obj = asset.objects.create(network_ip=network_ip,manage_ip=manage_ip,model=model,data_center=data_center,cabinet=cabinet,
                                   position=position,sn=sn,cpu=cpu,memory=memory,disk=disk,port=port,use=use,ship_time=ship_time,
                                   end_time=end_time,product_line=product_line,ps=ps)

             msg = "添加成功"
        except Exception as  e :
             msg = "添加失败,{}".format(e)
        finally:
            product_line_list = product_lines.objects.all()
            data_center_list = data_centers.objects.all()
            return render(request, 'asset/asset-add.html',
                          {"product_line_list": product_line_list, "data_center_list": data_center_list,'msg':msg })
    else:
        product_line_list = product_lines.objects.all()
        data_center_list = data_centers.objects.all()
        return render(request, 'asset/asset-add.html', {"product_line_list":  product_line_list,"data_center_list":data_center_list})