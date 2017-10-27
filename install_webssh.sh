#!/bin/bash

cd /opt
yum  install git -y
wget  https://storage.googleapis.com/golang/go1.8.1.linux-amd64.tar.gz
tar zxvf go1.8.1.linux-amd64.tar.gz -C /usr/local
echo 'export PATH="/usr/local/go/bin:$PATH"' >> /etc/profile
source    /etc/profile

cd  /opt && git clone --recurse-submodules https://github.com/shibingli/webconsole.git && cd webconsole && git submodule update --init --recursive

# 如果报错  可以把上面的 --recurse-submodules   删除掉
cd /opt/webconsole/src/apibox.club/apibox
GOPATH=/opt/webconsole go install


#centos 6 的系统会报错,需要执行以下下面的命令。 7的如果也报错的话，也可以试一下。
#cd /opt/webconsole/src/golang.org/x/
#rm -rf crypto/
#git clone https://github.com/golang/crypto.git
#cd /opt/webconsole/src/apibox.club/apibox
#GOPATH=/opt/webconsole go install

##以下为需要修改的内容。

#vim /opt/webconsole/conf/conf.json


#  "addr": ":9000",  ##修改端口为9000  可以自定义。 我设置的为9000，如果修改成别的端口，需要修改网页。 templates/asset/asset.html
# "enable_jsonp": true,    开启jsonp，启用跨域访问
# "cors_white_list": "42.62.6.54,42.62.6.54:9000,"  这里输入的地址为需要跨域访问的，添加webssh服务器端的地址。



##启动停止
#/opt/webconsole/bin/apibox   start   |   stop

##修改autoops       templates/asset/asset.html
# 第239和255 行 的地址 和端口，修改成自己webssh服务器端地址。


##具体可以看   https://github.com/shibingli/webconsole