## AutoOps

AutoOps是一款基于1.11版本django开发的，主要面向linux运维工程师使用,管理资产信息，批量执行命令、脚本，获取流量图，web ssh管理，技术文档等功能。



###  Demo

  -  地址:`http://42.62.55.58:8003/`        账号`admin`      密码`1qaz.2wsx`
  -  交流群号：`620176501`   欢迎交流！   <a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=bbe5716e8bd2075cb27029bd5dd97e22fc4d83c0f61291f47ed3ed6a4195b024"><img border="0" src="https://github.com/hequan2017/cmdb/blob/master/static/img/group.png"  alt="autoops开发讨论群" title="autoops开发讨论群"></a>
  -  后台地址 `http://42.62.55.58:8003/admin`     账号`admin`   密码`1qaz.2wsx`
  -  资产api地址 `http://42.62.55.58:8003/asset/api/asset.html`
  -  博客:`http://hequan.blog.51cto.com/`
  -  github:`https://github.com/hequan2017/autoops/`
  -  码云:`https://gitee.com/hequan2020/autoops`

  
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/autuops.png)  


### 更新记录
  -  1.3.4  数据库切换为mysql数据库。
  -  1.3.3  增加删除历史获取的流量、CPU、内存等数据。优化性能页面打开速度。
  -  1.3.2  新增 资产查询、管理网IP、网卡MAC地址、内存显示优化等。 硬盘、内存显示优化，修复核心数显示不正确。
  -  1.3    新增 技术文档 板块。
  -  1.2    权限管理完善。 增加附件上传下载功能。
  -  1.1.5  新增 权限管理。 根据后台用户组，区分不同权限。如：在后台先建一个 测试机 组，把普通用户加入到此组。在前端添加资产时，在产品线中会出现测试机 。 测试机组下的用户 只管管理测试机产品线的资产。             
  -  1.1    新增 平台登录记录、web登录记录、密码修改等功能。


###  功能
  - asset资产
    - api
  - names用户（预留模块）
  - tasks任务
  - webssh登陆
  - 技术文档 (真正运维人员的管理平台，自带技术文档，有问题不用再去别的地方找)

### 环境
   * Python 3.6.2 
   * Django 1.11.6
   * Python  2.7  (用来启动 supervisor)
   
### 安装 

   * 开发环境部署：
   
   
   1. 下载，安装基本环境,安装目录为/opt下，如是其他目录，请修改supervisor.conf中的相应设置即可。
 ```
 cd /opt
 git  clone  git@github.com:hequan2017/autoops.git

cd autoops/
yum install sshpass -y

pip3 install -r requirements.txt     

pip3 install https://github.com/darklow/django-suit/tarball/v2


```
    添加的资产 里面 请执行   yum install  ipmitool     dmidecode   -y 以获取信息
  
    2. 安装其他组件
 
 * 执行 `install_redis.sh` 
 * 执行 `install_webssh.sh` ,需要修改的内容见脚本内，如果不需要webssh，可暂时不用安装。
 * 安装 `supervisor  `
 
```
 pip2   install    supervisor   
 
 echo_supervisord_conf > /etc/supervisord.conf 
 
 mkdir /etc/supervisord.d/
``` 
  
  
``` 
 vim /etc/supervisord.conf
 
[include]
files = /etc/supervisord.d/*.conf

[inet_http_server] 
port=0.0.0.0:9001 
username=user
password=123
``` 
 * 配置文件  `cp   /opt/autoops/supervisor.conf  /etc/supervisord.d/`
 

### 启动

  * 启动supervisor进程管理  `/usr/bin/python2.7   /usr/bin/supervisord -c /etc/supervisord.conf`
  * 关于数据库 请修改 `autops/settings`文件, 如果没有mysql，请选择上面那种，注释下面的。如果有，则可以启用mysql，设置相关连接地址。
  
    关于mysql安装方法，可参考我的博客 `http://hequan.blog.51cto.com/5701886/1982428`
``` 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

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
  * 初始化数据库
```
python manage.py makemigrations
python manage.py  migrate
python manage.py  createsuperuser      创建管理员
``` 
  
  
  * 启动主服务     `python manage.py  runserver  0.0.0.0:80`  或者   命令启动： `uwsgi --http :80 --chdir /opt/autoops/ -w autoops.wsgi --static-map=/static=static   `
  * 打开   0.0.0.0:9001  账号user  密码123    进入进程管理界面，管理redis,webssh,celery等启动关闭。

  *  如果想在生产环境部署、启动, 可以参考 `http://hequan.blog.51cto.com/5701886/1982769`
  

### 截图
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
