import numpy as np
from chainer.datasets import tuple_dataset

def loadData(total):
  train = []
  test = []
  f = open('converted_data.txt', 'r')
  index = 0

  text_data = []
  label_data = []
  for line in f:
    if index < total:
      tmp = line.split(",")
      text = np.array([np.float32(x) for x in tmp[2:]])
      label = np.int32(tmp[1])
      text_data.append(text)
      label_data.append(label)
      
    index += 1
  f.close()

  threshold = np.int32(total * 0.9)
  train = tuple_dataset.TupleDataset(text_data[0:threshold], label_data[0:threshold])
  test  = tuple_dataset.TupleDataset(text_data[threshold:],  label_data[threshold:])

  return train, test

def loadDict():
  f = open('./neural_network/dictionary.txt', 'r')
  dictionary = []
  for line in f:
      dictionary.append(line.strip('\n'))

  f.close()
  return dictionary
