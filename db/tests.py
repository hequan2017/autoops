#/usr/bin/python
#_*_ coding:utf-8  _*_

import pymysql.cursors

def  sql(user,password,host,port,sqls):
    sql = '/*--user={0};--password={1};--host={2};--execute=1;--port={3};*/\
    inception_magic_start;{4}inception_magic_commit;'.format(user,password,host,port,sqls)

    print(sql)

    try:
        ret = {"ip": host, "data": None}
        conn=pymysql.connect(host='192.168.10.83',user='',passwd='',db='',port=6669)
        cursor=conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        column_name_max_size=max(len(i[0]) for i in cursor.description)
        row_num=0

        data = []

        for result in results:
            row_num=row_num+1
            data.append(('*'.ljust(27,'*'),row_num,'.row', '*'.ljust(27,'*')))
            row = map(lambda x, y: (x,y), (i[0] for i in cursor.description), result)
            for each_column in row:
                if each_column[0] != 'errormessage':
                    data.append((each_column[0].rjust(column_name_max_size),":",each_column[1]))
                else:
                    data.append((each_column[0].rjust(column_name_max_size),':',each_column[1].replace('\n','\n'.ljust(column_name_max_size+4))))

        ret['data']  = data
        print(data)
        cursor.close()
        conn.close()
        return ret
    except pymysql.Error as e:
         data = "Mysql Error %d: %s" % (e.args[0], e.args[1])
         ret = {"ip": host, "data": data}
         return ret


if __name__=="__main__":
    a = sql(user='root',password=123456,host='192.168.10.81',port=3306,sqls='use hequan;CREATE TABLE adaptive_office(id int);')
    print(a)


