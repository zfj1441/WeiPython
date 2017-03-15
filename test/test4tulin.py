# -*- coding:utf-8 -*-
import json
import time
import urllib
import urllib2


class RobotService(object):
    """Auto reply robot service"""
    KEY = '1d1c405af0944ef0a597d8d9a823d4f7'
    url = 'http://www.tuling123.com/openapi/api'

    @staticmethod
    def auto_reply(req_info):
        query = {'key': RobotService.KEY, 'info': req_info.encode('utf-8')}
        headers = {'Content-type': 'text/html', 'charset': 'utf-8'}
        data = urllib.urlencode(query)
        req = urllib2.Request(RobotService.url, data)
        f = urllib2.urlopen(req).read()
        print json.loads(f)
        # return json.loads(f).get('text').replace('<br>', '\n')
        # return json.loads(f).get('text'

    def __anyRet(self, msg):
        if msg['code'] == '100000':
            '''文本类,以text返回'''
            pass
        elif msg['code'] == '200000':
            '''链接类，以link返回'''
            pass
        elif msg['code'] == '302000':
            '''新闻类，以news或Articles返回'''
            pass
        elif msg['code'] == '308000':
            '''菜谱类，以news或Articles返回'''
            pass
        elif msg['code'] == '313000':
            '''儿歌类'''
            pass
        elif msg['code'] == '314000':
            '''诗词类'''
            pass
        else:
            pass


if __name__ == '__main__':
    from lxml import etree

    # 创建根节点
    root = etree.Element(u'xml')
    tmproot = etree.SubElement(root, 'subkey')
    itemroot = etree.SubElement(tmproot, u'item')
    tmpkey_ele = etree.SubElement(itemroot, 'aa')
    tmpkey_ele.text = etree.CDATA(unicode('22'))
    print etree.tostring(root, pretty_print=True, xml_declaration=False, encoding=u'utf-8')
