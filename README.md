## AutoOps

AutoOps是一款基础django开发的，面向运维工程师使用，可以管理资产，批量执行命令、脚本，web ssh管理。


###  Demo

  -  地址:`http://42.62.55.58:8003/`    账号`admin`   密码`1qaz.2wsx`
  -  交流群号：`620176501`  
  -  资产api地址 `http://42.62.55.58:8003/asset/api/asset.html`
  
 

###  功能
  - asset资产
    - api
  - names用户（预留模块）
  - tasks任务
  - webssh

### 环境
   * Python 3.6.2 
   * Django 1.11.4
   
### 安装 
   1. 下载，安装基本环境
 ```
 cd /opt
 
git  clone  git@github.com:hequan2017/autoops.git

cd autoops/

pip3 install -r requirements.txt     

pip3 install https://github.com/darklow/django-suit/tarball/v2
```
   2. 安装其他组件
 
 * 执行 `install_redis.sh` 
 * 执行 `install_webssh.sh` ,需要修改的内容见脚本内
 * 安装 `supervisor  `
 
  ```
 pip2 install    supervisor   
 
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
 * 配置文件  `cp /opt/autoops/supervisor.conf  /etc/supervisord.d/`
 

### 启动

  * 启动supervisor进程管理  `/usr/bin/python2.7 /usr/bin/supervisord -c /etc/supervisord.conf`
  * 启动主服务     `python manage.py  runserver  0.0.0.0:8001`    

### 截图
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/1.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/2.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/3.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/4.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/5.png)
![图片](https://github.com/hequan2017/autoops/blob/master/static/demo/6.png)


### 贡献者


#### 1.0
- 何全
