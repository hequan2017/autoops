#!/bin/bash
##http://mysql-inception.github.io/inception-document/install/
##https://github.com/mysql-inception/inception




#Cetos7.4系统  环境设置
yum install cmake   ncurses-devel gcc gcc-c++  openssl-devel
yum  remove bison -y


cd /usr/local/src/

wget http://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz
tar -zxvf m4-1.4.18.tar.gz
cd m4-1.4.18


./configure && make && make install



wget http://ftp.gnu.org/gnu/bison/bison-2.5.tar.gz
tar -zxvf bison-2.5.tar.gz
cd bison-2.5/
./configure


vim ./lib/stdio.h

##删除  这一行  _GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");

./configure

make && make install

bison  -V



cd /usr/local/
wget https://github.com/mysql-inception/inception/archive/master.zip

unzip master.zip
mv inception-master/  inception
mv master.zip inception.zip
mv inception.zip   /usr/local/src/

sh inception_build.sh builddir  linux


#由于python3使用的pymysql模块里并未兼容inception返回的server信息，因此需要编辑  /usr/local/python3/lib/python3.5/site-packages/pymysql/connections.py
#在if int(self.server_version.split('.', 1)[0]) >= 5: 这一行之前加上以下这一句并保存，记得别用tab键用4个空格缩进：
#self.server_version = '5.6.24-72.2-log'

    def _request_authentication(self):
        # https://dev.mysql.com/doc/internals/en/connection-phase-packets.html#packet-Protocol::HandshakeResponse
        self.server_version = "5.7.20-log"
        if int(self.server_version.split('.', 1)[0]) >= 5:
            self.client_flag |= CLIENT.MULTI_RESULTS


vim  /usr/local/python3/lib/python3.5/site-packages/pymysql/cursors.py

        if not self._defer_warnings:
            #self._show_warnings()
            pass




nohup    /usr/local/inception/builddir/mysql/bin/Inception  --defaults-file=/opt/autoops/script/inc.cnf   >/dev/null  2>&1   &


#测试
mysql -uroot -h127.0.0.1 -P6669

inception get variables;












