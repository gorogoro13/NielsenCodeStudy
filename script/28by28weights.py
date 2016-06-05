# -*- coding: utf-8 -*-
"""
28by28weight.py
~~~~~~~~~~
$ python 28by28weight.py
"""
import numpy as np
import my_sql as ms
import MySQLdb
import matplotlib.pyplot as plt
import os
import struct
import binascii
import atexit
import sys


def tbl_sets(size):
    """
    set[0] = ['act_L1']
    set[1] = ['act_L2', 'b_L2', 'w_L2_j0001', 'w_L2_j0002', ...
    set[2] = ['act_L3', 'b_L3', 'w_L3_j0001', 'w_L3_j0002',...

    """
    set = [[]]
    set[0].append("act_L1")
    for l in xrange(2, len(size)+1):
        set.append([])
        set[l-1].append("act_L" + str(l))
        set[l-1].append("b_L" + str(l))
        for i in xrange(1,size[l-1]+1):
            set[l-1].append("w_L" + str(l) + "_j" + "{0:04d}".format(i))
    return set

"""テーブルから全行をFloat64として取り出す"""
def read_All_row_F(cursor,tbl_name):
    # connector = MySQLdb.connect(host="localhost",
    #                            db=db_name, user="root", passwd="at0830", charset="utf8")
    #cursor = connector.cursor()
    sql = "SELECT * FROM " + tbl_name

    cursor.execute(sql)
    result = cursor.fetchall()
    data =[]

    for row in xrange(0,len(result)):
        data.append(list(result[row]))
        #for a in row[0:3]:
        #    data[row].append(a)
        for col in xrange(3, len(data[row])):
            b = struct.unpack('!d', binascii.unhexlify(data[row][col]))[0]
            data[row][col] = b
    return data

"""  """
def draw_one(title):
    print "dummy"

""" CLOSER """
def all_done(cursor, connection):
    cursor.close()
    connection.close()
    print "DB connection is closed."

# matplotlib  http://seesaawiki.jp/met-python/d/matplotlib

if __name__ =='__main__':
    # プロセスID
    pid = os.getpid()
    print pid
    f = open('28by28weight.pid', 'w')
    f.write(str(pid))
    f.close()
    #
    db = "epoch_01_a"
    sizes = [784,30,10]
    #row_num =28
    #col_num=28
    #x = np.arange(5001)
    #y = np.arange(5001)
    connector = MySQLdb.connect(host="localhost",
                                db=db, user="root", passwd="at0830", charset="utf8")
    cursor = connector.cursor()
    atexit.register(all_done,cursor,connector)
    #tables = tbl_sets([784,30,10])
    #ms.read_all_row_F(cursor,tbl_name)

    """ L2 """
    #TODO 多分この for n のブロックは不要
    #for n in xrange(0,784):
    tables = tbl_sets(sizes)
    for j in xrange(3, len(tables[1])):
        #if j == 3:
        #    sys.exit("Done.")
        tbl_name = tables[1][j]
        #all_row = read_All_row_F(cursor, tbl_name)
        for col in xrange(3, sizes[0] + 3):

            # 列ごとに全レコードを読み込む
            #TODO SQLで間引く
            sql = "select w_" + "{0:04d}".format(col -2) + " from " + tbl_name + ";"
            cursor.execute(sql)
            results = cursor.fetchall()
            #print  results[col][0]
            #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            # サンプリング数を減らす
            x = np.arange((len(results)-1)/1)
            y = []
            for row in xrange(0,(len(results)-1)/1):
                b = struct.unpack('!d', binascii.unhexlify(results[row * 1][0]))[0]
                #print b
                #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                y.append(float(b))

            #plt.subplot(row_num, col_num, n)
            #if col == 4 and j == 1:
            plt.hold(False)
            plt.plot(x, y)
            title = tbl_name + "_w_" + "{0:04d}".format(col -2)
            plt.title(title)
            plt.grid()

            p_dir = "g_pict/"
            file_name = title + ".eps"
            plt.savefig(p_dir + file_name, dpi=100, bbox_inches = 'tight')
            #plt.show()

"""
PythonTeXに半自動的にLaTeXドキュメントに埋め込む http://xaro.hatenablog.jp/entry/2013/09/16/155444
"""