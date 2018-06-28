# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
from chainer import datasets, iterators, optimizers, serializers
from muji_model import MujiNN
from utils import loadData, loadDict
import MeCab

model = MujiNN()

serializers.load_npz('./neural_network/my_mnist.model', model)


def predict(review):
  mecab = MeCab.Tagger("-Ochasen")
  # node = mecab.parseToNode(review.encode('utf-8'))
  node = mecab.parseToNode(review)
  dictionary = loadDict()
  doc = {}
  for w in dictionary:
    doc[w] = 0

  while node:
    word = node.surface
    features = node.feature.split(",")
    if (len(features) > 6) and not features[6]:
      word = features[6]
    if (word in dictionary):
      doc[word] += 1
    node = node.next

  tmp = []
  for k,v in doc.items():
    tmp.append(np.float32(v))
  
  converted_doc = np.array([np.float32(x) for x in tmp])
  converted_doc = converted_doc[None, ...]
  y = model(converted_doc)
  y = y.data
  pred_label = y.argmax(axis=1)
  return int(pred_label) + 1

if __name__ == '__main__':
  content = 'ずっと気になっており、先日の無印週間の際に購入しました。時間になると鳩出てきて鳴っていると子供達が大喜びします。私自身も幼少期の頃を思い出します。'
  print(predict(content))
