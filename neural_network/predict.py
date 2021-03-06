# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
from chainer import datasets, iterators, optimizers, serializers
from muji_model import MujiNN
from utils import loadData, loadDict, loadIdf
import MeCab

model = MujiNN()

serializers.load_npz('./neural_network/my_mnist.model', model)


def predict(review):
  mecab = MeCab.Tagger("-Ochasen")
  # node = mecab.parseToNode(review.encode('utf-8'))
  node = mecab.parseToNode(review)
  dictionary = loadDict()
  # idfW = loadIdf()
  doc = {}
  for w in dictionary:
    doc[w] = 0

  num_words = 0
  while node:
    word = node.surface
    features = node.feature.split(",")
    if (len(features) > 6) and features[6]:
      word = features[6]

    if (word in dictionary):
      doc[word] = 1
      print()
      num_words += 1
    node = node.next

  # tmp = [num_words]
  tmp = []
  for k,v in doc.items():
    # if (num_words == 0):
    #   tf = 0
    # else:
    #   tf = float(v) / num_words
    # tmp.append(np.float32(tf * idfW[k]))
    tmp.append(v)

  converted_doc = np.array([np.float32(x) for x in tmp])
  converted_doc = converted_doc[None, ...]
  y = model(converted_doc)
  y = y.data
  pred_label = y.argmax(axis=1)
  return int(pred_label)

if __name__ == '__main__':
  content = 'この椅子はデザインを見て一発で気に入りました。座り心地もよく長時間座っていても腰が楽です。そしてお尻が蒸れません！'
  print(predict(content))
