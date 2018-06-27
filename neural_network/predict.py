from __future__ import print_function
import numpy as np
from chainer import datasets, iterators, optimizers, serializers
from muji_model import MujiNN
from utils import loadData

model = MujiNN()

serializers.load_npz('my_mnist.model', model)

train, test = loadData(1000)

# Get a test image and label
for tmp in test:
  x, t = tmp

  x = x[None, ...]
  y = model(x)

  # The result is given as Variable, then we can take a look at the contents by the attribute, .data.
  y = y.data

  # Look up the most probable digit number using argmax
  pred_label = y.argmax(axis=1)

  print('label', t)
  print('predicted label:', pred_label[0])