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
  for i in range(0,len(aux)):
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
  
  
def prueba():
  aux = read_file('car.csv')
  print entr([3,2,3,1,3,2,3,1])
prueba()
