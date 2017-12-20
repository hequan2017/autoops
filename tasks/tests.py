#/usr/bin/python
#_*_ coding:utf-8  _*_

import pymysql.cursors




sql='/*--user=root;--password=123456;--host=192.168.10.81;--execute=1;--port=3306;*/\
inception_magic_start;\
use hequan;\
CREATE TABLE adaptive_office(id int);\
inception_magic_commit;'



try:
    conn=pymysql.connect(host='127.0.0.1',user='',passwd='',db='',port=6669)
    cursor=conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    column_name_max_size=max(len(i[0]) for i in cursor.description)
    row_num=0
    for result in results:
        row_num=row_num+1
        print('*'.ljust(27,'*'),row_num,'.row', '*'.ljust(27,'*'))
        row = map(lambda x, y: (x,y), (i[0] for i in cursor.description), result)
        for each_column in row:
            if each_column[0] != 'errormessage':
                print(each_column[0].rjust(column_name_max_size),":",each_column[1])
            else:   print(each_column[0].rjust(column_name_max_size),':',each_column[1].replace('\n','\n'.ljust(column_name_max_size+4)))
    cursor.close()
    conn.close()
except pymysql.Error as e:
     print("Mysql Error %d: %s" % (e.args[0], e.args[1]))