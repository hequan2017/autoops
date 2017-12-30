## AutoOps

AutoOps 是一款基于 2.0 版本django开发的，主要面向linux运维工程师使用,管理linux资产信息，Mysql数据库，批量执行命令、脚本,获取流量图，web ssh管理，技术文档等功能。

欢迎大家测试使用，有问题可反馈。


###  Demo

  -  地址:  `http://42.62.55.58:8003/`        账号`admin`      密码`1qaz.2wsx`
  -  交流群号： `620176501`   欢迎交流！   <a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=bbe5716e8bd2075cb27029bd5dd97e22fc4d83c0f61291f47ed3ed6a4195b024"><img border="0" src="https://github.com/hequan2017/cmdb/blob/master/static/img/group.png"  alt="autoops开发讨论群" title="autoops开发讨论群"></a>
  -  后台地址 `http://42.62.55.58:8003/admin`     账号`admin`   密码`1qaz.2wsx`
  -  博客:    `http://hequan.blog.51cto.com/`
  -  github:  `https://github.com/hequan2017/autoops/`
  -  码云:    `https://gitee.com/hequan2020/autoops`

###  架构图

 
![DEMO](https://github.com/hequan2017/autoops/blob/master/static/demo/autoops.png)


### 更新记录  

  -  1.6.7   权限梳理，若干代码优化。
      -  根据后台用户组进行区分。admin有最高权限。
      -  例如：新建  运维组、开发组 ， 新建 运维组 里面的 hequan 账号
      -  那么  hequan 只能看见 运维组下面的服务器、数据库，执行工具也只能选择 运维组的。 hequan 无法添加服务器、数据库。
     
  -  1.6    Mysql数据库操作: 自动审核 + 执行 （目前只适用于Mysql）  
      -  自动审核： 利用软件去审核命令是否正确。
      -  命令执行： 去数据库执行命令，会忽略报警和警告，使用前建议 先 自动审核一下。  
      -  回滚功能
  
  -  1.4    更新django 为2.0
  -  1.3    新增 技术文档 板块。
  -  1.2    权限管理完善。 增加附件上传下载功能。
  -  1.1.5  新增 权限管理。 根据后台用户组，区分不同权限。如：在后台先建一个 测试机 组，把普通用户加入到此组。在前端添加资产时，在产品线中会出现测试机 。 测试机组下的用户 只管管理测试机产品线的资产。             
  -  1.1    新增 平台登录记录、web登录记录、密码修改等功能。


###  功能
  - asset资产
    - api     `http://42.62.55.58:8003/asset/api/asset.html`
    - 自动获取服务器信息
    - 全部导出
    - CPU 内存 流量图
  - names 用户（预留模块）
      -  加密解密   password_crypt.py 
  - tasks任务 
     - 命令行
     - 工具  
        - shell 
        - python
        - yml
        
  - webssh  登陆 （用复制粘贴的时候，会显示二份，但实际只有一个，不影响使用，请忽略。）
  
  - library 技术文档 (真正运维人员的管理平台，自带技术文档，有问题不用再去别的地方找)
    - DjangoUeditor 富文本编辑器
    
  - 数据库自动审核-- 命令执行   回滚
    - Inception 
  - 后台管理
    - admin     
   

### 环境

   * Python 3.6.4
   * Django 2.0
   * Python 2.7  (用来启动 supervisor)
 
 
   
### 安装 

   * 开发环境部署：
   
   
   1. 下载，安装基本环境,安装目录为/opt下，如是其他目录，请修改supervisor.conf中的相应设置即可。
 
```bash
cd /opt
yum install git   sshpass -y 
git  clone  git@github.com:hequan2017/autoops.git
    
cd autoops/
pip3 install -r requirements.txt     
    
pip3 install git+git://github.com/sshwsfc/xadmin.git@django2
```
    
  
   添加的资产 里面 请执行  ` yum install  ipmitool     dmidecode   -y  `以获取更多信息
   
  
    2. 安装其他组件
    
 
 * 执行 `srcipt/install_redis.sh`   
 * 安装 `script/install_webssh.sh` ,  需要修改的内容见脚本内，如果不需要webssh，可暂时不用安装。
 * 安装 `script/install_inception.sh` ,  需要修改的内容见脚本内，如果不需要 数据库自动审核，可暂时不用安装。
 
 * 安装   `supervisor  `
 
```bash
pip2   install    supervisor   

echo_supervisord_conf > /etc/supervisord.conf 
mkdir /etc/supervisord.d/
     

vim /etc/supervisord.conf
     
[include]
files = /etc/supervisord.d/*.conf
    
[inet_http_server] 
port=0.0.0.0:9001 
username=user
password=123

```  
    
 * 配置文件    ` cp   /opt/autoops/script/supervisor.conf    /etc/supervisord.d/   `
 

###  环境设置

  * 关于数据库 请修改 `autops/settings`文件, 如果没有mysql，请选择上面那种，注释下面的。如果有，则可以启用mysql，设置相关连接地址。
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
DEBUG = True  ## 实际生产环境实用，请关闭  False

BROKER_URL = 'redis://127.0.0.1:6379/0'  ##Redis地址

Webssh_ip = "42.62.6.54"    ##WebSSH 软件的 访问IP
Webssh_port='9000'


Inception_ip = '127.0.0.1'      ## 此为 Inception 软件地址 需要设置
Inception_port = '6669'         ## 此为 Inception 软件端口号

inception_remote_system_password='123456'             ## 设置回滚备份服务器相关参数，并同步修改一下 script/inc.cnf 里面的设置
inception_remote_system_user='root'
inception_remote_backup_port='3306'
inception_remote_backup_host='192.168.10.81'

```  
  
    
  * 初始化数据库（可删除文件夹的 db.sqlite3）
  
```bash
python manage.py makemigrations
python manage.py  migrate
python manage.py  createsuperuser             ##创建管理员
``` 
             
      
  * 启动supervisor进程管理  `/usr/bin/python2.7   /usr/bin/supervisord -c /etc/supervisord.conf`
    加到linux 开机启动里面  `chmod +x  /etc/rc.d/rc.local ` 把上面的命令放到这个文件里面  
  
  
  * 启动: 统一用supervisor 管理进程,  打开   0.0.0.0:9001  账号user  密码123    进入进程管理界面，管理uwsgi,redis,webssh,celery,Inception 等启动关闭。
此方法不涉及到nginx。

 
  * 登陆后台，设置定时获取主机图，设置数据中心、组。
  
  * 设置定时获取主机信息任务。 先创建执行的时间频率，再创建任务，创建后，观察队列任务是否执行成功，如不成功，重启所有celery任务。
 ![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/9.png)



###  开发设置

  * 如果想在windows 下的 pycharm打开，请注释  
  
  ```djangotemplate
asset/views.py
from  tasks.ansible_runner.runner import AdHocRunner


tasks/views.py   
from   tasks.ansible_runner.runner import AdHocRunner, PlayBookRunner
from   tasks.ansible_runner.callback import CommandResultCallback
```
    
    
    
   
###  生产环境   
   
  * 如果想在生产环境部署、启动, 用nginx去处理。 可以参考   `http://hequan.blog.51cto.com/5701886/1982769` , 请把`supervisor.conf` 中 关于uwsgi的部分删除掉, 
用以下方式控制UWSGI的启动 关闭.


```bash
uwsgi  --ini    /opt/autoops/script/uwsgi.ini   # 启动uwsgi配置  也可以把这个命令写到开机的文件里面
uwsgi  --stop   /opt/autoops/script/uwsgi.pid # 关闭uwsgi
uwsgi  --reload  /opt/autoops/script/uwsgi.pid  #重新加载
```
 
*  或者用nginx 
nginx 配置文件修改如下

```html
root         /opt/autoops;
   
   
    location / {
        include uwsgi_params;
        uwsgi_connect_timeout 30;
        uwsgi_pass unix:/opt/autoops/script/uwsgi.sock;
        
    }
    location /static/ {
            alias  /opt/autoops/static/;
            index  index.html index.htm;
    }
     
```




###   截图
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/1.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/2.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/3.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/4.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/5.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/6.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/7.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/8.png)


### 贡献者

#### 1.0
- 何全
