# -*-coding:utf-8 -*-
__author__ = 'cwq'

import qrcode  # 导入模块

qr = qrcode.QRCode(
    version=8,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=50,
    border=4,
)
qr.add_data('http://vr7jj.ngrok.cc/wechat')
qr.make(fit=True)

img = qr.make_image()
img.save("advanceduse.png")
