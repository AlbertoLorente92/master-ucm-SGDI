import csv
from scipy.spatial import distance
import numpy as np
import math
from collections import Counter
import json

def read_file(filename):
  infile = open(filename, 'r')
  reader = csv.reader(infile)
  lista = list(reader)
  inst = [[y for y in x] for x in lista[1:]]
  aux = lista[0]
  attrib_dic = {}
  for i in range(0,len(aux)-1):
    aux2 = list(set([x[i] for x in lista[1:]]))
    attrib_dic[aux[i]] = (i , aux2)	
  classes =list(set([x[-1] for x in lista[1:]]))
  return (inst,attrib_dic,classes)

# Algoritmo id3
def id3(inst, attrib_dic, classes, candidates):
  listClases = [x[-1] for x in inst]
  if len(set(listClases)) == 1:
    return {'nombre' : listClases[0]}
  claseModa = max(set(listClases), key=listClases.count)
  if len(candidates) == 0:
    return {'nombre' : claseModa}

  attr = selecciona_atributo(attrib_dic, inst)
  arbol = {'nombre':attr, 'hijos':{}}
  for val in candidates[attr][1]:
    subConj = getSubConjunto(candidates[attr][0], val, inst)
    if len(subConj) == 0:
      hoja = {'nombre' : claseModa}
    else:
      hoja = id3(subConj, attrib_dic, classes, {k:v for k,v in candidates.iteritems() if k != attr})
    arbol['hijos'][val] = hoja
  return arbol

# Calcula la entropia de una lista.
def entr(tList):
  entrSum = 0.0
  tLen = float(len(tList))
  aux = Counter(tList)
  for key, val in aux.iteritems():
    entrSum += -(val/tLen * math.log(val/tLen,2))
  return entrSum

# Devuelve la entropia de un atributo.
def entrAttr(attr, tList):
  lenList = len(tList)
  sumEntr = 0.0
  for val in attr[1]:
    subConj = getSubConjunto(attr[0], val, tList)
    sumEntr += entr([x[-1] for x in subConj]) * len(subConj) / lenList
  return sumEntr

# Devuelve el nombre del attributo que mayor ganancia de entropia
# aporta.
def selecciona_atributo(attrDict, tList):
  attrListEntr = {}
  for attrName, attrInfo in attrDict.iteritems():
    attrListEntr[attrName] = entrAttr(attrInfo, tList)
  return min(attrListEntr, key=attrListEntr.get)
  
# Devulve un subconjunto tal que, el atributo indicado por
# attrIndex siempre toma el valor definido por attrVal.
def getSubConjunto(attrIndex, attrVal, tList):
  return [x for x in tList if x[attrIndex] == attrVal]
 
def prueba():
  inst,attrib_dic,classes = read_file('aux.csv')
  arbol = id3(inst, attrib_dic, classes, attrib_dic)
  #print json.dumps(arbol, indent=4)
  write_dot_tree(arbol, 'out_id3.dot')

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
