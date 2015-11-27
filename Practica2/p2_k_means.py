import csv
from scipy.spatial import distance
#from collections import Counter
import numpy as np


def read_file(filename):
  infile = open(filename, 'r')
  reader = csv.reader(infile)
  lista = list(reader)
  return [[int(y) for y in x] for x in lista[1:]]

def kmeans(k, instancias, centroides_ini = None):
  if centroides_ini == None:
    centroides_ini = getCentroids(k,instancias)
  oldListCluster = [[] for x in range(0,k)]
  while True:
    newListCluster = getCluster(centroides_ini,instancias)
    if newListCluster == oldListCluster:
      break
    oldListCluster = newListCluster
    centroides_ini = recalcular_centroides(newListCluster)
  return (newListCluster , centroides_ini)

def getCluster(centroids, instancias):
  listCluster = [[] for x in range(0,len(centroids))]
  for ins in instancias:
    index = getMinMaxToTarget(ins,centroids)
    listCluster[index].append(ins)
  return listCluster

def recalcular_centroides(newListCluster):
  listaAux = []
  for lista in newListCluster:
    lista = np.array(lista)
    aux2 = np.mean(lista, axis=0).tolist()
    listaAux.append(aux2)
  return listaAux

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

def getMinMaxToTarget(target, theList, theFunc = min):
  listDistances = []
  for elem in theList:
    listDistances.append(distance.euclidean(target,elem))
  return listDistances.index(theFunc(listDistances))

def getMinMaxDistFromList(listaCluster, theFunc = max):
  distMin = -1
  for x in range(0,len(listaCluster)):
    for y in range(x,len(listaCluster)):
      if distance.euclidean(listaCluster[x],listaCluster[y]) > distMin:
        distMin = distance.euclidean(listaCluster[x],listaCluster[y])
  return distMin

def prueba():
  aux = read_file('customers.csv')
  (clusters, centroids) = kmeans(4,aux)
  for clus, cent in zip(clusters, centroids):
    print "cent: ",cent 
    print "clus: ",clus
 
  print "------------------------------------------------------------------------"
  listRadios = []
  listDiametros = []
  for clus, cent in zip(clusters, centroids):
    listRadios.append(distance.euclidean(cent,clus[getMinMaxToTarget(cent,clus,max)]))
    listDiametros.append(getMinMaxDistFromList(clus))


  print listRadios
  #print [2.0*x for x in listRadios]
  print "------------------------------------------------------------------------"
  print listDiametros

prueba()
