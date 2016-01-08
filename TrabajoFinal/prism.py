import csv
import sys
from collections import Counter

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

"""
Parameters:
  inst:     Lista con las instancias.
  attr_dic: Diccionario con los valores de cada atributo.
  classes:  Lista de las posibles clases.
Comments:
  1. Generamos reglas para cada clase, 'cl', en 'classes'.
  2. Empezamos haciendo una copia de las instancias.
  3. Dejamos de generar reglas para la clase 'cl'
     al llegar a un 'conj' sin instancia de la clase.
  4. Invocamos a 'prism_inner' que genera una regla.
  5. Guardamos esa regla
  6. Eliminamos todas las instancias cubiertas por la nueva regla."""
def prism_outer(inst, attr_dic, classes):
  rules = []
  for cl in classes:                            #1
    conj = [x for x in inst]                    #2
    while cl in [x[-1] for x in conj]:          #3
      rule = prism_inner(conj, attr_dic, cl)    #4
      rules.append([rule, cl])                  #5
      conj = removeCoveredIns(rule, conj)       #6
  return rules

"""
Parameters:
  inst:     Lista con las instancias.
  attr_dic: Diccionario con los valores de cada atributo.
  cl:       Clase sobre la que generar la regla.
Comments:
  1. Generamos una lista con todas las clases en 'inst'.
  2. Si todas las instancias son de la clase 'cl', 
     la regla esta completa. No es necesario generar mas
     condiciones.
  3. Si la lista de atributos esta vacia, pero tenemos
     instancias de clases diferentes, tenemos un clash.
  4. Seleccionamos el par (atributo, valor) con mayor ganancia.
  5. Obtenemos las instancias que cumplen 'attr_val'.
  6. Invocamos de forma recursiva este metodo. De esta manera
     este metodo se repetira hasta que el #2 sea cierto. 
  7. Finalmente devolvemos la regla generada. """
def prism_inner(inst, attr_dic, cl):
  cls = [x[-1] for x in inst]                       #1
  if len(set(cls)) == 1:                            #2
    return []
  if len(attr_dic) == 0:                            #3
    aux = cls.count(cl) / float(len(cls))
    return [(-1, '__Clash__', str(aux))]
  pairList = []
  attr_val = select_pairAV(attr_dic, inst, cl)      #4
  pairList.append(attr_val)
  subSet = getSubSet(attr_val[0], attr_val[2], inst)#5
  attr_dic = [x for x in attr_dic if x[0]!=attr_val[0]]
  pairList += prism_inner(subSet, attr_dic, cl)     #6
  return pairList                                   #7
  
def inf(tList, cl):
  tLen = float(len(tList))
  aux = Counter(tList)
  entr = aux[cl]/tLen
  return entr, tLen

def inf_gainPairAV(pairAV, tList, cl):
  lenList = len(tList)
  subConj = getSubSet(pairAV[0], pairAV[2], tList)
  if len(subConj) == 0 :
    return None
  return inf([x[-1] for x in subConj], cl)

def select_pairAV(attrDict, tList, cl):
  listEntr = {}
  for pairAV in attrDict:
    listEntr[ pairAV ] = inf_gainPairAV(pairAV, tList, cl)
  return max(listEntr, key=listEntr.get)
  
def getSubSet(attrIndex, attrVal, tList, inv=False):
  if not inv:
    return [x for x in tList if x[attrIndex] == attrVal]
  return [x for x in tList if x[attrIndex] != attrVal]

def removeCoveredIns(pairList, inst):
  leftOvers = []
  for pairAV in pairList:
    if pairAV[1] == '__Clash__':
      continue
    leftOvers += getSubSet(pairAV[0], pairAV[2], inst, inv=True)
    inst       = getSubSet(pairAV[0], pairAV[2], inst)
  return leftOvers


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

if __name__=='__main__':
  file_name = sys.argv[1]
  inst, attr_dic, classes = read_file(file_name)
  rules = prism_outer (inst, attr_dic, classes)
  for rule in rules:
    print rule
  tree = create_tree_from_rules(rules)
  write_dot_tree(tree, rules, 'out_prism.dot')
