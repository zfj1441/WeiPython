# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from server import views

urlpatterns = [
    # url(r'^$', csrf_exempt(views.ServerInterfaceView.as_view())),
    url(r'^$', views.index, name='index'),
    url(r'^ss$', views.ss, name='ss'),
]
