import csv
from scipy.spatial import distance
import numpy as np
import math
from collections import Counter
import json
import time

def read_file(filename):
  infile = open(filename, 'r')
  reader = csv.reader(infile)
  lista = list(reader)
  inst = [[y for y in x] for x in lista[1:]]
  aux = lista[0]
  attrib_dic = []
  for i in range(0,len(aux)-1):
    aux2 = list(set([x[i] for x in lista[1:]]))
    for val in aux2 : 
      attrib_dic.append( (i, aux[i], val) )
  classes =list(set([x[-1] for x in lista[1:]]))
  return (inst,attrib_dic,classes)

# Algoritmo prism
def prism_pro(inst, attr_dic, classes):
  for cl in classes:
    conj = [x for x in inst]
    while True:
      if not cl in [x[-1] for x in conj]:
        break
      rule = prism_inner(conj, attr_dic, cl)
      print rule, '--------->', cl
      conj = removeCoveredIns(rule, conj)

def prism_inner(inst, attr_dic, cl):
  if len(set([x[-1] for x in inst])) == 1:
      return []
  pairList = []
  attr = select_pairAV(attr_dic, inst, cl)
  pairList.append(attr)
  subConj = getSubConjunto(attr[0], attr[2], inst)
  pairList += prism_inner(subConj, [x for x in attr_dic if x!=attr], cl)
  return pairList
  
# Calcula la entropia de una lista.
def entr(tList, cl):
  tLen = float(len(tList))
  aux = Counter(tList)
  entr = aux[cl]/tLen
  return entr, tLen

def entrPairAV(pairAV, tList, cl):
  lenList = len(tList)
  subConj = getSubConjunto(pairAV[0], pairAV[2], tList)
  if len(subConj) == 0 :
    return None
  #print entr([x[-1] for x in subConj], cl), pairAV[2]
  return entr([x[-1] for x in subConj], cl)

def select_pairAV(attrDict, tList, cl):
  listEntr = {}
  for pairAV in attrDict:
    listEntr[ pairAV ] = entrPairAV(pairAV, tList, cl)
  return max(listEntr, key=listEntr.get)
  
def getSubConjunto(attrIndex, attrVal, tList, inv=False):
  if not inv:
    return [x for x in tList if x[attrIndex] == attrVal]
  return [x for x in tList if x[attrIndex] != attrVal]

def removeCoveredIns(pairList, inst):
  leftOvers = []
  for pairAV in pairList:
    leftOvers += getSubConjunto(pairAV[0], pairAV[2], inst, inv=True)
    inst       = getSubConjunto(pairAV[0], pairAV[2], inst)
  return leftOvers
 
def prueba():
  print 'INTERESANTE : _________________________________________________________ '
  print '  http://www.csee.wvu.edu/~timm/cs591o/old/Rules.html'
  print '  aux.csv es sacado del ejemplo.'
  print 
  inst, attr_dic, classes = read_file('aux.csv')
  prism_pro (inst, attr_dic, classes)
  #print json.dumps(arbol, indent=4)
  #write_dot_tree(arbol, 'aux.dot')

def write_dot_tree(id3_tree, filename):
  to_write = 'digraph graphname {\n'
  to_write += getDot(id3_tree)
  to_write += '}\n'
  fd = open(filename, 'w')
  fd.write(to_write)
  fd.close()

# Devuelve un string que define el arbol formado por
# el algoritmo id3.
def getDot(tDict, count = [0]):
  out = ''
  nombreOld = tDict['nombre'] 
  tDict['nombre'] += `count[0]`
  count[0] += 1
  out += '{} [label="{}"];\n'.format(tDict['nombre'], nombreOld )
  if 'hijos' in tDict:
    for hijoK, hijoV in tDict['hijos'].iteritems():
      out += getDot(hijoV, count=count)
      out += '{} -> {} [ label="{}" ];\n'.format(tDict['nombre'], hijoV['nombre'], hijoK )
  return out

prueba()
