#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# read data from csv, write to database
# database includes: mysql/mongodb/excel/json/csv

import os
import pymysql
from lib.utility.path import DATA_PATH
from lib.zone.city import *
from lib.utility.date import *
from lib.utility.version import PYTHON_3
from lib.spider.base_spider import SPIDER_NAME

pymysql.install_as_MySQLdb()


def create_prompt_text():
    city_info = list()
    num = 0
    for en_name, ch_name in cities.items():
        num += 1
        city_info.append(en_name)
        city_info.append(": ")
        city_info.append(ch_name)
        if num % 4 == 0:
            city_info.append("\n")
        else:
            city_info.append(", ")
    return 'Which city data do you want to save ?\n' + ''.join(city_info)


if __name__ == '__main__':
    # 设置目标数据库
    ##################################
    # mysql/mongodb/excel/json/csv
    # database = "mysql"
    # database = "mongodb"
    # database = "excel"
    # database = "json"
    database = "mysql"
    ##################################
    db = None
    collection = None
    workbook = None
    csv_file = None
    datas = list()

    if database == "mysql":
        import records
        db = records.Database('mysql://root:prisma@localhost:9336/lianjia?charset=utf8', encoding='utf-8')
    elif database == "mongodb":
        from pymongo import MongoClient
        conn = MongoClient('localhost', 27017)
        db = conn.lianjia  # 连接lianjia数据库，没有则自动创建
        collection = db.xiaoqu  # 使用xiaoqu集合，没有则自动创建
    elif database == "excel":
        import xlsxwriter
        workbook = xlsxwriter.Workbook('xiaoqu.xlsx')
        worksheet = workbook.add_worksheet()
    elif database == "json":
        import json
    elif database == "csv":
        csv_file = open("xiaoqu.csv", "w")
        line = "{0};{1};{2};{3};{4};{5};{6}\n".format('city_ch', 'date', 'district', 'area', 'xiaoqu', 'price', 'sale')
        csv_file.write(line)

    city = get_city()
    # 准备日期信息，爬到的数据存放到日期相关文件夹下
    date = get_date_string()
    # 获得 csv 文件路径
    # date = "20180331"   # 指定采集数据的日期
    # city = "sh"         # 指定采集数据的城市
    city_ch = get_chinese_city(city)
    csv_dir = "{0}/{1}/xiaoqu/{2}/{3}".format(DATA_PATH, SPIDER_NAME, city, date)

    files = list()
    if not os.path.exists(csv_dir):
        print("{0} does not exist.".format(csv_dir))
        print("Please run 'python xiaoqu.py' firstly.")
        print("Bye.")
        exit(0)
    else:
        print('OK, start to process ' + get_chinese_city(city))
    for csv in os.listdir(csv_dir):
        data_csv = csv_dir + "/" + csv
        # print(data_csv)
        files.append(data_csv)

    # 清理数据
    count = 0
    row = 0
    col = 0
    for csv in files:
        print('process...', csv)
        with open(csv, 'r') as f:
            for line in f:
                count += 1
                text = line.strip()
                try:
                    # 如果小区名里面没有逗号，那么总共是6项
                    fields = text.split(',')
                    date = fields[0]
                    district = fields[1]
                    area = fields[2]
                    xiaoqu = fields[3]
                    price = fields[4]
                    sale = fields[5]
                    ninetydaysales = fields[6]
                    buildyear = fields[7]
                    currentonrent = fields[8]
                    lng = fields[9]
                    lat = fields[10]
                    sale = sale.replace(r'套在售二手房', '')
                    price = price.replace(r'暂无', '0')
                    price = price.replace(r'元/m2', '')
                    ninetydaysales = ninetydaysales.replace(r'暂无', '0')
                    price = int(price)
                    sale = int(sale)
                except Exception as e:
                    print(line)
                    raise e

                # print("{0} {1} {2} {3} {4} {5}".format(date, district, area, xiaoqu, price, sale))
                # 写入mysql数据库
                if database == "mysql":
                    db.query('INSERT INTO xiaoqu (city, date, district, area, xiaoqu, price, sale, ninetydaysales, buildyear, currentonrent, lng, lat) '
                             'VALUES(:city, :date, :district, :area, :xiaoqu, :price, :sale, :ninetydaysales, :buildyear, :currentonrent, :lng, :lat)',
                             city=city_ch, date=date, district=district, area=area, xiaoqu=xiaoqu, price=price,
                             sale=sale, ninetydaysales=ninetydaysales, buildyear=buildyear, currentonrent=currentonrent,
                             lng=lng, lat=lat)
                # 写入mongodb数据库
                elif database == "mongodb":
                    data = dict(city=city_ch, date=date, district=district, area=area, xiaoqu=xiaoqu, price=price,
                                sale=sale)
                    collection.insert(data)

                elif database == "json":
                    data = dict(city=city_ch, date=date, district=district, area=area, xiaoqu=xiaoqu, price=price,
                                sale=sale)
                    datas.append(data)
                elif database == "csv":
                    line = "{0};{1};{2};{3};{4};{5};{6}\n".format(city_ch, date, district, area, xiaoqu, price, sale)
                    csv_file.write(line)

    # 写入，并且关闭句柄
    if database == "excel":
        workbook.close()
    elif database == "json":
        json.dump(datas, open('xiaoqu.json', 'w'), ensure_ascii=False, indent=2)
    elif database == "csv":
        csv_file.close()

    print("Total write {0} items to database.".format(count))
