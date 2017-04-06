###WeiPython
python2.7+django1.4。
封装了微信开发需要的一些类和函数，包括三种消息类，xml文件的解析和生成, json解析等。
你可以在此基础上开发练手。你只需要克隆代码，然后实现wechatService.py里的processRequest方法就可以根据不同消息类型回复。目前实现的是调用[图灵机器人](http://www.tuling123.com/openapi/)自动回复，可以实现翻译，查询天气，简单聊天等功能。(初学python时练手的，代码非常不pythonic，慎用代码)

###Step
- Clone this reposity: `git clone https://github.com/PegasusWang/WeiPython.git`
- Write your own processRequest in wechatService.py
- upload your code to sae or bae server.

###ChangeLog
20170405  
1、使用新版django1.10.6版本重新部署  
2、增加404.html 500.html及相关解析  
3、tools增加解二维码功能

20170329  
1、增加server应用，对外提供api  
2、增加微信命令模式(查询远端数据库)

20170316  
1、修改class2xml中组织xml错误  
2、新增返回对象工厂类repFactory  
3、增加tuling返回图文消息

20170311  
修改部分BUG

###remark
runcode:python manage.py runserver 0.0.0.0:8000

###[Tutorial](http://ningning.today/2015/02/21/python/django-python%E5%BE%AE%E4%BF%A1%E5%BC%80%E5%8F%91%E4%B9%8B%E4%B8%80%EF%BC%8D%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C/)

