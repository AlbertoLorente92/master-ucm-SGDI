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
  rules = []
  for cl in classes:
    conj = [x for x in inst]
    while True:
      if not cl in [x[-1] for x in conj]:
        break
      rule = prism_inner(conj, attr_dic, cl)
      rules.append([rule, cl])
      conj = removeCoveredIns(rule, conj)
  return rules

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
  inst, attr_dic, classes = read_file('aux.csv')
  rules = prism_pro (inst, attr_dic, classes)
  aux_method(rules)
  #print json.dumps(rules, indent=4)
  #write_dot_tree(rules, 'aux.dot')


def aux_method(rules):
  for rule in rules:
    print rule
  tree = create_tree_from_rules(rules)
  write_dot_tree(tree, rules, 'out_prism.dot')

def create_tree_from_rules(rules):
  arbol = {'nombre': 'datos', 'hijos':{}}
  for rule in rules:
    if len(rule[0]) == 1:
      cond_str  = '' + rule[0][0][1] + '\n' + rule[0][0][2] 
      arbol['hijos'][cond_str] = {'nombre' : rule[1]}
  rules = [x for x in rules if len(x[0]) > 1 ]

  while( len(rules) > 0 ):
    cond      = most_repeating_condition(rules)
    cond_str  = '' + cond[1] + '\n' + cond[2] 
    rules_a   = get_rules_have_condition(rules, cond)
    rules_a   = remove_condition(rules_a, cond)
    rules     = get_rules_have_condition(rules, cond, inverted=True)
    arbol['hijos'][cond_str] = create_tree_from_rules(rules_a)

  return arbol

def most_repeating_condition(rules):
  conditions = [y for x in rules for y in x[0]]
  attr = Counter(conditions)
  attr = max(attr, key=attr.get)
  return attr


def get_rules_have_condition(rules, condition, inverted=False):
  if inverted:
    return [x for x in rules if condition not in x[0]]
  return [x for x in rules if condition in x[0]]


def remove_condition(rules, condition):
  return [ [ [y for y in x[0] if y != condition], x[1]] for x in rules]


def getDot(tDict, count = [0]):
  out = ''
  nombreOld = tDict['nombre'] 
  tDict['nombre'] += `count[0]`
  count[0] += 1
  if 'hijos' in tDict:
    out += '{} [shape=box, label="", width=.1];\n'.format(tDict['nombre'], nombreOld )
  else:
    out += '{} [label="{}", width=.0];\n'.format(tDict['nombre'], nombreOld )
  if 'hijos' in tDict:
    for hijoK, hijoV in tDict['hijos'].iteritems():
      out += getDot(hijoV, count=count)
      out += '{} -> {} [ label="{}" ];\n'.format(tDict['nombre'], hijoV['nombre'], hijoK )
  return out

def write_dot_tree(id3_tree, rules, filename):
  to_write = 'digraph graphname {\n'
  to_write += 'rankdir="LR";'
  to_write += getDot(id3_tree)
  to_write += '}\n'
  fd = open(filename, 'w')
  fd.write(to_write)
  fd.close()

prueba()
