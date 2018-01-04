#!/bin/bash
cd /usr/local/src
wget http://mirrors.sohu.com/python/3.6.4/Python-3.6.4.tgz

yum -y install zlib*  python-devel mysql-devel zlib-devel openssl-devel


tar xf Python-3.6.4.tgz
cd Python-3.6.4/
./configure   --enable-shared --enable-loadable-sqlite-extensions --with-zlib
./configure --enable-optimizations
make
make install


rm -rf /usr/bin/python

ln -s /usr/local/bin/python3.6 /usr/bin/python


vim /usr/bin/yum
 改为
#!/usr/bin/python2.7

vim /usr/libexec/urlgrabber-ext-down
改为
#!/usr/bin/python2.7

vim /etc/ld.so.conf
/usr/local/lib
include ld.so.conf.d/*.conf


/sbin/ldconfig

mkdir .pip

vim  /root/.pip/pip.conf

[global]
index-url = http://pypi.douban.com/simple
trusted-host = pypi.douban.com




python -V

