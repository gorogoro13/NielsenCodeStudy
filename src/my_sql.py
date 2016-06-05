# -*- coding: utf-8 -*-
""" analist Nielsen's Network """
"""VERSION 0.10"""
# TODO pandas Library  http://www15191ue.sakura.ne.jp:8000/home/pub/64/
# TODO 数値型(データ型)のまとめ http://pentan.info/sql/mysql/mysql_type_num.html
# TODO numpyの型 http://oppython.hatenablog.com/entry/2015/09/13/151235
# TODO RubyとPythonとC#のround関数のバグっぽい挙動について http://d.hatena.ne.jp/hnw/20131229
# TODO 浮動小数点演算、その問題と制限 http://docs.python.jp/2/tutorial/floatingpoint.html
# TODO Mysqlに格納する数値の型はDECIMALにしたほうがよい？
# 16．データ型と最小値/最大値 http://www.cgis.biz/others/mysql/16/
"""
tinyint			-128	127
tinyint(unsigned)	0	255
smallint		-32768	32767
smallint(unsigned)	0	65535
mediumint		-8388608	8388607
mediumint(unsigned)	0	16777215
int			-2147483648	2147483647
int(unsigned)		0	4294967295
bigint			-9223372036854775808	9223372036854775807
bigint(unsigned)	0	18446744073709551615
decimal		decimal(M,D)で指定。Mは桁数、Dは小数点以下の桁数
■http://www.risewill.co.jp/blog/archives/1111
特定のデータベースのデータを dump バックアップ
$ mysqldump --single-transaction -u root -p data2 > data2.sql
特定のデータベースのみ復元
$ mysql -u root -p data2 < data2.sql
ファイルに出力する方法
tee 出力先ファイルパス # 出力開始
notee #出力終了
"""
import MySQLdb
#import numpy as np
import struct
import binascii
""" データベースを作成することはできないのであらかじめ作成しておく
mysql -u root -p
作成
>CREATE DATABASE  IF NOT EXISTS db_name;
テーブルの構造を見る
>use db_name
>show columns from TABLENAME;
各レコードごと縦表示する \Gをつけると;は付けない。
>select * from table_name\G
ログインの際にページングオプションを指定する
>mysql --pager='less -S' -u user -ppassword -h host
削除
>DROP DATABASE db_name;
"""

""" データベースに接続する　"""
def Mconnect(dbname):
    connector = MySQLdb.connect(host="localhost",
                            db=dbname, user="root", passwd="at0830", charset="utf8")
    return connector

""" 単一レイヤーのCHAR(16)ノードテーブルを作る　"""
def CrtTble(connector,tbl_name,col_prefix,col_num):
    cursor = connector.cursor()
    col_names = _gen_col_char20(col_prefix,col_num)
    #sql = "CREATE TABLE " + tbl_name + "(" + col_names + ")" + " ENGINE=InnoDB ROW_FORMAT=Dynamic;"
    sql = "CREATE TABLE " + tbl_name + "(" + col_names + ")" + " ENGINE=MyISAM ROW_FORMAT=Dynamic;"
    cursor.execute(sql)
    return cursor

""" 単一レイヤーのFloatノードテーブルを作る　"""
def CrtTble_F(connector,tbl_name,col_prefix,col_num):
    cursor = connector.cursor()
    col_names = _gen_colname4(col_prefix,col_num)
    sql = "CREATE TABLE " + tbl_name + "(" + col_names + ");"
    cursor.execute(sql)
    return cursor

""" MNISTデータのテーブルを作る　"""
def CrtTbleMNIST(connector,tbl_name,col_prefix,col_num):
    cursor = connector.cursor()
    col_names = _gen_colnameMNIST(col_prefix,col_num)
    sql = "CREATE TABLE " + tbl_name + "(" + col_names + ");"
    cursor.execute(sql)
    return cursor

"""16進数ダンプしてFloat64を格納する　"""
def insert_f64CHAR16(tbl_name, cursor, all_list):
    ch16 = []
    ch16.append(all_list[0])
    ch16.append(all_list[1])
    ch16.append(all_list[2])
    al = all_list[3:]
    for a in al:
        ch16.append(binascii.hexlify(struct.pack("!d", a)))
    sql = "INSERT INTO " + tbl_name + " VALUES " + str(tuple(ch16)) + ";"
    #    print sql
    cursor.execute(sql)

"""NDArrayをデータベースに格納する　"""
def insert_nda(tbl_name, cursor, all_list):

    sql = "INSERT INTO " + tbl_name + " VALUES " + str(tuple(all_list)) + ";"
#    print sql
    cursor.execute(sql)
"""(クラスメソッド)CHAR(16)で保存するカラム名の生成"""
def _gen_col_char20(prefix,num):
    colnames = "Epc TINYINT unsigned, batch INT unsigned, chr TINYINT unsigned"
    for col in xrange(1,num+1):
        col4 = "{0:04d}".format(col)
        colname = prefix + col4
        #colnames = colnames + ", " + colname + " VARCHAR(255) NOT NULL"
        colnames = colnames + ", " + colname + " CHAR(16) NOT NULL"
    return colnames


"""(クラスメソッド)カラム名の生成"""
def _gen_colname4(prefix,num):
    colnames = "Epc TINYINT unsigned, batch INT unsigned, chr TINYINT unsigned"
    for col in xrange(1,num+1):
        col4 = "{0:04d}".format(col)
        colname = prefix + col4
        colnames = colnames + ", " + colname + " FLOAT NOT NULL"
    return colnames

"""(クラスメソッド)MNISTデータ用のカラム名の生成"""
def _gen_colnameMNIST(prefix,num):
    colnames = "id INT unsigned NOT NULL PRIMARY KEY "
    for col in xrange(1,num+1):
        col4 = "{0:04d}".format(col)
        colname = prefix + col4
        colnames = colnames + ", " + colname + " FLOAT NOT NULL"
    return colnames

"""テーブルから1行を取り出す"""
def read_one_row(db_name,tbl_name,epc,bat,chr):
    connector = MySQLdb.connect(host="localhost",
                                db=db_name, user="root", passwd="at0830", charset="utf8")
    cursor = connector.cursor()

    sql = "SELECT * FROM " + tbl_name + " WHERE Epc = " + str(epc) \
                    + " AND batch = " + str(bat) + " AND chr = " + str(chr) + ";"

    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    connector.close()

    return result

"""テーブルから最終1行をFloat64として取り出す"""
def read_Last_one_row_F(cursor,tbl_name):
    # connector = MySQLdb.connect(host="localhost",
    #                            db=db_name, user="root", passwd="at0830", charset="utf8")
    #cursor = connector.cursor()
    sql = "SELECT * FROM " + tbl_name + " order by batch desc limit 1;"
    cursor.execute(sql)
    result = cursor.fetchall()
    data = list(result[0])
    for col in xrange(3, len(data)):
        b = struct.unpack('!d', binascii.unhexlify(data[col]))[0]
        data[col] = b
    return data

"""テーブルから1行を辞書で取り出す"""
def read_one_row_dic(db_name,tbl_name,epc,bat,chr):
    connector = MySQLdb.connect(host="localhost",
                                db=db_name, user="root", passwd="at0830", charset="utf8",
                                cursorclass=MySQLdb.cursors.DictCursor )
    cursor = connection.cursor()
    sql = "SELECT * FROM " + tbl_name + " WHERE Epc = " + epc \
          + " batch = " + bat + " chr = " + chr +";"
    cursor.execute(sql)
    result_dic = cursor.fetchall()
    return result_dic

"""テーブルから全ての行を取り出す"""
def read_all(db_name,tbl_name):
    connector = MySQLdb.connect(host="localhost",
                                db=db_name, user="root", passwd="at0830", charset="utf8")
    cursor = connector.cursor()
    sql = "SELECT * FROM " + tbl_name + ";"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

"""テーブルから全ての行をfloat64として取り出す"""
def read_all_row_F(cursor, tbl_name):
    #connector = MySQLdb.connect(host="localhost",
     #                           db=db_name, user="root", passwd="at0830", charset="utf8")
    #cursor = connector.cursor()
    sql = "SELECT * FROM " + tbl_name + ";"
    cursor.execute(sql)
    result = cursor.fetchall()
    f = []

    for row in xrange(0, len(result)):
        hex_data = list(result[row])
        data = []
        for col in xrange(3, len(hex_data)):
            data.append(struct.unpack('!d', binascii.unhexlify(hex_data[col]))[0])
        f.append(data)
    return f