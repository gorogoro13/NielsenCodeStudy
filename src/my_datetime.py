# -*- coding: utf-8 -*-
"""
my_datetime.py
~~~~~~~~~~
http://www.yukun.info/blog/2008/06/python-date.html
"""
"""
***ソースコード***
#!/usr/bin/python
# coding: UTF-8

# 現在の日付・時刻の取得と出力 | datetimeクラスの属性、today()、strftime()メソッドの使い方
import datetime # datetimeモジュールのインポート
import locale   # import文はどこに書いてもOK(可読性などの為、慣例でコードの始めの方)

# today()メソッドで現在日付・時刻のdatetime型データの変数を取得
d = datetime.datetime.today()
#   ↑モジュール名.クラス名.メソッド名
print 'd == %s : %s\n' % (d, type(d)) # Microsecond(10^-6sec)まで取得
# datetime型の各属性へのアクセス
# year, month, day
print '%s年%s月%s日\n' % (d.year, d.month, d.day)
# hour, minute, second, microsecond
print '%s時%s分%s.%s秒n' % (d.hour, d.minute, d.second, d.microsecond)
# strftime()メソッドで日付時刻の書式を指定して出力
print d.strftime("%Y-%m-%d %H:%M:%S"), '\n'
# 地域の設定
locale.setlocale(locale.LC_ALL, 'ja') # 属性の出力に影響(曜日とか)
print locale.getlocale(), '\n'
print d.strftime("%B%d日%A") # locale.setlocale()でlocale指定してないと"Fri"と表示(デフォルトの設定地域)
print d.strftime("%p")       # 指定の地域でのAM/PMの対応する文字列
print d.strftime("%x %X")    #               日付と時刻に対応する文字列

***実行結果***
d == 2008-06-06 11:50:25.964000 : &#60;type &#39;datetime.datetime&#39;&#62;
2008年6月6日
11時50分25.964000秒
2008-06-06 11:50:25
(&#39;Japanese_Japan&#39;, &#39;932&#39;)
6月06日金曜日
午前
2008/06/06 11:50:25
"""
import datetime # datetimeモジュールのインポート
# import locale   # import文はどこに書いてもOK(可読性などの為、慣例でコードの始めの方)

def my_date_time():
    # today()メソッドで現在日付・時刻のdatetime型データの変数を取得
    d = datetime.datetime.today()
    #   ↑モジュール名.クラス名.メソッド名

    # datetime型の各属性へのアクセス
    # year, month, day
    t = '%s年%s月%s日' % (d.year, d.month, d.day)
    # hour, minute, second, microsecond
    t += '%s時%s分%s.%s秒' % (d.hour, d.minute, d.second, d.microsecond)
    return t

def main():
    print " "

if __name__ == '__main__':
    main()