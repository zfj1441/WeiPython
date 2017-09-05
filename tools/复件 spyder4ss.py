# -*- coding:utf-8 -*-
import re, os
import requests, time
import sqlite3
from bs4 import BeautifulSoup
from zxing import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import logging
import logging.config

CONF_LOG = "logger.conf"
logging.config.fileConfig(CONF_LOG);  # 采用配置文件
logger = logging.getLogger('main')

urllist = [{'site': u'https://freessr.xyz/',
            'csspath': u'body > div.container > div.row > div.col-md-6.text-center',
            'remath': r'.*<h4>.*服务器地址:(.*)</h4>.*<h4>端口:(\d+)</h4>.*<h4>.*密码:(.*)</h4>.*<h4>.*加密方式:(.*)</h4>.*<h4>.*状态:<font .*>(.*)</font></h4>.*',
            'method': u'',
            },
           {'site': u'https://www.shadowsocksgo.com/page/testss.html',
            'csspath': u'body > div.tplmain > table.main_table > tr > td.righttd > div.pagect > div.pagecontent > div.testvpnitem',
            'remath': r'.*服务器IP：<span>(.*)</span><br/>	端口：(.*)<br/>	密码：(.*)<br/>	加密方式：<span>(.*)</span></div>(.*)',
            'method': u'',
            },
           {'site': u'http://freess.org/#portfolio-preview',
            'csspath': u'section#portfolio-preview > div.row > div.4u.12u(mobile) > a.image.fit',
            'remath': r'',
            'method': u'Z1GetSS',
            }, ]


def Z1GetSS(urlmsg):
    try:
        import base64
        retdata = {}
        # 通过bs4取二维码的url
        url = urlmsg['href']
        logger.debug("imgurl:%s" % url)
        imgurl = "http://freess.org/" + url

        # 下载图片
        if not os.path.exists("..\\media\\download"):
            os.mkdir("..\\media\\download")
        local_filename = "..\\media\\download\\tmp." + imgurl.split('.')[-1]
        r = requests.get(imgurl, stream=True)  # here we need to set stream = True parameter
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            f.close()
        local_filename = local_filename.replace('\\', '/')
        # 通过zxing解析二维码
        zx = BarCodeReader("zxing")
        barcode = zx.decode(local_filename)
        tmp = barcode.data.split("ss://")
        if len(tmp) >= 2:
            tmp = base64.b64decode(tmp[1])
            tmp = str(tmp).replace("\r\n", "")
            tmp = str(tmp).replace("\n", "")
            # tmp = aes-256-cfb:48644506@139.162.67.43:443
        logger.debug('二维信息[%s]' % tmp)
        tmp = tmp.split("@")
        ip = tmp[1].split(':')
        key = tmp[0].split(':')
        # 取ss信息
        retdata.setdefault('ip', ip[0])
        retdata.setdefault('post', ip[1])
        retdata.setdefault('password', key[1])
        retdata.setdefault('mode', key[0])
        retdata.setdefault('state', "")
        return 0, retdata
    except Exception, e:
        logger.error("异常:[%s]" % (e.message))
        return 1, retdata


def __remsg(rowdata, remath):
    '''
    从html数据中通过正则表达式取出ss信息
    :param htmldata:
    :param remath:
    :return:
    '''
    retdata = {}
    m = re.match(remath, str(rowdata))
    if m:
        retdata.setdefault('ip', m.group(1))
        retdata.setdefault('post', m.group(2))
        retdata.setdefault('password', m.group(3))
        retdata.setdefault('mode', m.group(4))
        retdata.setdefault('state', m.group(5))
        return 0, retdata
    else:
        logger.info('not match')
        return 1, retdata


def getHtml(url, csspath, remath, method):
    '''
    获取页面并解析
    :param url:
    :param csspath:
    :param remath:
    :param mtehod:自定义方法函数(优先)
    :return:
    '''
    retlist = []
    html_txt = requests.get(url, verify=False).text
    soup = BeautifulSoup(html_txt, 'lxml')
    tablelist = soup.select(csspath)
    for l in tablelist:
        retdata = {}
        if method != '':
            logger.info("本次采用自定义方法[%s]解析ss信息" % method)
            # modpath = "from %s import *" % ('printhello') 暂时不引用其它模块
            # exec modpath
            suc, retdata = eval(method)(l)
        else:
            logger.info("本次采用默认方法(正则表达式)解析ss信息")
            if re != '':
                l = str(l).replace("\r\n", "")
                l = str(l).replace("\n", "")
                suc, retdata = __remsg(l, remath)
            else:
                raise Exception("正则表达式为空")
        if suc == 0:
            retlist.append(retdata)
    return retlist


def getss():
    logger.info("start run getss()")
    begintime = time.time()
    # print getHtml(url.get('site'), url.get('csspath'), url.get('remath'))
    conn = sqlite3.connect("..\Untitled.sqlite3")
    cur = conn.cursor()
    for url in urllist:
        logger.info("开发扫描网站 [%s]", url.get('site'))
        try:
            webdata = getHtml(url.get('site'), url.get('csspath'), url.get('remath'), url.get('method'))
            cur.execute("DELETE FROM ssinfo where sitename='%s'" % url['site'])
            for row in webdata:
                try:
                    sql = "insert into ssinfo(sitename,serial,ip,port,password,mode,state) VALUES ('%s',null, '%s', '%s', '%s', '%s', '%s')" \
                          % (url['site'], row['ip'], row['post'], row['password'], row['mode'],
                             str(row['state']).encode('utf-8'))
                    cur.execute(sql)
                except Exception as e:
                    print(e)
        except Exception, e:
            logger.error("异常:[%s][%s]" % (url.get('site'), e.message))
        time.sleep(5)
    cur.close()
    conn.commit()

    endtime = time.time()
    usetime = endtime - begintime
    logger.info(u"执行脚本总用时 %s 秒" % usetime)
