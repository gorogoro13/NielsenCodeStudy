# -*- coding: utf-8 -*-
desc = """
network.py "第1引数：テーブル名" "第2引数：DB名"
~~~~~~~~~~
SQL問い合わせで得た結果（16進数ダンプだれたfloat64）をFloat64に変換して（指数部のない）少数で表示する。
出力は、各カラムの値、合計、最大、最小。
"""
import os
import sys # モジュール属性 argv を取得するため
import MySQLdb
#import numpy as np
import struct
import binascii
argvs = sys.argv  # コマンドライン引数を格納したリストの取得
argc = len(argvs) # 引数の個数
# デバッグプリント
#print argvs
#print argc
print
if (argc != 3):   # 引数が足りない場合は、その旨を表示
    print "Usage: \n $ python  {0}".format(desc)
    quit()         # プログラムの終了
print "The last row of Table: {0} in {1}(DB).".format(argvs[1], argvs[2])

pid = os.getpid()
print "PID: {0}".format(pid)
f = open('28by28weight.pid', 'w')
f.write(str(pid))
f.close()

tbl_name = argvs[1]
db = argvs[2]
connector = MySQLdb.connect(host="localhost",
                           db=db, user="root", passwd="at0830", charset="utf8")
cursor = connector.cursor()
sql = "SELECT * FROM " + tbl_name + " order by batch desc limit 1;"
cursor.execute(sql)
result = cursor.fetchall()
data = list(result[0])
sum = 0
fnum = []
for col in xrange(3, len(data)):
    b = struct.unpack('!d', binascii.unhexlify(data[col]))[0]
    sum += b
    print "{0:.11f}".format(b)
    data[col] = b # 関数にして利用する場合は、　return data
    fnum.append(b)
print "合計＝ {0:.11f}".format(sum)
#print fnum
#sys.exit("Done.")

print "最大値＝ {0:.11f}".format(max(fnum))
print "最小値＝ {0:.11f}".format(min(fnum))

