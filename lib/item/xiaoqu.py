#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 小区信息的数据结构


class XiaoQu(object):
    def __init__(self, *args):
        for index, i in enumerate(args):
            setattr(self, str(index), str(i))

    def text(self):
        return ','.join(self.__dict__.values())
