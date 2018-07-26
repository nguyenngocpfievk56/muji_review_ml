# -*- coding: utf-8 -*-
import json
import numpy as np
import operator

f = open('preprocessing/muji_review_like.csv', 'r')
convertedData = open('preprocessing/normalize_like.txt', 'w')

normalized_reviews = {}
for line in f:
  tmp = line.split(",")
  likes = np.float32(tmp[1])
  if likes > 9:
    normalized_reviews[tmp[0]] = 10.0
  else:
    normalized_reviews[tmp[0]] = np.float32(tmp[1])

for k,v in normalized_reviews.items():
  convertedData.write("%s,%d\n" % (k, v))

f.close()
convertedData.close()