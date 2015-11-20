import csv
import re
from scipy.spatial import distance

def read_file(filename):
  infile = open(filename, 'r')
  reader = csv.reader(infile)
  lista = list(reader)
  #return [x for x in lista[:][:], lista[:1]]

def sonCompatibles(i1, i2):
  if len(i1) == len(i2)  : return True
  if len(i1) == len(i2)-1: return True
  return False

def distancia(i1, i2):
  if len(i1) == len(i2):
    return distance.euclidean(i1[:-1], i2[:-1])
  if len(i1) == len(i2)-1:
    return distance.euclidean(i1[:], i2[:-1])
  print 'Epic Fail.'
 
def knn(k, i, c):
  if not sonCompatibles(i, c[0]):
    return 'Tipos incopatibles.'

  menores = []
  #for
  return 'Son compatibles.'


print read_file('iris_test.csv')
#print distancia( ['4.9', '3.1', '1.5', '0.1', 'Iris-setosa'],  ['4.9', '3.1', '1.5', '0.1', 'Iris-setosa'])
