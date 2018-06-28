# -*- coding: utf-8 -*-
import json
from mysql.connector import (connection)
from predict import predict

with open('./preprocessing/config.json') as config_file:
    data = json.load(config_file)

cnx = connection.MySQLConnection(user=data['mysql']['user'], password=data['mysql']['passwd'],
                                 host=data['mysql']['host'],
                                 database=data['mysql']['db'])
cursor = cnx.cursor()

def addNewReview(content, productId):
  score = predict(content)
  query = ('INSERT INTO cs_entry_comment(entry_id, description, score) VALUES(%d, "%s", %d)' % (productId, content, score))
  try:
    cursor.execute(query)
    cnx.commit()
    print("SUCCESS")
  except:
    print("FAILED")

def showReviewsOf(productId):
  query = ('SELECT id, description, score FROM cs_entry_comment WHERE entry_id = %d ORDER BY score DESC' % productId)
  cursor.execute(query)
  for (id, description, score) in cursor:
    print('-' * 150)
    print('Review ID: %s --- Score: %s' % (id, score))
    print(description)
    print('-' * 150)
  return 0

if __name__ == '__main__':
  entry_id = 54066
  content = 'ずっと気になっており、先日の無印週間の際に購入しました。時間になると鳩出てきて鳴っていると子供達が大喜びします。私自身も幼少期の頃を思い出します。'
  # addNewReview(content, entry_id)
  showReviewsOf(entry_id)