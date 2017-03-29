# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
import random
from django.http import JsonResponse


# Create your views here.
# class ServerInterfaceView(View):
#
#     def get(self, request):
#         print "get"
#         return HttpResponse("hello")
#
#     def post(self, request):
#         print "post"
#         return HttpResponse("world")
def dict_factory(cursor, row):
    '''
    # 指定工厂方法让sqlite3返回字典类型
    :param cursor:
    :param row:
    :return:
    '''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def index(request):
    return HttpResponse(u"欢迎使用vr7jj提供的api")


def ss(request):
    import sqlite3
    conn = sqlite3.connect("Untitled.sqlite3")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # cur.execute("select sitename,ip,port,password,mode from ssinfo")
    # 随即取一条
    cur.execute("SELECT sitename,ip,port,password,mode FROM ssinfo ORDER BY RANDOM() LIMIT 1")
    data = cur.fetchone()
    cur.close()
    return JsonResponse(data)
