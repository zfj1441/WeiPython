# -*- coding:utf-8 -*-
"""
# Author: Pegasus Wang (pegasuswang@qq.com, http://ningning.today)
# Created Time : Fri Feb 20 21:38:57 2015

# File Name: wechatService.py
# Description:

# :copyright: (c) 2015 by Pegasus Wang.
# :license: MIT, see LICENSE for more details.
"""

import json
import time
import urllib
import urllib2

from wechatUtil import MessageUtil
from wechatReply import *
from dbTools import *

class RobotService(object):
    """Auto reply robot service"""
    KEY = 'd92d20bc1d8bb3cff585bf746603b2a9'
    url = 'http://www.tuling123.com/openapi/api'

    @staticmethod
    def auto_reply(req_info):
        query = {'key': RobotService.KEY, 'info': req_info.encode('utf-8')}
        headers = {'Content-type': 'text/html', 'charset': 'utf-8'}
        data = urllib.urlencode(query)
        req = urllib2.Request(RobotService.url, data)
        f = urllib2.urlopen(req).read()
        # return json.loads(f).get('text').replace('<br>', '\n')
        return json.loads(f)


class WechatService(object):
    """process request"""
    @staticmethod
    def processRequest(request):
        """process different message types.

        :param request: post request message
        :return: None
        """
        requestMap = MessageUtil.parseXml(request)
        fromUserName = requestMap.get(u'FromUserName')
        toUserName = requestMap.get(u'ToUserName')
        createTime = requestMap.get(u'CreateTime')
        msgType = requestMap.get(u'MsgType')
        msgId = requestMap.get(u'MsgId')

        textReply = TextReply()
        textReply.setToUserName(fromUserName)
        textReply.setFromUserName(toUserName)
        textReply.setCreateTime(time.time())
        textReply.setMsgType(MessageUtil.RESP_MESSAGE_TYPE_TEXT)

        if msgType == MessageUtil.REQ_MESSAGE_TYPE_TEXT:
            content = requestMap.get('Content').decode('utf-8')    # note: decode first
            # ret = RobotService.auto_reply(content)
            # mycmd
            if content.split(':')[0] in dbTools.MYCMD_TYPE and len(content.split(':')) >= 2:
                ret = {}
                # only return text type msg
                ret.setdefault('code', '100000')
                msg = dbTools.getMsgByMobile(str(content.split(':')[1]))
                ret.setdefault('text', msg)
            else:
                ret = RobotService.auto_reply(content)
            # end
            if ret.get('code') == 100000:
                retobj = repFactory.getRetObj(MessageUtil.RESP_MESSAGE_TYPE_TEXT)
                retobj.setMsgType(MessageUtil.RESP_MESSAGE_TYPE_TEXT)
                retobj.setContent(ret.get('text'))
            elif ret.get('code') == 200000:
                retobj = repFactory.getRetObj(MessageUtil.RESP_MESSAGE_TYPE_NEWS)
                retobj.setMsgType(MessageUtil.RESP_MESSAGE_TYPE_NEWS)
                aas = []
                a = Article()
                a.setTitle('test')
                a.setDescription('test')
                a.setUrl(ret.get('url'))
                a.setPicUrl(
                    u'http://images.cnitblog.com/blog/370046/201310/07160044-e2bf032c27f94f778132cb4a9e06431a.png')
                aas.append(a)
                retobj.setArticleCount(len(aas))
                retobj.setArticles(aas)
            elif ret.get('code') == 302000:
                retobj = repFactory.getRetObj(MessageUtil.RESP_MESSAGE_TYPE_NEWS)
                retobj.setMsgType(MessageUtil.RESP_MESSAGE_TYPE_NEWS)
                aas = []
                maxtime = 5
                for new in ret.get('list'):
                    a = Article()
                    a.setTitle(new.get('article'))
                    a.setUrl(new.get('detailurl'))
                    a.setPicUrl(new.get('icon'))
                    aas.append(a)
                    if maxtime <= 0:
                        break
                    else:
                        maxtime = maxtime - 1
                retobj.setArticleCount(len(aas))
                retobj.setArticles(aas)
            elif ret.get('code') == 308000:
                retobj = repFactory.getRetObj(MessageUtil.RESP_MESSAGE_TYPE_NEWS)
                retobj.setMsgType(MessageUtil.RESP_MESSAGE_TYPE_NEWS)
                aas = []
                maxtime = 5
                for new in ret.get('list'):
                    a = Article()
                    a.setTitle(new.get('name'))
                    a.setDescription(new.get('info'))
                    a.setUrl(new.get('detailurl'))
                    a.setPicUrl(new.get('icon'))
                    aas.append(a)
                    if maxtime <= 0:
                        break
                    else:
                        maxtime = maxtime - 1
                retobj.setArticleCount(len(aas))
                retobj.setArticles(aas)
            else:
                retobj = repFactory.getRetObj(MessageUtil.RESP_MESSAGE_TYPE_TEXT)
                retobj.setMsgType(MessageUtil.RESP_MESSAGE_TYPE_TEXT)
                retobj.setContent(ret.get('text'))
        elif msgType == MessageUtil.REQ_MESSAGE_TYPE_IMAGE:
            respContent = u'您发送的是图片消息！'
        elif msgType == MessageUtil.REQ_MESSAGE_TYPE_VOICE:
            respContent = u'您发送的是语音消息！'
        elif msgType == MessageUtil.REQ_MESSAGE_TYPE_VIDEO:
            respContent = u'您发送的是视频消息！'
        elif msgType == MessageUtil.REQ_MESSAGE_TYPE_LOCATION:
            respContent = u'您发送的是地理位置消息！'
        elif msgType == MessageUtil.REQ_MESSAGE_TYPE_LINK:
            respContent = u'您发送的是链接消息！'
        elif msgType == MessageUtil.REQ_MESSAGE_TYPE_EVENT:
            eventType = requestMap.get(u'Event')
            if eventType == MessageUtil.EVENT_TYPE_SUBSCRIBE:
                respContent = u'^_^谢谢您的关注，本公众号由vr7jj基于WeiPython开发。如果你有兴趣继续开发，' \
                              u'，源码请联系:vr7jj2016@163.com.'
            elif eventType == MessageUtil.EVENT_TYPE_UNSUBSCRIBE:
                pass
            elif eventType == MessageUtil.EVENT_TYPE_SCAN:
                # TODO
                pass
            elif eventType == MessageUtil.EVENT_TYPE_LOCATION:
                # TODO
                pass
            elif eventType == MessageUtil.EVENT_TYPE_CLICK:
                # TODO
                pass

        if msgType == MessageUtil.REQ_MESSAGE_TYPE_TEXT:
            retobj.setToUserName(fromUserName)
            retobj.setFromUserName(toUserName)
            retobj.setCreateTime(time.time())
            respXml = MessageUtil.class2xml(retobj)
        else:
            textReply.setContent(respContent)
            respXml = MessageUtil.class2xml(textReply)
        return respXml



        """
        if msgType == 'text':
            content = requestMap.get('Content')
            # TODO

        elif msgType == 'image':
            picUrl = requestMap.get('PicUrl')
            # TODO

        elif msgType == 'voice':
            mediaId = requestMap.get('MediaId')
            format = requestMap.get('Format')
            # TODO

        elif msgType == 'video':
            mediaId = requestMap.get('MediaId')
            thumbMediaId = requestMap.get('ThumbMediaId')
            # TODO

        elif msgType == 'location':
            lat = requestMap.get('Location_X')
            lng = requestMap.get('Location_Y')
            label = requestMap.get('Label')
            scale = requestMap.get('Scale')
            # TODO

        elif msgType == 'link':
            title = requestMap.get('Title')
            description = requestMap.get('Description')
            url = requestMap.get('Url')
        """
