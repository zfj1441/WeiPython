#!/bin/sh

cd /root/WeiPython
cmd="T$1"
if [ "$cmd" == "Tstart" ]
then
	echo "启动"
	python /root/WeiPython/manage.py runserver 0.0.0.0:8000 &
elif [ "$cmd" == "Tstop" ]
then
	echo "停止"
	ps |grep manage.py | grep -v grep | awk '{print $1}' | xargs kill -9
else
	echo "usage: $0 start|stop"
fi
