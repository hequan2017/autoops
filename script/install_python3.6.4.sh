#!/bin/bash
cd /usr/local/src
wget http://mirrors.sohu.com/python/3.6.4/Python-3.6.4.tgz

yum -y install zlib*  python-devel mysql-devel zlib-devel openssl-devel  gcc


tar xf Python-3.6.4.tgz
cd Python-3.6.4/
./configure   --enable-shared --enable-loadable-sqlite-extensions --with-zlib
./configure --enable-optimizations
make
make install


rm -rf /usr/bin/python

ln -s /usr/local/bin/python3.6    /usr/bin/python


sed  -i    's/\#\!\/usr\/bin\/python/\#\!\/usr\/bin\/python2/'   /usr/bin/yum
sed  -i    's/\#\! \/usr\/bin\/python/\#\! \/usr\/bin\/python2/'   /usr/libexec/urlgrabber-ext-down


echo  "/usr/local/lib"  >> /etc/ld.so.conf


/sbin/ldconfig


mkdir -p  /root/.pip/

cat >  /root/.pip/pip.conf   <<EOF
[global]
trusted-host=mirrors.aliyun.com
index-url=http://mirrors.aliyun.com/pypi/simple/
EOF


python -V

