from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from asset.models import asset, system_users, performance
from .form import AssetForm, SystemUserForm
import json

from  tasks.ansible_runner.runner   import AdHocRunner
from tasks.views import ssh

asset_active = "active"
asset_list_active = "active"
system_user_list_active = "active"


def asset_list(request):
	obj = asset.objects.all()
	return render(request, 'asset/asset.html',
	              {'asset_list': obj, "asset_active": asset_active, "asset_list_active": asset_list_active})


def asset_add(request):
	if request.method == 'POST':
		form = AssetForm(request.POST)
		if form.is_valid():
			asset_save = form.save()
			form = AssetForm()
			return render(request, 'asset/asset-add.html',
			              {'form': form, "asset_active": asset_active, "asset_list_active": asset_list_active,
			               "msg": "添加成功"})
	else:
		form = AssetForm()
	return render(request, 'asset/asset-add.html',
	              {'form': form, "asset_active": asset_active, "asset_list_active": asset_list_active})


def asset_update(request, nid):
	asset_id = get_object_or_404(asset, id=nid)
	
	if request.method == 'POST':
		form = AssetForm(request.POST, instance=asset_id)
		if form.is_valid():
			asset_save = form.save()
			return redirect('asset.html')
	
	form = AssetForm(instance=asset_id)
	return render(request, 'asset/asset-update.html',
	              {'form': form, 'nid': nid, "asset_active": asset_active, "asset_list_active": asset_list_active})


def asset_del(request):
	ret = {'status': True, 'error': None, }
	if request.method == "POST":
		try:
			id_1 = request.POST.get("nid", None)
			asset_a = asset.objects.get(id=id_1).delete()
		except Exception as e:
			ret['status'] = False
			ret['error'] = '删除请求错误,{}'.format(e)
		return HttpResponse(json.dumps(ret))


def asset_all_del(request):
	ret = {'status': True, 'error': None, }
	if request.method == "POST":
		try:
			ids = request.POST.getlist('id', None)
			idstring = ','.join(ids)
			asset.objects.extra(where=['id IN (' + idstring + ')']).delete()
		except Exception as e:
			ret['status'] = False
			ret['error'] = '删除请求错误,{}'.format(e)
		return HttpResponse(json.dumps(ret))


def asset_detail(request, nid):
	asset_id = get_object_or_404(asset, id=nid)
	detail = asset.objects.get(id=nid)
	
	return render(request, "asset/asset-detail.html", {"assets": detail, "nid": nid,
	                                                   "asset_active": asset_active,
	                                                   "asset_list_active": asset_list_active})


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
			print(data)
			hostname = data['ansible_nodename']
			system = data['ansible_distribution'] + " " + data['ansible_distribution_version']
			disk = str(sum([int(data["ansible_devices"][i]["sectors"]) * \
			                int(data["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024 \
			                for i in data["ansible_devices"] if i[0:2] in ("vd", "ss", "sd")])) + str(" GB")
			
			memory = '{} MB'.format(data['ansible_memtotal_mb'])
			sn = data['ansible_product_serial']
			model = data['ansible_product_name']
			cpu = data['ansible_processor'][1] + " {}核".format(data['ansible_processor_count'])
			ass = asset.objects.filter(id=id).update(hostname=hostname, system=system, memory=memory,
			                                         disk=disk, sn=sn, model=model, cpu=cpu)
		
		except Exception as e:
			ret['status'] = False
			ret['error'] = '硬件更新错误{}'.format(e)
		return HttpResponse(json.dumps(ret))


def asset_web_ssh(request):
	if request.method == 'POST':
		id = request.POST.get('id', None)
		obj = asset.objects.get(id=id)
		ip = obj.network_ip + ":" + str(obj.port)
		username = obj.system_user.username
		password = obj.system_user.password
		ret = {"ip": ip, "username": username, 'password': password, "static": True}
		return HttpResponse(json.dumps(ret))


def asset_performance(request, nid):
	try:
		i = asset.objects.get(id=nid)
		# cpu_1 = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=i.system_user.password, cmd=" top -bn 1 -i -c | grep Cpu   ")
		# cpu_2 = cpu_1['data'].split()
		# cpu = cpu_2[1].split('%')[0]
		#
		# total = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=i.system_user.password, cmd=" free | grep  Mem:  ")
		# list = total['data'].split(" ")
		# while '' in list:
		#     list.remove('')
		# mem = float('%.2f' % (int(list[2]) / int(list[1]))) * 100
		cpu = 1
		mem = 2
		
		all = performance.objects.all()
		date, cpu_use, mem_use, in_use, out_use = [], [], [], [], []
		
		for i in all:
			if i.server_id == int(nid):
				date.append(i.cdate.strftime("%m-%d %H:%M"))
				cpu_use.append(i.cpu_use)
				mem_use.append(i.mem_use)
				in_use.append(i.in_use)
				out_use.append(i.out_use)
		
		return render(request, 'asset/asset-performance.html', {'cpu': cpu, 'mem': mem, "asset_id": id,
		                                                        'date': date, 'cpu_use': cpu_use, 'mem_use': mem_use,
		                                                        'in_use': in_use, 'out_use': out_use,
		                                                        "asset_active": asset_active,
		                                                        "asset_list_active": asset_list_active})
	
	except Exception as e:
		obj = asset.objects.all()
		error = "错误,{}".format(e)
		return render(request, 'asset/asset.html',
		              {'asset_list': obj, "asset_active": asset_active, "asset_list_active": asset_list_active,
		               "error_performance": error})


def system_user_list(request):
	obj = system_users.objects.all()
	return render(request, 'asset/system-user.html',
	              {'asset_list': obj, "asset_active": asset_active, "system_user_list_active": system_user_list_active})


def system_user_add(request):
	if request.method == 'POST':
		form = SystemUserForm(request.POST)
		if form.is_valid():
			assets_save = form.save()
			form = SystemUserForm()
			return render(request, 'asset/system-user-add.html',
			              {'form': form, "asset_active": asset_active,
			               "system_user_list_active": system_user_list_active,
			               "msg": "添加成功"})
	else:
		form = SystemUserForm()
	return render(request, 'asset/system-user-add.html',
	              {'form': form, "asset_active": asset_active, "system_user_list_active": system_user_list_active, })


def system_user_update(request, nid):
	system_user = get_object_or_404(system_users, id=nid)
	
	if request.method == 'POST':
		form = SystemUserForm(request.POST, instance=system_user)
		if form.is_valid():
			system_user_save = form.save()
			return redirect('system-user.html')
	
	form = SystemUserForm(instance=system_user)
	password = system_users.objects.get(id=nid).password
	print(password)
	return render(request, 'asset/system-user-update.html', {'form': form, 'nid': nid, "asset_active": asset_active,
	                                                         "system_user_list_active": system_user_list_active,
	                                                         "pass": password})


def system_user_del(request):
	ret = {'status': True, 'error': None, }
	if request.method == "POST":
		try:
			id = request.POST.get("nid", None)
			obj = system_users.objects.get(id=id).delete()
		except Exception as e:
			ret['status'] = False
			ret['error'] = '删除请求错误,{}'.format(e)
		return HttpResponse(json.dumps(ret))


def system_user_detail(request, nid):
	system_user = get_object_or_404(system_users, id=nid)
	detail = system_users.objects.get(id=nid)
	return render(request, "asset/system-user-detail.html",
	              {"system_users": detail, "nid": nid, "asset_active": asset_active,
	               "system_user_list_active": system_user_list_active})


def system_user_asset(request, nid):
	sys = system_users.objects.get(id=nid)
	obj = asset.objects.filter(system_user=nid)
	return render(request, "asset/system-user-asset.html", {"system_users": sys, "nid": nid, "asset_list": obj,
	                                                        "asset_active": asset_active,
	                                                        "system_user_list_active": system_user_list_active})
