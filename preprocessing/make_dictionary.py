# -*- coding: utf-8 -*-
import json
from mysql.connector import (connection)
import MeCab
import operator

mecab = MeCab.Tagger("-Ochasen")

with open('./preprocessing/config.json') as config_file:
    data = json.load(config_file)

cnx = connection.MySQLConnection(user=data['mysql']['user'], password=data['mysql']['passwd'],
                                 host=data['mysql']['host'],
                                 database=data['mysql']['db'])
cursor = cnx.cursor()

query = ("SELECT entry_id, description FROM cs_entry_comment WHERE entry_id IS NOT NULL AND status IN (1,2)")

cursor.execute(query)

words = {}
total = 0

for (entry_id, description) in cursor:
  print(entry_id)
  total += 1
  node = mecab.parseToNode(description.encode('utf-8'))

  while node:
    word = node.surface
    features = node.feature.split(",")
    wtype = features[0]
    if (len(features) > 6) and features[6]:
      word = features[6]
    if (wtype == "名詞" or wtype == "動詞" or wtype == "形容詞"):
      if (word in words):
        words[word] += 1
      else:
        words[word] = 1
    node = node.next

cursor.close()
cnx.close()

print 'Total Review : ', total

words = sorted(words.items(), key=operator.itemgetter(1))
word_frequence = open('./preprocessing/word_frequence.txt', 'w')
dictionary = open('./neural_network/dictionary.txt', 'w')
for word in words:
  word_frequence.write("%s %d\n" % (word[0], word[1]))
  if word[1] > 2:
    dictionary.write("%s\n" % word[0])
word_frequence.close()
dictionary.close()