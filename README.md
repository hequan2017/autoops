# AutoOps

> 🚀 **AutoOps 运维管理平台**  
> 基于 Django 2.0，面向 Linux 运维工程师的一站式资产与运维管理系统。

---

## ⚠️ 项目状态
本项目已停止开发。由于长时间未维护，可能存在部署差异或运行问题，仅供学习参考。  
因作者工作原因，后续不再提供更新与维护。

---

## ✨ 项目简介
AutoOps 提供资产管理、命令行批量执行、流量图监控、Web SSH、技术文档、数据库审核、Docker/K8s 管理等常用运维能力。  
欢迎测试使用，有问题可反馈。

---

## 🌐 Demo & 社区
- 交流群号：`620176501`（欢迎交流）
- 博客：`http://hequan.blog.51cto.com/`
- GitHub：`https://github.com/hequan2017/autoops/`
- 码云：`https://gitee.com/hequan2020/autoops`

---

## 🧭 架构图
![DEMO](static/demo/autoops.png)

---

## 🗺️ 更新记录
- **1.8** 最后一次更新：修改 ansible API 以支持 playbook（需自行测试）
- **1.7.8** 更换后台为 xadmin  
  - 注意：xadmin 暂不支持对象权限（django-guardian），需要时请登录 dadmin（默认 admin）。  
  - tasks 任务名示例：  
    - `tasks.task.任务`
    - `tasks.task.monitor_job`（定时获取 CPU/内存/流量）
    - `tasks.task.clean_history_host_monitor`（清除 1 周前历史记录）
    - `tasks.task.cmd_job`（定时执行命令）
- **1.7.7** 更换 webssh 启动方式  
- **1.7.6** 代码库功能上线，支持分发  
- **1.7.4** 更新 ansible，增强命令行功能  
- **1.6** MySQL 数据库自动审核 + 执行（仅限 MySQL）  
- **1.4** 升级 Django 2.0  
- **1.3** 新增技术文档模块  
- **1.2** 权限管理完善 + 附件上传下载  
- **1.1.5** 权限管理：基于用户组的资源隔离  
- **1.1** 新增平台登录记录、Web 登录记录、密码修改

---

## 🧩 功能概览
| 模块 | 能力要点 |
| --- | --- |
| **资产管理** | 资产信息 API、自动获取服务器信息、导出、CPU/内存/流量图 |
| **用户管理** | 用户模块（预留）、加密解密 `password_crypt.py` |
| **任务中心** | 命令行、工具（Shell/Python） |
| **WebSSH** | 远程登录（参考：https://github.com/huashengdun/webssh） |
| **Docker 管理** | 容器列表、启停/重启操作（Docker API） |
| **K8s 管理** | 集群资源概览（Namespace/Node/Pod/Service/ConfigMap/Secret/Deployment/DaemonSet/StatefulSet/Job/CronJob） |
| **技术文档** | 运维知识库 + 富文本编辑器 DjangoUeditor |
| **代码库** | 代码管理与主机分发 |
| **数据库审核** | Inception 审核/执行/回滚 |
| **后台管理** | xadmin + dadmin，支持基于用户组的资源隔离 |

---

## 🧪 运行环境
- Python 3.6.4（参考 `script/install_python3.6.4.py`）
- Django 2.0
- Python 2.7（用于 supervisor）
- CentOS 7.4
- Docker（可选，用于容器管理）
- Kubernetes（可选，用于集群管理）

> **Supervisor 管理组件**
> - uwsgi / webssh / celeryd / celerybeat / celerycam / celeryflower / Inception

---

## ⚙️ 安装

**开发环境部署**

1. 下载并安装基础环境（默认目录 `/opt`）
 
```bash
cd /opt
yum install git   sshpass    redis  -y 
systemctl enable redis.service 
systemctl start  redis.service 
git  clone  https://github.com/hequan2017/autoops.git
    
cd   autoops/
pip3 install -r requirements.txt       

cd /usr/local/src
wget https://codeload.github.com/sshwsfc/xadmin/zip/django2
unzip django2
cd xadmin-django2/
python setup.py  install

``` 

   添加的资产里面,  建议执行  ` yum install  ipmitool     dmidecode   -y  `以获取更多信息
   
2. 安装 `supervisor`
 
```bash
chmod +x    /opt/autoops/script/inception/bin/*
pip2   install    supervisor          ## 没有pip2 版本的 ，可以参考 script/install_pip2.sh
echo_supervisord_conf    > /etc/supervisord.conf 
mkdir /etc/supervisord.d/
     
vim /etc/supervisord.conf      ##进行相关设置
         
[inet_http_server]             ##HTTP登录账号密码
port=0.0.0.0:9001 
username=user
password=321

[include]
files = /etc/supervisord.d/*.conf
```
```bash
cp   /opt/autoops/script/supervisor.conf               /etc/supervisord.d/        
```
    
 

###  环境设置

  * 数据库: 请修改 `autops/settings`文件, 如果没有mysql，请选择上面那种。如果有，则可以启用mysql，设置相关连接地址。
     关于mysql安装方法，可参考我的博客 `http://hequan.blog.51cto.com/5701886/1982428`


```djangotemplate
DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     }
 }
 
 
DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'autoops',
           'USER': 'root',
           'PASSWORD': '123456',
           'HOST': '192.168.10.24',
           'PORT': '3306',
        }
}
``` 
  * 修改 autoops/settings 自定义参数
  
```djangotemplate
DEBUG = True                            ## 实际生产环境使用，请关闭    False

BROKER_URL = 'redis://127.0.0.1:6379/0'                  ##Redis地址,一般情况不用修改


Webssh_ip = '114.115.132.147'      ##WebSSH 软件的 访问IP,也就是本机外网IP，改这个地方就好了。
Webssh_port='9000'             ##端口号,默认即可。如有修改，需要修改  webssh/main.py文件 define('port', default=9000, help='listen port', type=int)

Inception_ip = '127.0.0.1'         ## 此为 Inception 软件地址,  默认为本机地址，一般不用修改
Inception_port = '6669'            ## 此为 Inception 软件端口号


inception_remote_system_password='654321'    ## 设置回滚备份（mysql）服务器相关参数，并同步修改一下 script/inc.cnf 里面的设置
inception_remote_system_user='root'
inception_remote_backup_port='3306'
inception_remote_backup_host='192.168.10.100'   ##设置备份数据库地址
```  

  * 修改一个文件 `/usr/local/lib/python3.6/site-packages/django/db/backends/mysql/base.py`   注释35 36 以下两行,找不到可以忽略。
  
```python  
if version < (1, 3, 3):
    raise ImproperlyConfigured("mysqlclient 1.3.3 or newer is required; you have %s" % Database.__version__)
```

  * 由于Inception 并不原生支持pymysql，所以需更改pymysql相关源码。
  
在script/  文件夹下有已经修改的connections.py 和 cursors.py 直接替换即可。  
替换位置为  `/usr/local/lib/python3.6/site-packages/pymysql`  下的 `connections.py 和 cursors.py `   两个文件
注:  如果想知道，修改了哪里，可参考script/备注。

```bash
cp /opt/autoops/script/connections.py   /usr/local/lib/python3.6/site-packages/pymysql/connections.py
cp /opt/autoops/script/cursors.py    /usr/local/lib/python3.6/site-packages/pymysql/cursors.py 
```
 
  * 初始化数据库（可删除文件夹的 db.sqlite3）
  
```bash
python manage.py makemigrations
python manage.py  migrate
python manage.py  createsuperuser             ##创建管理员
``` 
  * autoops 登陆的端口号 在 supervisor.conf  里面 第2行  ,默认是   0.0.0.0:8003 。如有修改端口号，请把supervisor 里的uwsgi  服务关闭,再启动。             
      
  * 启动supervisor进程管理  
```bash
/usr/bin/python2.7   /usr/bin/supervisord -c /etc/supervisord.conf
``` 


加到linux 开机启动里面  `chmod +x  /etc/rc.d/rc.local `  把上面的命令放到这个文件里面  
  
  
  * 启动: 统一用supervisor 管理进程,  打开   0.0.0.0:9001  账号user  密码321   进入进程管理界面，管理uwsgi,webssh,celery,Inception 等启动关闭。
     ![DEMO](static/demo/14.png)


  * 登陆后台，设置定时获取主机图，设置数据中心、用户组。
  
  
  * 设置定时获取主机信息任务。 先创建执行的时间频率，再创建任务，创建后，观察队列任务是否执行成功。   如不成功，重启所有supervisor中的  celery服务。
![DEMO](static/demo/9.png)





---

###  开发设置

  * 如果想在windows 下的 pycharm打开， 先pip 安装好模块，ansbile无法装在windows上，忽略掉。然后注释下面的代码。  注释xadmin
  
  ```djangotemplate
asset/views.py
from   tasks.ansible_2420.runner import AdHocRunner, CommandRunner
from  tasks.ansible_2420.inventory import BaseInventory

tasks/views.py   
from   tasks.ansible_2420.runner import AdHocRunner, CommandRunner
from  tasks.ansible_2420.inventory import BaseInventory

release/views.py
from   tasks.ansible_2420.runner import AdHocRunner
from  tasks.ansible_2420.inventory import BaseInventory
```
    
   
###  生产环境   
   
  * 如果想在生产环境部署、启动, 用nginx去处理。 可以参考   `http://hequan.blog.51cto.com/5701886/1982769` , 请把`supervisor.conf` 中 关于uwsgi的部分删除掉, 
用以下方式控制UWSGI的启动 关闭.

```bash
uwsgi  --ini    /opt/autoops/script/uwsgi.ini     # 启动uwsgi配置  也可以把这个命令写到开机的文件里面
uwsgi  --stop   /opt/autoops/script/uwsgi.pid    # 关闭uwsgi
uwsgi  --reload  /opt/autoops/script/uwsgi.pid   #重新加载
```
 
* nginx 配置文件修改如下。 此方法也要启动 uwsgi。

```bash
root         /opt/autoops;
   
   
    location / {
        include uwsgi_params;
        uwsgi_connect_timeout 30;
        uwsgi_pass unix:/opt/autoops/script/uwsgi.sock;
        
    }
    
    location /static/   {
            alias  /opt/autoops/static/;
            index  index.html index.htm;
    }     
```


###   截图
![DEMO](static/demo/13.png)
![DEMO](static/demo/12.png)
![DEMO](static/demo/1.png)
![DEMO](static/demo/4.png)
![DEMO](static/demo/5.png)
![DEMO](static/demo/7.png)

---
### 贡献者

#### 1.0
- 何全
