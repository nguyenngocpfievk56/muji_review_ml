# -*- coding: utf-8 -*-
import json
from mysql.connector import (connection)
import operator

with open('./preprocessing/config.json') as config_file:
    data = json.load(config_file)

cnx = connection.MySQLConnection(user=data['mysql']['user'], password=data['mysql']['passwd'],
                                 host=data['mysql']['host'],
                                 database=data['mysql']['db'])

cnx1 = connection.MySQLConnection(user=data['mysql']['user'], password=data['mysql']['passwd'],
                                 host=data['mysql']['host'],
                                 database=data['mysql']['db'])

cursor = cnx.cursor()
c1 = cnx1.cursor()

query = ("SELECT count(id) as count, entry_id FROM cs_entry_comment WHERE entry_id IS NOT NULL GROUP BY entry_id")

cursor.execute(query)

f = open('preprocessing/muji_review_view.csv', 'r')
review_views = {}
for line in f:
  tmp = line.split(",")
  review_views[tmp[0]] = tmp[1]

convertedData = open('preprocessing/normalize_views.txt', 'w')

for (count, entry_id) in cursor:
  q1 = ("SELECT id, entry_id FROM cs_entry_comment WHERE entry_id = %d" % entry_id)
  c1.execute(q1)
  tmp = {}
  for (id, entry_id) in c1:
    if str(id) in review_views:
      tmp[str(id)] = review_views[str(id)]
    else:
      tmp[str(id)] = 0
  # sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)
  sorted(tmp.items(), key=operator.itemgetter(1))
  point = 0
  for k, v in tmp.items():
    convertedData.write("%s,%d\n" % (k, point))
    if point < 9:
      point += 1

convertedData.close()
cursor.close()
cnx.close()