# -*- coding:utf-8 -*-
# -*-coding:utf8 -*-

import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class dbTools():
    MYCMD_TYPE = ['c']

    @staticmethod
    def getMsgByMobile(mobile):
        #        db = MySQLdb.connect("qdm115673525.my3w.com", "qdm115673525",
        #                             "zfj1441520", "qdm115673525_db", charset="utf8")
        db = MySQLdb.connect("192.168.1.1", "vr7jj", "zfj1441520", "homedb", charset="utf8")
        retmsg = '0\n';
        cursor = db.cursor()
        sql = "SELECT * FROM trans_msg where mobile like '%" \
              + str(mobile) + "%' LIMIT 30"
        print sql
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                retmsg = retmsg + str(row[5]) + '|' + str(row[2])[:10] + "|" \
                         + str(row[4]) + "|" + str(row[14]) + "|\n"
        except Exception as e:
            print e
            retmsg = "1\n" + e.message
        db.close()
        return retmsg


if __name__ == "__main__":
    print(dbTools.getMsgByMobile("18607093708"))
