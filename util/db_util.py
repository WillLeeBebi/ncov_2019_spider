# -*- coding: utf-8 -*-

#
# connect()方法用于连接数据库，返回一个数据库连接对象。如果要连接一个位于host.remote.com服务器上名为fourm的MySQL数据库，连接串可以这样写：
# db = MySQLdb.connect(host="remote.com",user="user",passwd="xxx",db="fourm" )
# connect()的参数列表如下：
# host，连接的数据库服务器主机名，默认为本地主机(localhost)。
# user，连接数据库的用户名，默认为当前用户。
# passwd，连接密码，没有默认值。
# db，连接的数据库名，没有默认值。
# conv，将文字映射到Python类型的字典。默认为MySQLdb.converters.conversions
# cursorclass，cursor()使用的种类，默认值为MySQLdb.cursors.Cursor。
# compress，启用协议压缩功能。
# named_pipe，在windows中，与一个命名管道相连接。
# init_command，一旦连接建立，就为数据库服务器指定一条语句来运行。
# read_default_file，使用指定的MySQL配置文件。
# read_default_group，读取的默认组。
# unix_socket，在unix中，连接使用的套接字，默认使用TCP。
# port，指定数据库服务器的连接端口，默认是3306。
# 连接对象的db.close()方法可关闭数据库连接，并释放相关资源。
# 连接对象的db.cursor([cursorClass])方法返回一个指针对象，用于访问和操作数据库中的数据。
# 连接对象的db.begin()方法用于开始一个事务，如果数据库的AUTOCOMMIT已经开启就关闭它，直到事务调用commit()和rollback()结束。
# 连接对象的db.commit()和db.rollback()方法分别表示事务提交和回退。
# 指针对象的cursor.close()方法关闭指针并释放相关资源。
# 指针对象的cursor.execute(query[,parameters])方法执行数据库查询。
# 指针对象的cursor.fetchall()可取出指针结果集中的所有行，返回的结果集一个元组(tuples)。
# 指针对象的cursor.fetchmany([size=cursor.arraysize])从查询结果集中取出多行，我们可利用可选的参数指定取出的行数。
# 指针对象的cursor.fetchone()从查询结果集中返回下一行。
# 指针对象的cursor.arraysize属性指定由cursor.fetchmany()方法返回行的数目，影响fetchall()的性能，默认值为1。
# 指针对象的cursor.rowcount属性指出上次查询或更新所发生行数。-1表示还没开始查询或没有查询到数据。

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBUtil(object):
    def __init__(self):
        self.db_engine = None

    def create_session_factory(self,
                               con_str='mysql+pymysql://zimt8:Debug.zimt8@www.zimt8.com:33061/zimt8?charset=utf8mb4?connect_timeout=30'):
        self.db_engine = create_engine(
            con_str,
            pool_pre_ping=True,
            echo=False)

        self.session_factory = sessionmaker(bind=self.db_engine)
        return self.session_factory

    def get_new_session(self):
        self.sesison = self.session_factory()
        return self.sesison


class DBSession():
    def __init__(self, session):
        self.session = session

    def exec_sql(self, sql,kwargs=None):
        # print(sql)
        self.session.execute(sql,kwargs)

    def commit(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def sql2list(self, sql,kwargs=None):
        rs = self.session.execute(sql,kwargs)
        list_ = []
        desc = rs.cursor.description
        columns = [col[0] for col in desc]
        for row in rs:
            list_.append(dict(zip(columns, row)))
        return list_

#
# dbu = DBUtil()
# session_factory = dbu.create_session_factory()
# dbs = DBSession(session_factory())

# dbu.create_connect()
# dbu.get_session()
# rs=dbu.sql2list('select * from pdd_goods limit 10')
# print(rs)
# rs=dbu.sql2list('select * from image_bed limit 10')
# print(rs)
