import csv
from scipy.spatial import distance
import numpy as np
import math
import matplotlib.pyplot as plt

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
      #print lista, aux2
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
  distMin = -1.0
  for x in range(0,len(listaCluster)):
    for y in range(x+1,len(listaCluster)):
      aux = distance.euclidean(listaCluster[x],listaCluster[y]) ##Si solo hay 2 instancias esto da = nan
      if len(listaCluster) == 2:
        print(aux,"---->>",listaCluster[x], "---",listaCluster[y])   
        aux = distanciaAMano(listaCluster[x],listaCluster[y])  ##pero si lo calculo todo manual funciona
      if aux > distMin:
        distMin = aux
  return distMin

def getAverageDistance(centroid, cluster):
  dist = 0.0
  for instance in cluster:
    dist = dist + math.pow(distance.euclidean(instance,centroid), 2)
  return dist//len(cluster)

def distanciaAMano(ins1,ins2):
  a1 = math.pow(math.fabs(ins1[0]-ins2[0]),2)
  a2 = math.pow(math.fabs(ins1[1]-ins2[1]),2)
  a3 = math.pow(math.fabs(ins1[2]-ins2[2]),2)
  a4 = math.pow(math.fabs(ins1[3]-ins2[3]),2)  
  a5 = math.pow(math.fabs(ins1[4]-ins2[4]),2)  
  a6 = math.pow(math.fabs(ins1[5]-ins2[5]),2)
  suma = a1+a2+a3+a4+a5+a6
  total = math.sqrt(suma)
  #print (total)
  return total
  
def prueba():
  aux = read_file('customers.csv')
  listRadios = []
  listDiametros = []
  listDistancia = []
  
  for i in range(2,21):
    (clusters, centroids) = kmeans(i,aux)
    listRadios = []
    listDiametros = []
    listDistancia = []
    
    for clus, cent in zip(clusters, centroids):
      tamanho = len(clus)
      if tamanho <= 1:
        listRadios.append(0)
        listDiametros.append(0)
        listDistancia.append(0)
      else:
        listRadios.append(distance.euclidean(cent,clus[getMinMaxToTarget(cent,clus,max)]))
        listDiametros.append(getMinMaxDistFromList(clus))
        listDistancia.append(getAverageDistance(cent,clus))
	 
    print ("$$$$$$$$$$$$")
    print ("------------------------------------------------------------------------")
    print (listRadios)
    print ("------------------------------------------------------------------------")
    print (listDiametros)
    print ("------------------------------------------------------------------------")
    print (listDistancia)
  
  plt.plot(listRadios)
  plt.xlabel('K-centros')
  plt.savefig('Radios.png')
  
  plt.plot(listDiametros)
  plt.xlabel('K-centros')
  plt.savefig('Diametros.png')
  
  plt.plot(listDistancia)
  plt.xlabel('K-centros')
  plt.savefig('Distancia.png')
  
prueba()