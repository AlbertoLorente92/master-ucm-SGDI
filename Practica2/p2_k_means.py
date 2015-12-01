import csv
from scipy.spatial import distance
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick

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
    centroides_ini = recalcular_centroides(newListCluster,centroides_ini)
  return (newListCluster , centroides_ini)

def getCluster(centroids, instancias):
  listCluster = [[] for x in range(0,len(centroids))]
  i = 0
  for ins in instancias:
    index = getMinMaxToTarget(ins,centroids)
    listCluster[index].append(ins)
  return listCluster

def recalcular_centroides(newListCluster,centroides):
  listaAux = []
  for lista, cent in zip(newListCluster, centroides):
    lista = np.array(lista)
    if len(lista) == 0:
      listaAux.append(cent)
    else:
      aux2 = np.mean(lista, axis=0).tolist()
      listaAux.append(aux2)
  return listaAux

def getCentroids(k, instancias):
  listaCentroids = [instancias[0]]
  for i in range(0,k):
    listaDistancias = []
    for ins in instancias:
      listaDistancias.append(getDist(ins,listaCentroids))
    max_pos = listaDistancias.index(max(listaDistancias))
    listaCentroids.append(instancias[max_pos])
  return listaCentroids

def getDist(i1, lista_ins):
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
  distMin = -1.0
  for x in range(0,len(listaCluster)):
    for y in range(x+1,len(listaCluster)):
      aux = distance.euclidean(listaCluster[x],listaCluster[y])
      if aux > distMin:
        distMin = aux
  return distMin

def getAverageDistance(centroid, cluster):
  dist = 0.0
  for instance in cluster:
    dist = dist + math.pow(distance.euclidean(instance,centroid), 2)
  return dist/float(len(cluster))

def getRadio(clus, cent):
  if len(clus) <= 1: return 0.0
  return distance.euclidean(cent,clus[getMinMaxToTarget(cent,clus,max)])

def getDiametro(clus):
  if len(clus) <= 1: return 0.0
  return getMinMaxDistFromList(clus)

def getDistancia(clus, cent):
  if len(clus) <= 1: return 0.0
  return getAverageDistance(cent,clus)

def getRadios(clusters, centorids):
  listaRadios = []
  for clus, cent in zip(clusters, centorids):
    listaRadios.append(getRadio(clus, cent))
  return listaRadios

def getDiametros(clusters):
  listaDiametros = []
  for clus in clusters:
    listaDiametros.append(getDiametro(clus))
  return listaDiametros

def getDistancias(clusters, centroids):
  listaDistancias = []
  for clus, cent in zip(clusters, centroids):
    listaDistancias.append(getDistancia(clus, cent))
  return listaDistancias

def getStats(lista):
  return [ np.mean(lista)-np.std(lista), np.mean(lista)+np.std(lista), min(lista), max(lista) ]

def getMeanWeight(listaRadios, listaPesos, total):
  auxSum = 0.0
  for rad, weight in zip(listaRadios, listaPesos):
    auxSum += rad * (weight/float(total))
  return auxSum
  
def prueba():
  aux = read_file('customers.csv')
  radios         = []
  radiosNorm     = [None, None]
  diametros      = []
  diametrosNorm  = [None, None]
  distancias     = []
  distanciasNorm = [None, None]
  
  for i in range(2,21):
    (clusters, centroids) = kmeans(i,aux)
    listRadios     = getRadios(clusters, centroids)
    radios.append(     [i]+getStats(listRadios))
    radioNorm = getMeanWeight(listRadios, [len(x) for x in clusters], len(aux))
    radiosNorm.append(radioNorm)

    listDiametros  = getDiametros(clusters)
    diametros.append(  [i]+getStats(listDiametros))
    diametroNorm = getMeanWeight(listDiametros, [len(x) for x in clusters], len(aux))
    diametrosNorm.append(diametroNorm)

    listDistancias = getDistancias(clusters, centroids)    
    distancias.append( [i]+getStats(listDistancias))
    distanciaNorm = getMeanWeight(listDistancias, [len(x) for x in clusters], len(aux))
    distanciasNorm.append(distanciaNorm)
    if i == 5:
      print '===>', listDistancias.index(max(listDistancias))
      print max(listDistancias)
      print clusters[listDistancias.index(max(listDistancias))]


  fig, ax = plt.subplots()
  fig.subplots_adjust(bottom=0.2)
  candlestick(ax, radios, width=0.2, alpha=0.5)
  plt.plot(radiosNorm)
  plt.axhline(0, color='red')
  plt.savefig('Radios.png')

  fig, ax = plt.subplots()
  fig.subplots_adjust(bottom=0.2)
  candlestick(ax, diametros, width=0.2, alpha=0.5)
  plt.plot(diametrosNorm)
  plt.axhline(0, color='red')
  plt.savefig('Diametros.png')

  fig, ax = plt.subplots()
  fig.subplots_adjust(bottom=0.2)
  candlestick(ax, distancias, width=0.2, alpha=0.5)
  plt.plot(distanciasNorm)
  plt.axhline(0, color='red')
  plt.savefig('Distancia.png')

prueba()
