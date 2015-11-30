import csv
from scipy.spatial import distance
import numpy as np
import math
import matplotlib.pyplot as plt

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
  
def prueba():
  aux = read_file('car.csv')
  print (len(aux[0]))
  print ("------------------------------------------------------------------------")
  print (aux[1])
  print ("------------------------------------------------------------------------")
  print (aux[2])
prueba()