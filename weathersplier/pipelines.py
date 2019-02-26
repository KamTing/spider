# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import cx_Oracle

# warehouse/passwd111@192.168.0.163/orcl

# conn = cx_Oracle.connect('warehouse/passwd111@192.168.0.162/orcl')  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
# curs = conn.cursor()
# # sql_list = list()


class WeathersplierPipeline(object):

    # def __init__(self):


    def open_spider(self, spider):
        self.conn = cx_Oracle.connect('warehouse/passwd111@192.168.0.162/orcl')  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
        self.curs = self.conn.cursor()
        self.dataset = []

    def process_item(self, item, spider):

        if spider.name == 'weather_spider':
            self.dataset.append((item['data'], item['no2'], item['pm2_5'], item['so2'], item['o3'], item['pm10'],
                                 item['aqi'], item['co']))
        elif spider.name == 'temperature_spider':
            print(item)

        return None

    def close_spider(self, spider):

        if spider.name == 'weather_spider':
            sql = "insert into warehouse.kam_test(data, no2, pm2_5, so2, o3, pm10, aqi, co) values (:1, :2, :3, :4, :5, :6, :7, :8)"
            self.curs.executemany(sql, self.dataset)
            self.conn.commit()
            print("数据入库成功")
        elif spider.name == 'temperature_spider':
            print('temperature_spider spider closed')



