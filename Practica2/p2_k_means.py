import csv
from scipy.spatial import distance
#from collections import Counter

def read_file(filename):
  infile = open(filename, 'r')
  reader = csv.reader(infile)
  lista = list(reader)
  return [[int(y) for y in x] for x in lista[1:]]

def kmeans(k, instancias, centroides_ini = None):
  if centroides_ini == None:
    centroides_ini = getCentroids(k,instancias)
  
  
def closestCentroid(ins, centroides_ini):
  listaDistancias = []
  for cent in centroides_ini:
    listaDistancias.append(distance.euclidean(cent,ins))
  return listaDistancias.index(min(listaDistancias))

def getCentroids(k, instancias):
  listaCentroids = [instancias[0]]
  for i in range(1,k):
    listaDistancias = []
    for ins in instancias:
      listaDistancias.append(getDistancia(ins,listaCentroids))
    max_pos = listaDistancias.index(max(listaDistancias))
    listaCentroids.append(instancias[max_pos])
  return listaCentroids

      

def getDistancia(i1, lista_ins):
  dist = 0.0
  for ins in lista_ins:
    dist+=distance.euclidean(i1,ins)
  return dist







def prueba():
  aux = read_file('customers.csv')
  listaCentros = getCentroids(4,aux)
  print listaCentros

prueba()
