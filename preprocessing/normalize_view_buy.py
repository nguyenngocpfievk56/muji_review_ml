# -*- coding: utf-8 -*-
import json
import numpy as np
import operator

f = open('preprocessing/review_view_buy.csv', 'r')
convertedData = open('preprocessing/normalize_view_buy.txt', 'w')

normalized_reviews = {}
for line in f:
  tmp = line.split(",")
  if (np.float32(tmp[1]) > 50):
    normalized_reviews[tmp[0]] = np.float32(tmp[2]) / np.float32(tmp[1])

sorted_normalized_reviews = sorted(normalized_reviews.items(), key=operator.itemgetter(1), reverse=True)
normalize_value = 9.0
normalize_factor = sorted_normalized_reviews[0][1]
normalize_ratio = normalize_value / normalize_factor

for k,v in normalized_reviews.items():
  print(k)
  tmp = int(round(normalize_ratio * v))
  convertedData.write("%s,%d\n" % (k, tmp))

f.close()
convertedData.close()
