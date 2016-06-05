# -*- coding: utf-8 -*-
"""
my_debug
~~~~~~~~~~
Waiting next output for debug-info.
To copy /home/grgr13/276virt/lib/python2.7/site-packages/my_scripts/my_debug.py
"""

#### Libraries
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
from numpy import random
import tempfile
import os
import datetime

#from tensorflow.examples.tutorials.mnist import input_data

def write_log(file, text):
    """07. Pythonのファイル操作
    https://sites.google.com/site/kuraitlab/programing-language/python/file-operations
    """
    f = open(file, 'a')
    f.write(str(text) + "\n")
    f.close()

def waitkey():
    waitingKeyPress = True
    while waitingKeyPress: #スペースキーが押されるのを待つ
        for e in event.get():
            if e.type == KEYDOWN and e.key == K_SPACE:
                waitingKeyPress = False

# MINSIT data Util, View a charactor ect...
def _to_number(label):
    for index, n in enumerate(label):
        if n != 0:
            return index

def view_a_charactor():
    """
    http://blog.amedama.jp/entry/2016/02/08/204551
    からコピー。
    引数：行列（リスト）…具体的にはニューロンネットの重みやバイアスを想定。
    戻値：pltオブジェクト…描画するか、ファイルに落とすかは呼び出し側に任せる。

    """
    #TODO Description matter.
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    X = mnist.train.images
    y = mnist.train.labels

    # データの中から 25 点を無作為に選び出す
    p = random.random_integers(0, len(X), 25)

    # 選んだデータとラベルを matplotlib で表示する
    samples = np.array(list(zip(X, y)))[p]
    for index, (data, label) in enumerate(samples):
        # 画像データを 5x5 の格子状に配置する
        plt.subplot(5, 5, index + 1)
        # 軸に関する表示はいらない
        plt.axis('off')
        # データを 8x8 のグレースケール画像として表示する
        plt.imshow(data.reshape(28, 28), cmap=cm.gray_r, interpolation='nearest')
        n = _to_number(label)
        # 画像データのタイトルに正解ラベルを表示する
        plt.title(n, color='red')
    # グラフを表示する
    plt.show()



# List Utility
def List2slFile():
    """
    List to siliarized FIle.
    リストオブジェクト（ネストしていてOK)をシリアライズしてファイルに書き込む。
    シリアライズ＞
    ＞[]はそのまま使うが１文字で改行する。
    ＞１要素１行（つまりカンマ","は使わないで、改行でデータ区切りとする。
    復元＞別ルーチンに実装する。
    引数：リストオブジェクト（ネストしていてOK)
    引数：書き出すディレクトリ
    引数：書き出すファイル名
    引数（オプション）：プレフィックス。省略時は"a_"
    戻値：成功した場合はtrueを返す。
    """
    #TODO 実装
    # tempfile.mkdtemp(dirpath)の使い方がわからない。/tmp/以下にランダムな名前のディレクトリが作成されて、その下にdirpath
    # で指定したディレクトリを作成しようとしているみたいだが、そのディレクトリにアクセスするためにランダムな名前はどうやって取得する？

    w_pid() # pidを記録
    # 一時ディレクトリ
    dirpath = "List2slFile_tmp"
    #temp_fname = "tmp_List2slFile.txt"
    if os.path.exists(dirpath) == False :
        tempfile.mkdtemp(dirpath) # 可能な限り最もセキュアな方法で、一時ディレクトリを作成します。

    # 一時ファイル
    suffix = ".txt"
    prefix = "tmp_List2slFile"
    if os.path.exists(dirpath + "/" + prefix + suffix) == False:
        tempfile.mkstemp(".txt", "tmp_List2slFile",dirpath,True)#可能な限り最もセキュアな方法で、一時ファイルを作成します。


def Listes2a_parameta_timeline():
    """
    List2slFileで時系列に書きだされた複数ファイルから、個々の要素（パラメーター）だけを時系列に沿って
    順番に並べたリストにする。
    引数：
    引数（オプション）："list"リストオブジェクトを返す（サイズ上限あり）　"file"List2slFile形式のファイルに書き出す。
    戻値：引数（オプション）に従う。"file"で成功した場合はtrueを返す。
    """
    #TODO 実装


# NdArray Utility

# OS Util
# 15.1. os — 雑多なオペレーティングシステムインタフェース
# http://docs.python.jp/2/library/os.html
def w_pid(filename = "pid.txt"):
    fn = filename
    # if os.path.exists("./" + filename) == False or os.path.isfile("./" + filename) == False :
    # f = open(fn, 'w') # ファイルが存在していない場合は新規作成（されるのか？）。されるとしてそれに任せる。
    pid = os.getpid()
    d = datetime.datetime.today()
    time_str = d.strftime("%Y-%m-%d %H:%M:%S") # , '\n' 追記ファイルにする場合
    name = os.ctermid() #プロセスの制御端末に対応するファイル名
    s = str(pid) + "    " + time_str + "    " + name
    print s
    f = open(fn, 'w') # ファイルが存在していない場合は新規作成（されるのか？）。
    f.write(str(s))
    f.close()

# MySQL Util
#TODO 巨大なArrayをファイルに書きだすのは心もとないので、MySQLに書き出す。SQLはデータの分析にも使える。

def main():
    print " "

def print_OK():
    print "IMPORT OK."

if __name__ == '__main__':
    main()
