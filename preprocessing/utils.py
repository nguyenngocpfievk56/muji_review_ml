def loadDict():
  f = open('dictionary.txt', 'r')
  dictionary = []
  for line in f:
      dictionary.append(line.strip('\n'))

  f.close()
  return dictionary