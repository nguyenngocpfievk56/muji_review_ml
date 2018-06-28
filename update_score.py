# -*- coding: utf-8 -*-
import json
from mysql.connector import (connection)

with open('./preprocessing/config.json') as config_file:
    data = json.load(config_file)

cnx = connection.MySQLConnection(user=data['mysql']['user'], password=data['mysql']['passwd'],
                                 host=data['mysql']['host'],
                                 database=data['mysql']['db'])
cursor = cnx.cursor()

f = open('./preprocessing/normalize_view_buy.txt', 'r')
for line in f:
  tmp = line.strip('\n').split(',')
  try:
    query = ("UPDATE cs_entry_comment SET score = %d WHERE id = %s" % (int(tmp[1]) + 1, tmp[0]) )
    cursor.execute(query)
  except:
    print(tmp[0])

cnx.commit()

f.close()
cursor.close()
cnx.close()