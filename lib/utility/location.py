# -*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.parse import quote
import json


def getjwd_bd(address):
    """根据地址获得经纬度（百度）"""
    url = 'http://api.map.baidu.com/geocoding/v3/?address='
    output = 'json'
    ak = 'FAjgfSoSquGTrL5cedE50HxhTl7EUqN7'#需填入自己申请应用后生成的ak
    add = quote(address) #本文城市变量为中文，为防止乱码，先用quote进行编码
    url2 = url+add+'&output='+output+"&ak="+ak
    req = urlopen(url2)
    res = req.read().decode()
    temp = json.loads(res)
    lng = float(temp['result']['location']['lng'])  # 经度 Longitude  简写Lng
    lat = float(temp['result']['location']['lat'])  # 纬度 Latitude   简写Lat
    return lng, lat


if __name__ == '__main__':
    print(getjwd_bd('中远两湾城'))