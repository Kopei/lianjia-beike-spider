# -*- coding:utf-8 -*-
import os
import time
from urllib.request import urlopen
from urllib.parse import quote
import json

import threadpool
import pandas as pd


POOL_SIZE = 512


def getjwd_bd(address):
    """根据地址获得经纬度（百度）"""
    url = 'http://api.map.baidu.com/geocoding/v3/?address='
    output = 'json'
    ak = 'FAjgfSoSquGTrL5cedE50HxhTl7EUqN7'  # 需填入自己申请应用后生成的ak
    add = quote(address)  # 本文城市变量为中文，为防止乱码，先用quote进行编码
    url2 = url + add + '&output=' + output + "&ak=" + ak
    req = urlopen(url2)
    res = req.read().decode()
    temp = json.loads(res)
    if temp.get('result'):
        lng = float(temp['result']['location']['lng'])  # 经度 Longitude  简写Lng
        lat = float(temp['result']['location']['lat'])  # 纬度 Latitude   简写Lat
    else:
        lng = 0
        lat = 0
    return lng, lat


if __name__ == '__main__':
    addressDf = pd.read_csv(
        '/Users/ncpbestgmail.com/github/lianjia-beike-spider/data/ke/xiaoqu/sh/20200307/baoshan_dachangzhen.csv',
        header=None, names=['date', 'district', 'area', 'xiaoqu', 'price', 'sale', 'ninetydaysale', 'buildyear',
                            'currentonrent'])

    addresses = addressDf['xiaoqu']
    t1 = time.time()
    pool = threadpool.ThreadPool(POOL_SIZE)
    my_requests = threadpool.makeRequests(getjwd_bd, addresses)
    [pool.putRequest(req) for req in my_requests]
    pool.wait()
    pool.dismissWorkers(POOL_SIZE, do_join=True)  # 完成后退出
    t2 = time.time()
    print(t2-t1)
    for i in addresses:
        getjwd_bd(i)
    print(time.time()-t2)