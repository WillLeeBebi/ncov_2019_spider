# -*- coding: utf-8 -*-
import hashlib
import json

from util.db_util import DBUtil, DBSession
from util.http_util import HttpClass
from time import sleep

from loguru import logger
from pymongo import MongoClient


class NcovSpider(object):
    def __init__(self):
        self.url_area = 'http://lab.isaaclin.cn/nCoV/api/area?latest=0'
        self.url_overall = 'http://lab.isaaclin.cn/nCoV/api/overall?latest=0'
        self.ohttp = HttpClass()
        self.host = '127.0.0.1'
        self.port = 27017

    def get_md5_value(self, str):
        return hashlib.md5(str.encode("utf8")).hexdigest()

    def import_history(self):
        # 导入历史数据 到mongo
        with open('data/overall.json', 'r', encoding='utf-8') as f:
            overall_json = f.read()
        overall_json = json.loads(overall_json)

        with open('data/area.json', 'r', encoding='utf-8') as f:
            area_json = f.read()
        area_json = json.loads(area_json)

        # 创建mongodb客户端
        self.client = MongoClient(self.host, self.port)
        # 创建数据库
        self.db = self.client.ncov
        # 创建集合
        self.collection = self.db.DXYArea
        self.collection.insert_many(area_json)

        # 创建集合
        self.collection = self.db.overall
        self.collection.insert_many(overall_json)
        print('写入成功')

    def mongo_to_mysql(self):
        # 将数据从mongo到mysql
        dbu = DBUtil()
        dbu.create_session_factory(
            con_str='mysql+pymysql://root:root@127.0.0.1:3306/ncov?charset=utf8mb4?connect_timeout=30')
        dbs = DBSession(dbu.get_new_session())

        n = 0
        self.client = MongoClient("mongodb://{}:{}/".format(self.host, self.port))
        self.database = self.client["ncov"]

        while 1:
            self.collection = self.database["DXYArea"]
            query = {}
            cursor = self.collection.find(query)
            sql = 'insert into dxyarea (_id,comment,confirmedCount,country,createTime,curedCount,deadCount,modifyTime,operator,provinceName,provinceShortName,suspectedCount,updateTime) values(:_id,:comment,:confirmedCount,:country,:createTime,:curedCount,:deadCount,:modifyTime,:operator,:provinceName,:provinceShortName,:suspectedCount,:updateTime)'
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                doc['updateTime'] = str(doc['updateTime'])
                try:
                    doc['modifyTime'] = str(doc['modifyTime'])
                except:
                    doc['modifyTime'] = None

                try:
                    doc['createTime'] = str(doc['createTime'])
                except:
                    doc['createTime'] = None
                try:
                    doc['operator'] = str(doc['operator'])
                except:
                    doc['operator'] = None

                    try:
                        if doc['cities']!='':
                            if isinstance(doc['cities'],list) is False:
                                doc['cities'] = json.loads(doc['cities'])

                            for r in doc['cities']:
                                sql2 = 'insert into dxyarea_city (dxyarea_id,cityName,deadCount,curedCount,suspectedCount,confirmedCount) values(:dxyarea_id,:cityName,:deadCount,:curedCount,:suspectedCount,:confirmedCount)'
                                r['dxyarea_id']=doc['_id']
                                try:
                                    dbs.exec_sql(sql2, r)

                                except Exception as e:
                                    emsg = (repr(e))
                                    if 'Duplicate entry' in emsg:
                                        pass
                                    else:
                                        logger.exception('遇到一个问题')
                            dbs.commit()
                        # else:
                        #     print(doc['cities'])
                    except:
                        logger.exception('')
                        # print(doc['cities'])
                        pass
                try:
                    dbs.exec_sql(sql, doc)

                except Exception as e:
                    emsg = (repr(e))
                    if 'Duplicate entry' in emsg:
                        pass
                    else:
                        logger.exception('遇到一个问题')
            dbs.commit()

            self.collection = self.database["DXYOverall"]
            query = {}
            cursor = self.collection.find(query)
            sql = 'insert into dxyoverall (_id,abroadRemark,confirmedCount,countRemark,curedCount,dailyPic,deadCount,generalRemark,infectSource,passWay,remark1,remark2,remark3,remark4,remark5,summary,suspectedCount,updateTime,virus) values(:_id,:abroadRemark,:confirmedCount,:countRemark,:curedCount,:dailyPic,:deadCount,:generalRemark,:infectSource,:passWay,:remark1,:remark2,:remark3,:remark4,:remark5,:summary,:suspectedCount,:updateTime,:virus)'
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                doc['updateTime'] = str(doc['updateTime'])
                try:
                    doc['abroadRemark'] = str(doc['abroadRemark'])
                except:
                    doc['abroadRemark'] = None
                try:
                    doc['generalRemark'] = str(doc['generalRemark'])
                except:
                    doc['generalRemark'] = None
                try:
                    dbs.exec_sql(sql, doc)

                except Exception as e:
                    emsg = (repr(e))
                    if 'Duplicate entry' in emsg:
                        pass
                    else:
                        logger.exception('遇到一个问题')
            dbs.commit()

            logger.debug('转换数据成功')
            sleep(30)


ns = NcovSpider()
# ns.import_history()
ns.mongo_to_mysql()
