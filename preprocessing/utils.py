def loadDict():
  f = open('neural_network/dictionary.txt', 'r')
  dictionary = []
  for line in f:
      dictionary.append(line.strip('\n'))

  f.close()
  return dictionary