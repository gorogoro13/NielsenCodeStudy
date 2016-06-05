#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#draw_MNISTdata.py
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
from numpy import random

from tensorflow.examples.tutorials.mnist import input_data


def _to_number(label):
    for index, n in enumerate(label):
        if n != 0:
            return index


def main():
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


if __name__ == '__main__':
    main()
