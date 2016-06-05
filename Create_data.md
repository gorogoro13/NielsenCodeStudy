＜概要＞
　Githubのリポジトリ（https://github.com/gorogoro13/NielsenCodeStudy.git）を作成した際に、
　２．以降はScript/以下にまとめた。
　１．はsrc/のメインの実行ファイル（nielsen27_chap_01）を使用する。

１．　network.pyの実行プロセス（逆伝播）のパラメータの変化を記録する
$>>> import mnist_loader
$>>> training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
$>>> import network
$>>> net = network.Network([784, 30, 10],3, incriment = True, hex = True)
$>>> net.SGD(training_data, 1, 10, 3.0, test_data=test_data)
#TODO net = network.Network([784, 30, 10],3, incriment = True, hex = True)
#TODO parameter d[d, dbname1] incriment[ incriment, dbname2]
#TODO  ネットワーク初期化パラメータのデバッグオプションで、データーベース名を指定できるようにする

２．　グラフを保存する
$ python 28by28weight.py （現在L2のみ固定のスクリプト）
・データベース名    db = "epoch_01_a"
・保存ディレクトリ    p_dir = "g_pict/"　#TODO 振り分けディレクトリ
・保存フォーマット    file_name = title + ".eps"
・クエリー          sql = "select w_" + "{0:04d}".format(col -2) + " from " + tbl_name + ";"
"""TODO       L2      L3
weights       ◯
baiases
activations
"""

３．　画像をpngフォーマットに変換する
$ bash eps2png.sh "source directory" #　"source directory"内の.epsを.pngに変換して出力する
$ bash eps2png_save.sh "dir_prefix" # "dir_prefix"で指定した名前に通し番号をつけたディレクトリ内の.epsを.pngに変換して出力する

４．　htmlを生成する
$ python gen_ghtml.py > index.html #L2j0001-00030のリンク付き


$ bash gen_html.sh "output file name" "source directory" #L2指定ノード単体のhtml




