import csv
from scipy.spatial import distance
from collections import Counter

def read_file(filename):
  infile = open(filename, 'r')
  reader = csv.reader(infile)
  lista = list(reader)
  return [[float(y) for y in x[:-1]]+[x[-1]] for x in lista[1:]]

def sonCompatibles(i1, i2):
  if len(i1) == len(i2)  : return True
  if len(i1) == len(i2)-1: return True
  return False

def distancia(i1, i2):
  if len(i1) == len(i2):
    return distance.euclidean(i1[:-1], i2[:-1])
  if len(i1) == len(i2)-1:
    return distance.euclidean(i1[:], i2[:-1])
  if len(i1)-1 == len(i2):
    return distance.euclidean(i1[:-1], i2[:])
  print 'Epic Fail.'
 
def knn(k, i, c):
  if not sonCompatibles(i, c[0]):
    return 'Tipos incopatibles.'

  # Guardamos tuplas de (clase, distancia) entre 'i' y c[0...n].
  # Luego lo ordenamos por la distancia y cogemos los k primeros.
  dist_min = sorted([(c[y][-1], distancia(i,c[y])) for y in range(0,len(c)-1)], key=lambda tup: tup[1])[:k]
  clases = Counter([x[0] for x in dist_min])
  return max(clases, key=clases.get)

def test(k, trainset, testset):
  aux = []
  for test in testset:
    clase = knn(k, test, trainset)
    if test[-1] == clase: aux +=[True]
    else: aux +=[False]
  return aux.count(True)/float(len(aux))

def pruebas():
  train_set = read_file('iris.csv')
  test_set = read_file('iris_test.csv')
  aux = test (5, train_set, test_set )
  print aux

pruebas()
