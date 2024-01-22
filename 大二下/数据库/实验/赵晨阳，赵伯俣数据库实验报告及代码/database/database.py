import pymysql

connect = pymysql.connect(host='localhost', db='student', user='zby', passwd='z', charset='utf8')
# 创建数据库访问的游标
cursor = connect.cursor()


class redgister_db(object):
    # 插入数据的函数
    def exert(sql):
        # 执行sql语句
        cursor.execute(sql)
        connect.commit()

    # 删除数据库
    def select(sql):
        cursor.execute(sql)
        # return cursor.fetchone()
        return cursor.fetchall()

    def closeDB(self):
        connect.close()

    # def select_all(sql):
    #   cursor.execute(sql)
    #   return cursor.fetchall()
