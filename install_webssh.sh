#!/bin/bash

cd /opt
wget  https://storage.googleapis.com/golang/go1.8.1.linux-amd64.tar.gz
tar zxvf go1.8.1.linux-amd64.tar.gz -C /usr/local
echo 'export PATH="/usr/local/go/bin:$PATH"' >> /etc/profile
source    /etc/profile
cd  /opt && git clone --recurse-submodules https://github.com/shibingli/webconsole.git && cd webconsole && git submodule update --init --recursive
cd /opt/webconsole/src/apibox.club/apibox
GOPATH=/opt/webconsole go install


##以下为需要修改的内容。

#vim /opt/webconsole/conf/conf.json


#  "addr": ":9000",  ##修改端口为9000  可以自定义。 我设置的为9000，如果修改成别的端口，需要修改网页。 templates/host/host.html
# "enable_jsonp": true,    开启jsonp，启用跨域访问
# "cors_white_list": "42.62.6.54,42.62.6.54:9000,"  这里输入的地址为需要跨域访问的，添加web主机的地址。



##启动停止
#/opt/webconsole/bin/apibox   start   |   stop

##修改templates/host/host.html
# 第751和767 行 的地址 和端口，修改成自己的。


##具体可以看 https://github.com/shibingli/webconsole