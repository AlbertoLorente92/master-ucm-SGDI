import csv
from scipy.spatial import distance
import numpy as np
import math
from collections import Counter

def read_file(filename):
  infile = open(filename, 'r')
  reader = csv.reader(infile)
  lista = list(reader)
  inst = [[y for y in x] for x in lista[1:]]
  aux = lista[0]
  attrib_dic = {}
  # Importante. En la linea de Abajo he anadido un -1.
  # Es necesario para no coger las clases, solo los atributos.
  for i in range(0,len(aux)-1):
    aux2 = list(set([x[i] for x in lista[1:]]))
    attrib_dic[aux[i]] = (i , aux2)	
  classes =list(set([x[-1] for x in lista[1:]]))
  return (inst,attrib_dic,classes)

def id3(inst, attrib_dic, classes, candidates):
  pass

def entr(tList):
  entrSum = 0.0
  tLen = float(len(tList))
  aux = Counter(tList)
  for key, val in aux.iteritems():
    entrSum += -(val/tLen * math.log(val/tLen,2))
  return entrSum

def entrAttr(attr, tList):
  lenList = len(tList)
  sumEntr = 0.0
  for val in attr[1]:
    subConj = getSubConjunto(attr[0], val, tList)
    sumEntr += entr([x[-1] for x in subConj]) * len(subConj) / lenList
  return sumEntr

def selecciona_atributo(attrDict, tList):
  attrListEntr = {}
  for attrName, attrInfo in attrDict.iteritems():
    attrListEntr[attrName] = entrAttr(attrInfo, tList)
  print attrListEntr # TODO quitar este print
  return min(attrListEntr, key=attrListEntr.get)
  
def getSubConjunto(attrIndex, attrVal, tList):
  return [x for x in tList if x[attrIndex] == attrVal]
 
def prueba():
  # Esto es lo que haria el read_file, pero manual.
  inst = aux[1:]
  attrNames= aux[0]
  attrib_dic = {}
  for i in range(0,len(attrNames)-1):
    aux2 = list(set([x[i] for x in aux[1:]]))
    attrib_dic[attrNames[i]] = (i , aux2)	
  # Esto es lo que haria el read_file, pero manual.

  print selecciona_atributo(attrib_dic, inst)

aux = [
  ['atr1', 'atr2', 'atr3', 'atr4', 'class'],
  [1,1,1,1,3],
  [1,1,1,2,2],
  [1,1,2,1,3],
  [1,1,2,2,1],
  [1,2,1,1,3],
  [1,2,1,2,2],
  [1,2,2,1,3],
  [1,2,2,2,1],
  [2,1,1,1,3],
  [2,1,1,2,2],
  [2,1,2,1,3],
  [2,1,2,2,1],
  [2,2,1,1,3],
  [2,2,1,2,2],
  [2,2,2,1,3],
  [2,2,2,2,3],
  [3,1,1,1,3],
  [3,1,1,2,3],
  [3,1,2,1,3],
  [3,1,2,2,1],
  [3,2,1,1,3],
  [3,2,1,2,2],
  [3,2,2,1,3],
  [3,2,2,2,3] ]

prueba()

# Importante: Lo que esta bien.
#   -> Las funciones 'read_file' y 'entr' que hicimos juntos.
#      En la funcion 'read_file' he hecho una pequena correcion.
#   -> El array 'aux' con los valores de las diapos de ID3. Creo que vendra bien para probar el funcinamiento de esto.
#   -> La funcion 'getSubConjunto' que hace lo que indica el nombre.
#      Se invoca de la siguiente manera :  subConj = getSubConjunto(0, 1, aux)
#        Esto devuelve las filas que tienen valor 1 en la columna 0, las 8 primeras de aux.
#   -> La funcion 'entrAttr' que calcula la entropia para un atributo.
#      Se invoca de la siguiente manera :  entrAttr( (0, [1,2,3]), aux) . Esto devuelve 1.28669102172.
#   -> La funcion 'selecciona_atributo' devuelve el 'key' del atributo que aporta mayor ganancia.

# Con esto yo creo que quedaria tan solo implementar la funcion recursiva. La que genera el arbol.
