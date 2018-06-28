# -*- coding: utf-8 -*-
import json
from mysql.connector import (connection)
import MeCab
import operator
from utils import loadDict

mecab = MeCab.Tagger("-Ochasen")

with open('./preprocessing/config.json') as config_file:
    data = json.load(config_file)

cnx = connection.MySQLConnection(user=data['mysql']['user'], password=data['mysql']['passwd'],
                                 host=data['mysql']['host'],
                                 database=data['mysql']['db'])
cursor = cnx.cursor()

query = ("SELECT id, description FROM cs_entry_comment WHERE entry_id IS NOT NULL AND status IN (1,2)")

cursor.execute(query)

dictionary = loadDict()
f = open('preprocessing/normalize_view_buy.txt', 'r')
review_views = {}
for line in f:
  tmp = line.split(",")
  review_views[tmp[0]] = tmp[1]

convertedData = open('converted_data.txt', 'w')

for (id, description) in cursor:
  print(id)
  if (str(id) in review_views):
    doc = {}
    for w in dictionary:
      doc[w] = 0

    node = mecab.parseToNode(description.encode('utf-8'))
    while node:
      word = node.surface
      features = node.feature.split(",")
      if (len(features) > 6) and not features[6]:
        word = features[6]
      if (word in doc):
        doc[word] += 1
        
      node = node.next

    views = int(review_views[str(id)])
    convertedData.write("%d,%d" % (id, views))
    for w, freq in doc.items():
      convertedData.write(",%d" % freq)

    convertedData.write("\n")

convertedData.close()
cursor.close()
cnx.close()