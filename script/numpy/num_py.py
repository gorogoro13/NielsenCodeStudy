# -*- coding: utf-8 -*-
"""
num_py.py
~~~~~~~~~~
numpyの演算を数値で確認する
（参考：http://naoyat.hatenablog.jp/entry/2011/12/29/021414）
"""
import numpy as np
""" 添字アクセス、スライス、イテレート """
#一次元配列
def d_1():
    a = np.arange(10)**3
    print "a = np.arange(10)**3\na = {0}".format(a)
    #array([  0,   1,   8,  27,  64, 125, 216, 343, 512, 729])
    print "a[2] = {0} ".format(a[2])
    #8
    print "a[2:5] = {0}".format(a[2:5])
    #array([ 8, 27, 64])
    a[:6:2] = -1000
    print "a[:6:2] = -1000 \na = {0}".format(a)    # a[0:6:2] = -1000 と等価; 最初から位置6の手前まで、要素1つおきに-1000にセット
    #array([-1000,     1, -1000,    27, -1000,   125,   216,   343,   512,   729])

    print "a[ : :-1] = {0}".format(a[ : :-1])                                 # 反転されたa
    #array([  729,   512,   343,   216,   125, -1000,    27, -1000,     1, -1000])

    print "for i in a:"
    for i in a:
        print "    i = {0}".format(i)

#多次元配列は軸ごとに添字を１つ持つことができる。これらの添字はカンマ区切りのタプルで与えられる：
def f(x,y):
    return 10*x+y

def d_2():
    b = np.fromfunction(f,(5,4),dtype=int)
    print ">>> b = fromfunction(f,(5,4),dtype=int) = \n{0}".format(b)
    print ">>> b[2,3] = \n{0}".format(b[2,3])
    print ">>> b[0:5, 1] = \n{0}".format(b[0:5, 1])                       # bの各行の2列目
    print ">>> b[ : ,1] = \n{0}".format(b[ : ,1])                        # 前の例と等価
    print ">>> b[1:3, : ] = \n{0}".format(b[1:3, : ])                      # bの2行目3行目の各列
    print "与えられた添字の数が軸数より少ない場合、足りない添字は完全なスライスと見なされる："
    print ">>> b[-1] = \n{0}".format(b[-1])                                  # 最後の行。b[-1,:] と等価。
    print "多次元配列のイテレートは最初の軸に関して行われる："
    print "for row in b:"
    for row in b:
        print "row = {0}".format(row)
    print "しかし、配列の各要素についてある演算を行いたい場合には、配列の全要素を渡り歩くイテレータであるflat属性が使える："
    print "for element in b.flat:"
    for element in b.flat:
        print "element = {0}".format(element)
    print "配列には、各軸沿いの要素数によって与えられた形状(shape)がある："
    print "b.shape = {0}".format(b.shape)
    print "配列の形状は、様々なコマンドで変更できる："
    print "b.ravel() = {0}".format(b.ravel())# 配列を解きほぐして(ravel)平らにする
    print "b.shape = (5, 2) = \n{0}".format(b)
    print "b.transpose() = \n{0}".format(b.transpose())
    txt = """ravel() の結果として得られる配列に含まれる要素の順序は普通に "C-style"、即ち、一番右の添字が「最初に変わる」ので、a[0,0]の次に来る要素はa[0,1]である。他の形状に再整形されても、配列は再び "C-style" として扱われる。Numpyは普通ravel()が引数をコピーしなくてもいいようにこの順序で格納して配列を作成するが、その配列が他の配列をスライスして作られたものであったり、一般的でないオプションで作られたものである場合、コピーが必要になるかもしれない。関数 ravel(), reshape() はオプション引数を指定することで、FORTRAN形式の配列を用いるようにもできる。その場合、一番左の添字が最初に変わる。
reshape関数はその引数を修正された形状で返す一方で、resizeメソッドは配列そのものを修正する："""
    print txt
    a_txt = """a = np.array([[ 7.,  5.],
               [ 9.,  3.],
               [ 7.,  2.],
               [ 7.,  8.],
               [ 6.,  8.],
               [ 3.,  2.]])"""
    a = np.array([[ 7.,  5.],
                  [ 9.,  3.],
                  [ 7.,  2.],
                  [ 7.,  8.],
                  [ 6.,  8.],
                  [ 3.,  2.]])
    print a_txt
    print "a.resize((2,6))".format(a.resize((2,6)))
    print "再整形操作において寸法が-1で与えられた場合、他の寸法は自動的に算出される："
    print "a.reshape(3,-1) = \n{0}".format(a.reshape(3,-1))
#d_1()
d_2()