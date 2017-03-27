# -*- coding:utf-8 -*-
from zxing import *


def test_barcode_parser():
    text = """
file:/home/oostendo/Pictures/datamatrix/4-contrastcrop.bmp (format: DATA_MATRIX, type: TEXT):
Raw result:
36MVENBAEEAS04403EB0284ZB
Parsed result:
36MVENBAEEAS04403EB0284ZB
Also, there were 4 result points.
  Point 0: (24.0,18.0)
  Point 1: (21.0,196.0)
  Point 2: (201.0,198.0)
  Point 3: (205.23952,21.0)
"""

    barcode = BarCode(text)
    if (barcode.format != "DATA_MATRIX"):
        return 0

    if (barcode.raw != "36MVENBAEEAS04403EB0284ZB"):
        return 0

    if (barcode.data != "36MVENBAEEAS04403EB0284ZB"):
        return 0

    if (len(barcode.points) != 4 and barcode.points[0][0] != 24.0):
        return 0

    return 1


def test_codereader(imagepath):
    # ~ zx = BarCodeReader(zxing_location)
    zx = BarCodeReader("zxing")

    barcode = zx.decode(imagepath)
    return barcode.data
    # if re.match("http://", barcode.data):
    #   return 1
    # return 0


if __name__ == "__main__":
    import base64

    zxing_location = ".."
    testimage = "res/qr.png"
    data = test_codereader(testimage)
    print data
    # print base64.b64decode(data.split("ss://")[1])
