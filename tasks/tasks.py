from celery import Celery, platforms
from asset.models import asset,performance
from tasks.views import ssh
import threading,time,datetime
from names.password_crypt import decrypt_p


platforms.C_FORCE_ROOT = True

app = Celery('my_task')
app.config_from_object('django.conf:settings',)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



def   job(id):  ##计划任务

    i = asset.objects.filter(id=id).first()
    password = decrypt_p(i.system_user.password)

    cpu1 = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=password, cmd=" top -bn 1 -i -c | grep Cpu   ")

    cpu2 = cpu1['data'].split()

    cpu3 = cpu2[1].split('%')
    cpu4 = cpu2[3].split('%')

    cpu = str(float(str(cpu3[0])) + float(str(cpu4[0])))


    total = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=password, cmd=" free | grep  Mem:  ")
    list = total['data'].split(" ")
    while '' in list:
        list.remove('')
    mem = float('%.2f' % (float('%.3f' % (int(list[2]) / int(list[1]))) * 100))


    in1 = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=password, cmd="cat /proc/net/dev  |  grep eth0  ")
    in2 = in1['data'].split()

    time.sleep(1)

    in3 = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=password,cmd="cat /proc/net/dev  |  grep eth0  ")
    in4 = in3['data'].split()

    in_network = int((int(in4[1]) - int(in2[1]))/1024/10*8)
    out_network = int((int(in4[9]) - int(in2[9]))/1024/10*8)
    performance.objects.create(server_id=i.id, cpu_use=cpu, mem_use=mem,in_use=in_network,out_use=out_network)


@app.task()
def  ansbile():   ##如果想异步调用 ansible api,请在任务前面添加如下


    from multiprocessing import current_process
    # try:
    #     current_process()._config
    # except AttributeError:
    current_process()._config = {'semprefix': '/mp'}




@app.task()
def monitor_job():
    object = asset.objects.all()
    i_list = []
    for i in object:
        i_list.append(i.id)


    print(i_list)

    t_list = []
    for i in i_list:
        t = threading.Thread(target=job, args=[i, ])
        t.start()
        t_list.append(t)
    for i in t_list:
        i.join()



@app.task()
def  cmd_job(host,cmd):
    i = asset.objects.get(network_ip=host)
    password = decrypt_p(i.system_user.password)
    ret = ssh(ip=i.network_ip, port=i.port, username=i.system_user.username, password=password, cmd=cmd)
    return  ret['data']




@app.task()
def  clean_history_host_monitor():
    now = datetime.datetime.now()
    last_time = now + datetime.timedelta(days=-7)
    a = performance.objects.filter(cdate__lt=last_time).delete()


def test():  ##  下面是异步调用 celery 的例子

    from tasks.tasks import cmd_job

    aa = cmd_job.apply_async(args=('43.241.238.109', 'pwd'))
    print("id",aa.task_id,"返回值",aa.get() ,aa.result, "状态",aa.state)

    from  djcelery.models import TaskMeta
    b = TaskMeta.objects.get(task_id=aa).result
    print("返回值",b)