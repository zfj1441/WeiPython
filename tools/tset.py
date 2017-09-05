# -*- coding:utf-8 -*-
import re, os
import requests, time
import sqlite3
from bs4 import BeautifulSoup
from zxing import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def Z1GetSS():
    import base64
    local_filename = "../media/download/tmp.png"
    # 通过zxing解析二维码
    zx = BarCodeReader("zxing")
    barcode = zx.decode(local_filename)
    tmp = barcode.data.split("ss://")
    if len(tmp) >= 2:
        tmp = base64.b64decode(tmp[1])
        tmp = str(tmp).replace("\r\n", "")
        tmp = str(tmp).replace("\n", "")
        # tmp = aes-256-cfb:48644506@139.162.67.43:443
    print('二维信息[%s]' % tmp)


Z1GetSS()
