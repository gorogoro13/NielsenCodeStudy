# -*- coding: utf-8 -*-
"""
network.py
~~~~~~~~~~

A module to implement the stochastic gradient descent learning
algorithm for a feedforward neural network.  Gradients are calculated
using backpropagation.  Note that I have focused on making the code
simple, easily readable, and easily modifiable.  It is not optimized,
and omits many desirable features.
「確率的勾配下降法(SGD)」を用いた「順伝播型ニューラルネットワーク」の
モジュール。「誤差逆伝播法」を用いて「勾配下降」が計算される。

VERSION 0.11
・self.baiases, self.weights の保存と読み込みによって、継続的に学習を進められる。
#TODO
・バッチごとに（baiases, baiases)と一文字ごとのactivationsを保存する現在のモードと、
Epoch単位の最終パラメーターだけを保存できるモード（新たに実装）を使い分け出来るようにする。
・”読み込み先DB”と”保存先DBをパラメータで指定できるようにする。”
・現在はhexモードのみだが、floatモードの効率・正確性との比較で、必要なら使い分けできるようにする。
"""


#### Libraries
# Standard library
import random
import sys
# Third-party libraries
import numpy as np
import timer as tm
# my_libraries
import my_debug
import my_sql as ms
import my_datetime as dt
#import my_draw_data as dd
# atexit – プログラムの終了時に関数を呼び出す http://ja.pymotw.com/2/atexit/
import atexit
import sys

#TODO　モード"hex"
""" http://qiita.com/shibukawa/items/682f0f86dc7bf8ea5869
float64はIEEE-754の64ビット(符号1ビット、仮数52ビット、指数11ビット 合計64ビット=>16桁の16進数)
MySQLカラムをCHAR(16)で宣言。文字列として格納する。
float64はstruct.packを使ってバイト配列にして、その後formatで16進数の文字列にします。
ネットワークバイトオーダーで出しています。
>>> import numpy as np
>>> import struct
>>> import binascii
>>> a = np.float64(10.12345456)
>>> binascii.hexlify(struct.pack("!d", a))
'40243f356fa37bf1'
復元
>>> b = struct.unpack('!d', binascii.unhexlify('40243f356fa37bf1'))[0]
>>> a == b
True
"""
class Network(object):
    #TODO parameter d[d, dbname1] incriment[ incriment, dbname2]
    # d＝debugパラメータ　　incriment＝パラメータの継承　　hex＝float64を16進ダンプで保存
    def __init__(self, sizes, d = 0, incriment = False, hex = True):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.  Note that the first
        layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers.
        【意訳】
        sizes=[784, 30, 10]とした場合
        net = network.Network([784, 30, 10])とインスタンスを作成すると、
        リストの要素数(len)は総レイヤー数を表し、各要素は
        「784ニューロンの入力層,30ニューロンの中間層,10ニューロンの出力層」
        でネットワークを構築する。
        [784,90,30,10]とすれば、中間層は90ニューロンと30ニューロンの2層作成
        される。

        数学の行列は、1次元の横ベクトルの縦方向への集積となる。1次元の縦ベクトルは
        要素数１の横ベクトル（スカラー）を縦に集積したものとする。
        （参照）NumPy 配列の基礎  http://www.kamishima.net/mlmpyja/nbayes1/ndarray.html
        最後に， np.ndarray の1次元と2次元の配列と，数学の概念であるベクトル
        と行列との関係について補足します． 線形代数では，縦ベクトルや横ベクトル
        という区別がありますが，1次元の np.ndarray 配列にはそのような区別はあ
        りません． そのため，1次元配列を転置することができず，数学でいうところ
        のベクトルとは厳密には異なります．

        そこで，縦ベクトルや横ベクトルを区別して表現するには，それぞれ列数が1で
        ある2次元の配列と，行数が1である2次元配列を用います． 縦ベクトルは次のよ
        うになり:

        In [65]: np.array([[1], [2], [3]])
        Out[65]:
        array([[1],
            [2],
            [3]])
        横ベクトルは次のようになります（リストが2重にネストしていることに注意）:

        In [66]: np.array([[1, 2, 3]])
        Out[66]: array([[1, 2, 3]])

        """
        self.num_layers = len(sizes) #総レイヤー数
        self.sizes = sizes # [入力層のニューロン数、中間層のニューロン数、出力層の層のニューロン数]
        # バイアス値を各中間層と出力層の各ニューロン数のベクトル（リスト）で作成
        # sizes = [784, 30, 10] なら中間層30列1行のバイアス、出力層10列1行のバイアス 
        # np.random.randn(y,1)    # 標準正規分布(ガウシアン)による (y x 1) の行列
        # self.biases =  [  array([...[],[]...30要素]), ・・・ [1列30行]
        #                   array([...[],[]...10要素])  ] ・・・ [1列10行]
        # Numpy によるデータ行列の取り扱い
        # http://daemon.ice.uec.ac.jp/~shouno/2012.Programming/NumpyBasic.html
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]] # [1列30行][1列10行]
        if incriment == False:
            print "self.baiases  incriment == False"
        else:
            tmp_connection = ms.Mconnect("epoch_01")
            tmp_cursor = tmp_connection.cursor()
            if hex == True:
                print "self.baiases  hex == True"
                result_L2 = ms.read_Last_one_row_F(tmp_cursor, "b_L2")
                result_L3 = ms.read_Last_one_row_F(tmp_cursor, "b_L3")
                #print result_L3[0]
                #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                for i in xrange(0,sizes[1]):
                    self.biases[0][i] = result_L2[3+i]
                for j in xrange(0,sizes[-1]):
                    self.biases[1][j] = result_L3[3+j]
            else:
                sql = "select * from b_L2 order by batch desc limit 1;"
                tmp_cursor.execute(sql)
                result_L2 = tmp_cursor.fetchall()
                sql = "select * from b_L3 order by batch desc limit 1;"
                tmp_cursor.execute(sql)
                result_L3 = tmp_cursor.fetchall()
                #print result_L3[0]
                #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                for i in xrange(0,sizes[1]):
                    self.biases[0][i] = result_L2[0][3+i]
                for j in xrange(0,sizes[-1]):
                    self.biases[1][j] = result_L3[0][3+j]
            tmp_cursor.close()
            tmp_connection.close()
        #print "{0}".format(self.biases)
        #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        #---------------------------------------------------------------------------
        # 重み
        # 標準正規分布による sizes[:-1]× sizes[1:] の行列（順番的には列×行）・・・まちがい（行列順が逆）
        # sizes = [784, 30, 10] なら784列30行、30列10行を作成・・・まちがい（行列順が逆）
        # self.weights = [  array([...[784要素のリスト],[]...30個 ]),
        #                   array([...[30要素のリスト],...10個 ])  ]
        # 各層のactivationベクトルとの内積を計算するので、その向きに行列を合わせる。
        #TODO --その１ Strange bug. w_L3_j0001の最終レコードがw_L2_j0001 に挿入されてしまう。
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])] # [784列30行][30列10行]・・・まちがい（行列順が逆）
        if incriment == False:
            print "self.weight  incriment == False"
        else:
            tmp_connection = ms.Mconnect("epoch_01")
            tmp_cursor = tmp_connection.cursor()
            if hex == True:
                #TODO ndarray 行列 参照 https://www.google.co.jp/search?q=ndarray+%E8%A1%8C%E5%88%97+%E5%8F%82%E7%85%A7&ie=utf-8&oe=utf-8&aq=t&hl=ja&gws_rd=ssl
                """  ndarrayのスライシング
                2 次元以上の配列の場合、インデックスで参照した先は 1 次元以上の配列になります。
                >>> arr = np.array( [[[1,2,3], [4,5,6]], [[7,8,9],[10,11,12]]] )
                >>> arr.ndim # 次元数
                #=> 3
                >>> arr[0]
                #=> array([[1, 2, 3],
                #          [4, 5, 6]])
                # 2 次元配列が返る
                インデックスに配列を指定するとその分次元数を削減した配列を取り出せます。
                >>> arr[1,0]
                #=> array([7, 8, 9])
                >>> arr[1,0,2]
                #=> 9

                Row size too large (> 8126).
                http://qiita.com/hatappi/items/132f56c00e428beef777

                # http://oshiete.goo.ne.jp/qa/4747480.html
                Q:文字列サイズは文字数ではない？
                MySQL 4.1で仕様変更（unicodeの実装）があり、char(n)のnの意味が変わりました。
                MySQL 4.0まではバイト数、MySQL 4.1以降は文字数です。
                """
                #if hex == True:
                print "self.weights  hex == True"
                for i in xrange(1, sizes[1]+1):
                    tbl_name="w_L2" + "_j" + "{0:04d}".format(i)
                    result_L2 = ms.read_Last_one_row_F(tmp_cursor,tbl_name)
                    for e in xrange(0, sizes[0]):
                        self.weights[0][i-1][e] = result_L2[e+3]
                print "self.weights[0](L2-weights) is inserted."
                for j in xrange(1, sizes[-1]+1):
                    tbl_name="w_L3" + "_j" + "{0:04d}".format(j)
                    result_L3 = ms.read_Last_one_row_F(tmp_cursor,tbl_name)
                    for f in xrange(0, sizes[1]):
                        self.weights[1][j-1][f] = result_L3[f+3]
                print "self.weights[1](L3-weights) is inserted."
            else:
                for i in xrange(1, sizes[1]+1):
                    tbl_name="w_L2" + "_j" + "{0:04d}".format(i)
                    sql = "select * from " + tbl_name + " order by batch desc limit 1;"
                    tmp_cursor.execute(sql)
                    result_L2 = tmp_cursor.fetchall()
                    for e in xrange(0, sizes[0]):
                        #print "dummy"
                        self.weights[0][i-1][e] = result_L2[0][e]
                print "self.weights[0](L2-weights) is inserted."
                for j in xrange(1, sizes[-1]):
                    tbl_name="w_L3" + "_j" + "{0:04d}".format(j)
                    sql = "select * from " + tbl_name + " order by batch desc limit 1;"
                    tmp_cursor.execute(sql)
                    result_L3 = tmp_cursor.fetchall()
                    for f in xrange(0, sizes[1]):
                        self.weights[0][j-1][f] = result_L3[0][f]
                print "self.weights[1](L3-weights) is inserted."
            tmp_cursor.close()
            tmp_connection.close()
        #print "{0}".format(self.weights)
        #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # 0:"NO"    Nothing Do.
        # 1:"Debug" Debug messege.
        # 2:"VBouse"冗長なメッセージ
        # 3:"Write"
        # 4:"F-N"   最終ネットワークの重みとバイアスをファイルに書き出す。
        # 5:"BackProp" 逆伝播のみ表示する
        dbg=("No","Debug","VBouse","Write","F-N", "BackProp")
        self.dbg = dbg[d]
        if self.dbg == "Debug" or self.dbg == "BackProp":
            print "===ニューラルネットを初期化しました"
            print "レイヤー数(入力層＋中間層＋出力層)＝{0}".format(self.num_layers)
            print "入力層＝{0}ニューロン".format(self.sizes[0])
            print "中間層＝{0}ニューロン".format(self.sizes[1])# [1:-2]
            print "出力層＝{0}ニューロン".format(self.sizes[-1])
            self.mini_batch_num=0
            my_debug.print_OK()
        elif self.dbg == "Write":
            self.incriment = incriment
            self.db="epoch_02"
            self.batchs_num = 0
            self.char_num = 0
            self.Epochs_num = 0
            self.connection = ms.Mconnect(self.db)
            self.cursor = self.connection.cursor()
            """ 初期値のレコード """
            for l in xrange(2,self.num_layers+1):
                """ 「バイアス」 """
                tbl_name="b_L" + str(l)
                self.cursor = ms.CrtTble(self.connection,tbl_name,"b_",self.sizes[l-1])# baiases
                bs = []
                bs.append(self.Epochs_num)
                bs.append(self.batchs_num)
                bs.append(self.char_num)
                for bj in xrange(0,len(self.biases[l-2])):
                    bs.append((self.biases[l-2][bj][0]))
                ms.insert_f64CHAR16(tbl_name,self.cursor,bs)
                #connection.commit()
                """ 「重み」 """
                #TODO --その２ Strange bug. w_L3_j0001の最終レコードがw_L2_j0001 に挿入されてしまう。
                for j in xrange(1,self.sizes[l-1]+1):
                    tbl_name="w_L" + str(l) + "_j" + "{0:04d}".format(j)
                    self.cursor = ms.CrtTble(self.connection,tbl_name,"w_",self.sizes[l-2])
                    #self.connection.commit()
                    wt = []
                    wt.append(self.Epochs_num)
                    wt.append(self.batchs_num)
                    wt.append(self.char_num)
                    for wj in xrange(0, len(self.weights[l-2][j-1])):
                        #print self.weights[l-2][j-1][wj]
                        wt.append(self.weights[l-2][j-1][wj])
                    ms.insert_f64CHAR16(tbl_name,self.cursor,wt)
                tbl_name="act_L" + str(l-1)
                self.cursor = ms.CrtTble(self.connection,tbl_name,"a_",self.sizes[l-2])# activations入力〜中間層
                save_l = l
            tbl_name="act_L" + str(save_l)
            self.cursor = ms.CrtTble(self.connection,tbl_name,"a_",self.sizes[save_l-1])# activations出力層
            #connection.commit()
            tbl_name="Label"
            self.cursor = ms.CrtTble(self.connection,tbl_name,"n_",self.sizes[save_l-1])# activations出力層
            self.connection.commit()
            print "act_L{0} is created.".format(str(save_l))
            #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            test_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent.  The ``training_data`` is a list of tuples
        ``(x, y)`` representing the training inputs and the desired
        outputs.  The other non-optional parameters are
        self-explanatory.  If ``test_data`` is provided then the
        network will be evaluated against the test data after each
        epoch, and partial progress printed out.  This is useful for
        tracking progress, but slows things down substantially.
        「確率的勾配下降法(SGD)」
        self.update_mini_batch(mini_batch, eta)でWeightsとbaiasesを(誤差
        が減少する更新する方向に）更新する。
        training_data
        epochs　学習回数
        mini_batch_size　サンプリング数
        eta
        test_data=None
        """
        atexit.register(all_done,self)
        if self.dbg == "Debug":
            n_test = len(test_data)
            print "===SGD（確率的勾配下降法）を開始します"
            print "テストデータは{0}個です。".format(n_test)
            print "学習回数は{0}回です。".format(epochs)
            print "1回の学習につき、ミニバッチ1個（サンプリングデータ{0}個）で学習します。".format(mini_batch_size)
            batch_num = 0

        if test_data: n_test = len(test_data)
        n = len(training_data)
        for j in xrange(epochs):
            if self.dbg == "Debug":
                print "◆◆◆◆◆◆◆◆　{0}回目の学習を開始します。　◆◆◆◆◆◆◆◆".format(j+1)
            random.shuffle(training_data)
            if self.dbg == "Debug":
                print "トレーニングデータをシャッフルしました。"
            if self.dbg == "BackProp":
                batch_num = 0
            # ミニバッチ
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in xrange(0, n, mini_batch_size)]
            if self.dbg == "Debug":
                print "トレーニングデータを{0}から{1}の{2}個サンプルしました。"\
                    .format(k,k+mini_batch_size,mini_batch_size)
                print "{0}個の手書き文字による学習を{1}回繰り返し、重みとバイアスを更新ます--{2}回目/{3}". \
                    format(mini_batch_size, n / mini_batch_size,j ,epochs )
                # 10(mini_batch_size)個の手書き文字による学習を5000(len(training_data) / mini_batch_size)
                # 回繰り返し、重みとバイアスを更新ます--j回目/30(epochs)
                print "{0}個の手書き文字の逆伝播の結果を学習率{1}で重みとバイアスに反映させ更新します。".format(mini_batch_size, eta)

                print "これを{0}回行うのが1回の学習(Epoch)です。".format(n / mini_batch_size)

                #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            batch_time = 0
            for mini_batch in mini_batches:
                batch_time = batch_time + 1
                print "batch_time = {0} / {1}".format(batch_time, len(mini_batches))
                # (n / mini_batch_size) ×　= 5000回　重みとバイアスを更新するのが1回の学習　を30(epochs)回行う。
                # Go to "update_mini_batch" func ====>>>>
                if self.dbg == "Debug":
                    batch_num = batch_num + 1
                    if batch_num % 100 == 0:
                        print "{0}個中　{1}個目のミニバッチを読み込みます。".format(n / mini_batch_size, batch_num)
                        #TODO 処理時間の表示
                        # https://yakst.com/ja/posts/42
                        #var = raw_input()
                if self.dbg == "BackProp":
                    batch_num = batch_num + 1
                    if batch_num == 5000:
                        print "Epoch {0}: {1}個中　{2}個目のミニバッチを処置します。".format(j, n / mini_batch_size, batch_num)
                # mini_batch（１０文字分のデータ集積）でネットワークモデルを更新
                with tm.Timer() as t:
                    self.update_mini_batch(mini_batch, eta) # 学習率eta でself.weight, self.baias を更新する
                if self.batchs_num % 100 == 0:
                    my_log = "activations insertion to MySQL with one batch(batch_num={0}) is {1} s".format(self.batchs_num,t.secs)
                    my_debug.write_log("one_batch_time.txt", my_log)
                    my_log = "(" + dt.my_date_time() + ")\n"
                    my_debug.write_log("one_batch_time.txt", my_log)
            # mini_batch（１０文字分のデータ集積）でネットワークモデルを更新　を　5000回　行って、学習評価
            if self.dbg == "Write":
                self.Epochs_num = self.Epochs_num + 1
                if self.batchs_num == 100:
                    sys.exit()
                    var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            if test_data:
                print "Epoch {0}: {1} / {2}".format(
                    j, self.evaluate(test_data), n_test) # 順伝播で評価する
                var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            else:
                print "Epoch {0} complete".format(j)



    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The ``mini_batch`` is a list of tuples ``(x, y)``, and ``eta``
        is the learning rate.
        Weightsとbaiasesを(誤差が減少する更新する方向に）更新する。
        mini_batchは、mini_batches[0...9]からfor in でとり出された個々の
        データ。
        """

        if self.dbg == "Debug" or self.dbg == "BackProp":
            print "in >>>> update_mini_batch(self, mini_batch, eta):"
            print "===ミニバッチに対して誤差逆伝播法(backpropagation)を用いて、勾配下降(gradient descent)を適用します"
            self.mini_batch_num = self.mini_batch_num+1
            print "self.mini_batch_num = {0}個目のミニバッチ開始".format(self.mini_batch_num)
            per_ten = 1 # / 10

        # ニューラルネットの構造と同じひな形を作成
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # print "____DUMMY____"
        for x, y in mini_batch:
            if self.dbg == "VBouse":
                for b in xrange(0,784,1):
                    if x[b]>0.01:
                        pt="#"
                    else:
                        pt="-"
                    print pt,
                    #num=num+1
                    num=b+1
                    c=num%28
                    if c == 0 :
                        print "num={0}".format(num) #改行のため
                        if num/28==28:
                            per_ten=per_ten+1
                            print "********** データ{0}／10 **********".format(per_ten)
            elif self.dbg == "Debug" or self.dbg == "BackProp":
                print "********** データ{0}／10 **********".format(per_ten)
                per_ten = per_ten + 1
            """elif self.dbg == "Write":
                self.char_num = self.char_num + 1
                acts = []
                acts.append(self.batchs_num * 1000 + self.char_num)
                connection = ms.Mconnect(self.db)
                cursor = connection.cursor()
                tbl_name = "act_L1"
                for act in xrange(0, self.sizes[0]):
                    acts.append(x[act][0])
                ms.insert_f64CHAR16(tbl_name,cursor,acts)
                connection.commit()
                cursor.close()
                connection.close()

                #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■"""

            # Go to "backprop" func ====>>>>

            delta_nabla_b, delta_nabla_w = self.backprop(x, y) # backprop(x, y)

            # delta_nabla_b = [　array([　[  1.55325932e-03], ・・・30個　]),
            # 　　　　　　        array([　[ 0.00032173],・・・10個　])　]
            # delta_nabla_w = [  array([ [ 784要素横ベクトル],・・・30個　]),
            #                    array([[ 30要素横ベクトル],...10個　])　]
            # 1文字分の逆伝播をネットワークモデルに集積累計
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
            #if self.dbg == "Debug":
            #print "nabla_b = {0}".format(nabla_b)
            #var = raw_input()
            #print "nabla_w = {0}".format(nabla_w)
            if self.dbg == "Debug" or self.dbg == "BackProp":
                print "{0}個目の文字データを処理しました".format(per_ten-1)
            # var = raw_input()
        # １０文字分のデータ集積でネットワークモデルを更新
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]
        """ weights, baiases 更新値の格納 """
        if self.dbg == "Write":
            self.batchs_num = self.batchs_num + 1
            self.char_num = 0
            for l in xrange(2,self.num_layers+1):
                tbl_name="b_L" + str(l)
                bs = []
                bs.append(self.Epochs_num)
                bs.append(self.batchs_num)
                bs.append(self.char_num)
                """self.biasesの更新値"""
                for bj in xrange(0,len(self.biases[l-2])):
                    bs.append((self.biases[l-2][bj][0])) #****************************************
                ms.insert_f64CHAR16(tbl_name,self.cursor,bs)
                """self.weightsの更新値"""
                for j in xrange(1,self.sizes[l-1]+1):
                    tbl_name="w_L" + str(l) + "_j" + "{0:04d}".format(j)
                    wt = []
                    wt.append(self.Epochs_num)
                    wt.append(self.batchs_num)
                    wt.append(self.char_num)
                    for wj in xrange(0, len(self.weights[l-2][j-1])):
                        #print self.weights[l-2][j-1][wj]
                        #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                        wt.append(self.weights[l-2][j-1][wj])
                    ms.insert_f64CHAR16(tbl_name,self.cursor,wt)
                    #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            self.connection.commit()
            #print "batch: {0}".format(self.batchs_num)
            #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
#            cursor.close()
#            connection.close()
            # print "self.biases = {0}".format(self.biases)
            # print "Mini-batch {0}の{1}文字の処理完了".format(self.batchs_num, len(mini_batch))
            #if self.batchs_num == 5: # DEBUG**********************************************************
                #sys.exit()
            #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``.
        to ``self.biases`` and ``self.weights``.
        重みとバイアスの修正量を返す。
        x:（28×28＝）要素数784のリスト[0...783]
        y:正解のクラス分けリスト[0...9]
        x 画像データ（28*28画素をシリアライズしたリストデータ）
        y ラベル（10クラス分類（10要素のリスト）で与えられた値＝（0 or 1）
        のリスト。
        """
        #dd.draw_one_char(x)
        if self.dbg == "Debug" or self.dbg == "BackProp":
            print "in >>>> backprop(self, x, y):"
            print "単一の画像に対して誤差逆伝播法を適用する"

            for b in xrange(0,784,1):
                if x[b]>0.01:
                    pt="#"
                else:
                    pt="-"
                print pt,
                #改行のため
                num=b+1
                c=num%28
                if c == 0 :
                    print "num={0}".format(num) #改行のため
            # var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            n = 0
            # in_signal = [] # sigmoidで評価されるsignal
        # ニューラルネットの構造と同じひな形を作成
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        """ feedforward """
        activation = x #x 画像データ（28*28画素をシリアライズしたリストデータ）
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        # sizes = [784, 30, 10] ならself.biasesは30列1行 self.weightsは784列30行
        for b, w in zip(self.biases, self.weights):
            # z = 重みw[array[[...]・画像[0...373]＋b
            # 結果、zは、 layer by layerなのでニューラルネットの構造(sizes）が
            # [784,30,10]なら、30列1行　と　10列1行　が生成される。
            # 重みwは、self.sizes = [784, 30, 10] なら784列30行の行列
            # activationは入力層の入力値で初期化されている。
            z = np.dot(w, activation)+b # layer by layer な出力。
            if self.dbg == "Debug":
                #for n in xrange(1,2,1):
                # n=n+1
                print "======== 第{0}層→第{1}層 ========".format(n+1,n+2)
                #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                # 描画ライブラリはあとまわし
                in_signal = [] # sigmoidで評価されるsignal
                for j in xrange(0, self.sizes[n+1]):
                    #print "第{0}層({1}ニューロン)→第{2}層.第{3}ニューロン".format(n,j,len(w[j]),n+1)
                    print "{0}層({1}node) → {2}層({3}/{4})nodeへの出力".format(n+1,len(w[j]),n+2,j+1,len(w))
                    sum_wa=0
                    for i in xrange(0, self.sizes[n]):
                        #    .format(n,i+1,len(w[j]),n+1,j,len(w),w[j][i],activation[i][0],b[j][0], \
                        #            w[j][i]*activation[i][0]+b[j][0])
                        # activationはデバッグでは(30,0)のタプルで要素数30のタプルだが、activation[j]ではなくactivation[j][0]
                        # で値を参照する。
                        # {0}=n層, {1}=i+1番目の要素, {2}＝合計要素数, {3}＝, {4}＝, {5}＝
                        a_len=len(w[j]) #  {2}＝前層の合計要素数
                        a_w=w[j][i] # {3}＝j番目のノードへの重み係数
                        # print "i = {0}, j = {1}".format(i, j)
                        # act = activation[i][j] # ◆◆◆◆{4}＝ｊ番目のノードへの出力（入力層の場合は前処理された入力データ値）
                        # act = activation[i][0] # ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆
                        act = activations[n][i] # ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆ ◆◆◆◆
                        inner_product = w[j][i] * act[0] # {5}＝　重み　×　ｊ番目のノードへの出力
                        sum_wa += inner_product # 内積計算
                        print "{0}層{1}/{2}から:w×a = {3:.2f} * {4:.2}  = {5:.2f}" \
                            .format(n+1, i+1, a_len, a_w, act[0], inner_product)
                    #if i==len(w[j])-1:
                    print "--------------------------------------------------------------"
                    print "(自計算) {0}層({1}node) → {2}層({3}/{4})nodeへの内積w・a = {5}" \
                        .format(n+1, len(w[j]), n+2, j+1, len(w), sum_wa)
                    print "baias                                         = {0}".format(b[j][0])
                    in_signal.append(sum_wa + b[j][0])
                    print "(自計算) 出力 = {0}".format(in_signal[j]) # 層（レイヤー）が移動するとき再初期化が必要
                    print "（正解） {0}層({1}/{2})nodeへの入力 = {3}".format(n+2,j,len(z),z[j][0])
                    print "--------------------------------------------------------------"

            zs.append(z)
            # activationは、sigmoid関数によって評価された30列１行　
            #
            activation = sigmoid(z)
            if self.dbg == "Debug":
                nodes = len(z)
                for j in xrange(0,nodes,1):
                    print "<<<{0}層第 {1} nodeのsigmoid評価>>>".format(n+2, j+1)
                    print "（自計算入力シグナル） = {0}".format(in_signal[j])
                    print "（正解）  sigmoid(z=[{0}])=               {1}".format(z[j][0],activation[j][0]) # 1.0/(1.0+np.exp(-z))
                    print "（自検算）： 1.0 / ( 1.0 + exp( -{0} ) ) = {1}".format(in_signal[j],1.0/(1.0+np.exp(-in_signal[j])))
                    print "--"
                n = n+1
            activations.append(activation)

        if self.dbg == "Write":
            with tm.Timer() as t:
                # activationsの格納
                self.char_num = self.char_num + 1

                #connection = ms.Mconnect(self.db)
                self.cursor = self.connection.cursor()
                for l in xrange(1, self.num_layers+1):
                    #print str(l)
                    tbl_name = "act_L" + str(l)
                    acts = []
                    acts.append(self.Epochs_num)
                    acts.append(self.batchs_num)
                    acts.append(self.char_num)
                    for act in xrange(0, self.sizes[l-1]):
                        #print str(act)
                        acts.append(activations[l-1][act][0])
                    ms.insert_f64CHAR16(tbl_name,self.cursor,acts)
                #self.connection.commit()
                #print "activations saved"
                tbl_name = "Label"
                n = []
                n.append(self.Epochs_num)
                n.append(self.batchs_num)
                n.append(self.char_num)
                for label in xrange(0, self.sizes[-1]):
                    n.append(y[label][0])
                ms.insert_f64CHAR16(tbl_name,self.cursor,n)
                self.connection.commit()
            #my_log = "activations at one charctor is {0} s".format(t.secs)
            #my_debug.write_log("one_char_time.txt",my_log)
            #my_log = "(" + dt.my_date_time() + ")\n"
            #my_debug.write_log("one_char_time.txt",my_log)

            #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

        """ backward pass 逆伝播 """
        #if self.dbg == "Debug":
        #    var = raw_input()
        # delta = [出力層クラス分け1列0行] - [正解] *  (sigmoid(z)*(1-sigmoid(z)))
        # delta = -誤差 * シグモイド関数の導関数　のように見えるが、
        # delta = 出力層における、{ 個々のニューロンの出力した活性値(activation)近傍の2乗差コスト関数の導関数(勾配)
        #       * 重み付き入力値(z)近傍のシグモイド関数の導関数（勾配）}　＝　出力層の個々のニューロンでの誤差
        # Nielsen 式（BP1) Back propagation 1
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1]) # 出力層の個々のニューロンでの誤差.zsはsigmoid評価前の重み付き出力.

        # sigmoid_prime(z) = sigmoid(z)*(1-sigmoid(z))
        # 出力層
        nabla_b[-1] = delta # 式（BP1)　baias-voctor の偏微分値
        # 前層の重み付き入力(activation)を転置して内積(dot)の形を取るが、1列N行と1列N行の内積なので、結果的にアマダール積になる。
        nabla_w[-1] = np.dot(delta, activations[-2].transpose()) # 重み付き入力wの
        #
        if self.dbg == "BackProp":
            print "L=L（出力)層 正解は{0}".format(np.transpose(y))
            print "actibation（シグモイド評価出力）の誤差 = (出力値ー正解値)× sigmoid評価前の重み付き出力（出力と正解は0〜１で正規化済）"
            for c in xrange(0, len(delta),1):
            #for c in xrange(0, 10,1):
                print "{0} = ( {1} - {2} ) × ({3} - {4})". \
                    format(delta[c], activations[-1][c] , y[c], sigmoid(zs[-1][c]),1-sigmoid(zs[-1][c]))
                #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            print "baias-voctor の偏微分値 = (出力値ー正解値)× sigmoid評価前の重み付き出力(deltaと同じ)"
            print "{0}".format(nabla_b[-1])
            #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            print "重み付き入力wの偏微分値= sum[c=0..9](delta[c] * activations[-2][c] )"
            print "                      誤差 × 出力ノードに入ってきた前層各ノードの評価出力"
            print "----出力層の重みwベクトルの偏微分----"
            print "{0}".format(nabla_w[-1])
            for c in xrange(0, len(delta),1):
                naiseki = 0
                print "--------------------------------------------------------------------"

                print "出力層　第　{0}　ノード".format(c+1)
                print "重み付き入力wの偏微分値= sum[c=0..9](delta[c] * activations[-2][c] )"
                print "nabla_w        =?  (自分計算)         =  誤差 × 出力ノードに入ってきた前層各ノードの評価出力"
                #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

                for d in xrange(0, len(nabla_w[-1]),1):
                    print "{0} =? {1} = {2}* {3}".format(nabla_w[-1][c][d], delta[c]*activations[-2][d],delta[c],activations[-2][d])
                    naiseki = naiseki + delta[c]*activations[-2][d]

        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        # 中間層〜入力層
        # L＝-1を出力層とした時の-l番目の層の「重みつき入力についての誤差」
        if self.dbg == "BackProp":
            print "====中間層〜入力層===="
        for l in xrange(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            if self.dbg == "BackProp":
                naiseki = np.dot(self.weights[-l+1].transpose(), delta)
                naiseki_d=[]
                g = 0
                #print "１つ出力側の層の「重みの転置行列（30行10列）」 self.weights[-l+1].transpose() = " # 30列10行
                #print "{0}".format(self.weights[-l+1].transpose())
                #print "１つ出力側の層のdelta(誤差)"
                #print "L＝-1を出力層とした時の-l番目の層のdelta = " # 1行30列
                #print "{0}".format(delta)
                #print "この層の「重み付き出力」のsigmoid関数偏微分sp"
                #print "{0}".format(sp)
                print "内積（正解）＝{0}".format(naiseki) # 1行30列 [0, n]で参照
                #var = raw_input() #　■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
                # １つ出力側の層の「重みの転置行列（30行10列）」と「活性関数sigmoidの導関数（1行30列）」から入力側の層の
                # 「重みつき入力についての誤差」を計算する
                # save_delta = １つ出力側の層[-l+1]の「重みつき入力についての誤差」deltaを値コピーしておく
                save_delta = np.array(delta) # あとで内積を検算するときに使う。
            # [-l]番目の層の 「バイアスについての誤差」
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            # [-l]番目の層の 「重みつき入力についての誤差」
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
            if self.dbg == "BackProp":
                #print "delta = " # 1行30列
                #print "{0}".format(delta)
                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                for c in xrange(0, self.sizes[-l], 1):
                    """
                    転置
                    import numpy
                    a = numpy.matrix([[1,2],[3,4]])
                    # [[1, 2],
                    #  [3, 4]]
                    a.T
                    # [[1, 3],
                    #  [2, 4]]
                    ndarrayの生成
                    >>> c = np.zeros( (2,1) )
                    array([[ 0. ],
                           [ 0. ]])
                    ◆◆◆◆　ndarrayの参照　◆◆◆◆
                    In [62]: a = np.array([[11, 12, 13], [21, 22, 23]])
                    In [63]: a.shape
                    Out[63]: (2, 3)
                    In [64]: a[1,2]　・・・　[列, 行]　の順で添字をカンマ区切りする。
                    Out[64]: 23
                    ◆◆◆◆　内積　◆◆◆◆
                    >>> a=np.array([[1,2,3],[4,5,6]])
                    >>> a
                    array([[1, 2, 3],
                           [4, 5, 6]])
                    >>> b=np.array([[1,3,5,7],[2,4,6,8],[4,5,6,7]])
                    >>> b
                    array([[1, 3, 5, 7],
                           [2, 4, 6, 8],
                           [4, 5, 6, 7]])
                    >>> np.dot(a,b)
                    array([[ 17,  26,  35,  44],
                           [ 38,  62,  86, 110]])
                    """
                    sum_d = 0
                    for d in  xrange(0, self.sizes[-l+1], 1):
                        sum_d = sum_d + self.weights[-l+1].transpose()[c][d]*save_delta[d]
                        if d == self.sizes[-l+1]-1:
                            naiseki_d.append(sum_d)
                            print "（内積 {3}層 {0}node）{1}　＝?　合計(自計算){2}".format(c+1, naiseki[c,0], sum_d, self.num_layers-l+1)
                            # nabla_b[-l] = delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
                            print "nabla_b[-{0}][{1}] {2}  =?  (自計算){3} = {4} * {5}". \
                                format(l, c, nabla_b[-l][g,0], naiseki_d[g]*sp[g,0],naiseki_d[g], sp[g,0])
                            # nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
                            print "nabla_w[-l]は30列784行 = np.dot(delta, activations[-l-1].transpose())"
                            g = g +1
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations.
        個々のニューロンにおける2乗差コスト関数の導関数"""
        return (output_activations-y)

#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function.
    シグモイド関数"""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function.
    シグモイド関数の導関数（勾配）"""
    return sigmoid(z)*(1-sigmoid(z))

def all_done(self):
    self.cursor.close()
    self.connection.close()
    print "DB connection is closed."