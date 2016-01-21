# -*- coding: utf-8 -*-
from createUser import *
from createQuestion import *
from createResponse import *
from consultas import *
import json

import pymongo
from pymongo import MongoClient

from bson.objectid import ObjectId

import time
import sys


def create_random_data():
  list_of_user_Ids = []
  list_of_question_Ids = []
  list_of_response_Ids = []

  print 'Insertar 30 Usuarios.'
  for x in range(0,30):
    time.sleep(.05)
    user = create_user()
    response = insert_user(user['_id'],user['nombre'],user['apellidos'],user['experiencia'],user['direccion'])
    response = json.loads(response)
    if response['status'] == 0:
      list_of_user_Ids.append(response['msg'])

  print 'Insertar 30 preguntas.'
  for x in range(0,30):
    time.sleep(.05)
    question = create_question()
    question['idusuario'] = random.choice(list_of_user_Ids)
    response = add_question(question['titulo'],question['tags'],question['texto'],question['idusuario'])
    response = json.loads(response)
    if response['status'] == 0:
      list_of_question_Ids.append(ObjectId(response['msg']['$oid']))

  print 'Insertar 120 respuestas.'
  for x in range(0,120):
    time.sleep(.05)
    response = create_response()
    response['idpregunta'] = random.choice(list_of_question_Ids)
    response['idusuario']  = random.choice(list_of_user_Ids)
    response = add_answer(response['texto'],response['idusuario'],response['idpregunta'])
    response = json.loads(response)
    if response['status'] == 0:
      list_of_response_Ids.append(ObjectId(response['msg']['$oid']))

  print 'Insertar 120 comentarios.'
  for x in range(0,120):
    time.sleep(.05)
    comment = create_comment()
    comment ['idcontestacion'] = random.choice(list_of_response_Ids)
    comment ['idusuario']  = random.choice(list_of_user_Ids)
    response = add_comment(comment['texto'],comment['idusuario'],comment['idcontestacion'])

  print 'Insertar 120 valoraciones.'
  for x in range(0,120):
    time.sleep(.05)
    score = create_score()
    score ['idcontestacion'] = random.choice(list_of_response_Ids)
    score ['idusuario']  = random.choice(list_of_user_Ids)
    response = add_answer(score['nota'],score['idusuario'],score['idcontestacion'])


def provision_data():
  users = db.usuarios.find({},{'_id':1})
  list_of_user_Ids = [us['_id'] for us in users]
  questions= db.preguntas.find({},{'_id':1})
  list_of_question_Ids = [qu['_id'] for qu in questions]
  responses = db.contestaciones.find({},{'_id':1})
  list_of_response_Ids = [re['_id'] for re in responses]

  if len(list_of_user_Ids) == 0 or len(list_of_question_Ids) == 0 or len(list_of_response_Ids) == 0:
    print 'Problema al aproviosionar. Intenta insertar datos primero.'
    my_exit()

  return list_of_user_Ids, list_of_question_Ids, list_of_response_Ids


def test1(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  print 'Insertar 30 usuarios generados aleatoriamente.'
  for x in range(0,30):
    time.sleep(.05)
    user = create_user()
    response = insert_user(user['_id'],user['nombre'],user['apellidos'],user['experiencia'],user['direccion'])
    response = json.loads(response)
    if response['status'] == 0:
      list_of_user_Ids.append(response['msg'])
    print '    ', response


def test2(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  print 'Ejecutar 10 veces update_user() con Ids que si estan la tabla.'
  for x in range(0,10):
    time.sleep(.05)
    user = create_user()
    user['_id'] = random.choice(list_of_user_Ids)
    response = update_user(user['_id'],user['nombre'],user['apellidos'],user['experiencia'],user['direccion'])
    response = json.loads(response)
    print '    ', response


  print 'Ejecutar 10 veces update_user() con Ids generados aleatoriamente.'
  for x in range(0,10):
    time.sleep(.05)
    user = create_user()
    response = update_user(user['_id'],user['nombre'],user['apellidos'],user['experiencia'],user['direccion'])
    response = json.loads(response)
    print '    ', response

def test3(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  print 'Insertar 30 preguntas generadas aleatoriamente, utilizando usuarios que existen.'
  for x in range(0,30):
    time.sleep(.05)
    question = create_question()
    question['idusuario'] = random.choice(list_of_user_Ids)
    response = add_question(question['titulo'],question['tags'],question['texto'],question['idusuario'])
    response = json.loads(response)
    if response['status'] == 0:
      list_of_question_Ids.append(ObjectId(response['msg']['$oid']))
    print '    ', response

  print 'Insertar 30 preguntas generadas aleatoriamente, utilizando usuarios aleatorios.'
  for x in range(0,30):
    time.sleep(.05)
    question = create_question()
    response = add_question(question['titulo'],question['tags'],question['texto'],question['idusuario'])
    response = json.loads(response)
    if response['status'] == 0:
      list_of_question_Ids.append(ObjectId(response['msg']['$oid']))
    print '    ', response

def test4(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  print 'Insertar 60 respuestas aleatorias.'
  for x in range(0,60):
    time.sleep(.05)
    response = create_response()
    response['idpregunta'] = random.choice(list_of_question_Ids)
    response['idusuario']  = random.choice(list_of_user_Ids)
    response = add_answer(response['texto'],response['idusuario'],response['idpregunta'])
    response = json.loads(response)
    if response['status'] == 0:
      list_of_response_Ids.append(ObjectId(response['msg']['$oid']))
    print '    ', response

  print 'Insertar 60 respuestas aleatorias, utilizando usuarios aleatorios.'
  for x in range(0,60):
    time.sleep(.05)
    response = create_response()
    response['idpregunta'] = random.choice(list_of_question_Ids)
    response = add_answer(response['texto'],response['idusuario'],response['idpregunta'])
    response = json.loads(response)
    if response['status'] == 0:
      list_of_response_Ids.append(ObjectId(response['msg']['$oid']))
    print '    ', response

def test5(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  print 'Insertar 60 comentarios aleatorios.'
  for x in range(0,60):
    time.sleep(.05)
    comment = create_comment()
    comment ['idcontestacion'] = random.choice(list_of_response_Ids)
    comment ['idusuario']  = random.choice(list_of_user_Ids)
    response = add_comment(comment['texto'],comment['idusuario'],comment['idcontestacion'])
    response = json.loads(response)
    print '    ', response

  print 'Insertar 60 comentarios aleatorios, utilizando usuarios aleatorios.'
  for x in range(0,60):
    time.sleep(.05)
    comment = create_comment()
    comment ['idcontestacion'] = random.choice(list_of_response_Ids)
    response = add_comment(comment['texto'],comment['idusuario'],comment['idcontestacion'])
    response = json.loads(response)
    print '    ', response

  print 'Intentar insertar 20 comentarios aleatorios, utilizando un idcontestacion aleatorio'
  for x in range(0,20):
    time.sleep(.05)
    comment = create_comment()
    comment ['idcontestacion'] = ObjectId()
    comment ['idusuario']  = random.choice(list_of_user_Ids)
    response = add_comment(comment['texto'],comment['idusuario'],comment['idcontestacion'])
    response = json.loads(response)
    print '    ', response

def test6(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  print 'Insertar 60 valoraciones aleatorias.'
  for x in range(0,60):
    time.sleep(.05)
    score = create_score()
    score ['idcontestacion'] = random.choice(list_of_response_Ids)
    score ['idusuario']  = random.choice(list_of_user_Ids)
    response = score_answer(score['nota'],score['idusuario'],score['idcontestacion'])
    response = json.loads(response)
    print '    ', response

  print 'Insertar 60 valoraciones aleatorias, utilizando usuarios aleatorios.'
  for x in range(0,60):
    time.sleep(.05)
    score = create_score()
    score ['idcontestacion'] = random.choice(list_of_response_Ids)
    response = score_answer(score['nota'],score['idusuario'],score['idcontestacion'])
    response = json.loads(response)
    print '    ', response

  print 'Intentar insertar 20 valoraciones aleatorias, utilizando un idcontestacion aleatorio'
  for x in range(0,20):
    time.sleep(.05)
    score = create_score()
    score ['idcontestacion'] = ObjectId()
    score ['idusuario']  = random.choice(list_of_user_Ids)
    response = score_answer(score['nota'],score['idusuario'],score['idcontestacion'])
    response = json.loads(response)
    print '    ', response

def test7(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  print 'Invocamos update_score 300 veces, Utilizando un idcontestacion y idusuario aleatorios.'
  print 'Al ser datos aleatorios la mayoria de actualizaciones fallaran: {u\'status\': 0, u\'msg\': 0} '
  print 'Cada poco tiempo habra suerte y escogeremos un usuario que haya \npuntuado el la respuesta escogida: {u\'status\': 0, u\'msg\': 1} '
  for x in range(0,300):
    score = create_score()
    score ['idcontestacion'] = random.choice(list_of_response_Ids)
    score ['idusuario']  = random.choice(list_of_user_Ids)
    response = update_score(score['nota'],score['idusuario'],score['idcontestacion'])
    response = json.loads(response)
    print '    ', response

def test8(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  print 'Borrar 10 preguntas escogidas de forma aleatoria. Podemos intentar eliminar una pregunta dos veces.'
  for x in range(0,10):
    response = random.choice(list_of_question_Ids)
    response = delete_question(response)
    response = json.loads(response)
    print '    ', response

def test9(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  print 'Nos traemos 3 preguntas que si existen.'
  for x in range(0,3):
    response = random.choice(list_of_question_Ids)
    response = get_question(response)
    print '    ', response
  print 'Nos traemos 3 preguntas que no existen.'
  for x in range(0,3):
    response = ObjectId()
    response = get_question(response)
    print '    ', response
  pass

def test10(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  while True:
    tags = get_expertises_tags()
    if len(tags) < 3:
      break
  print 'Vamos a buscar estos tags:', tags
  response = get_question_by_tag(tags)
  print '     ', response

def test11(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  pass

def test12(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  pass

def test13(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  pass

def test14(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  pass

def test15(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  pass

def test16(list_of_user_Ids, list_of_question_Ids, list_of_response_Ids):
  pass


def my_exit():
  print 'Bye, Bye .....................'
  sys.exit()


if __name__=='__main__':
  print 'Hola.'

  while True:
    drop = raw_input('¿Limpiar y generar nuevos datos?[yes,no,solo_limpiar]: ')
    if drop == 'solo_limpiar':
      print 'Usamos db.collection.drop() para limpiar los datos, [usuarios, pregunatas, contestaciones]' 
      db.usuarios.drop()
      db.preguntas.drop()
      db.contestaciones.drop()
      my_exit()
    if drop == 'yes':
      print 'Usamos db.collection.drop() para limpiar los datos, [usuarios, pregunatas, contestaciones]' 
      db.usuarios.drop()
      db.preguntas.drop()
      db.contestaciones.drop()
      print 'Rellenamos las tres colleciones con datos aleatorios.\
              \nEsto toma su tiempo dado que entre inserciones tenemos un time.sleep(0.05).\
              \nEsto mejora las ordenaciones por tiempo.'
      create_random_data()
      break
    if drop == 'no':
      break

  toTest = raw_input('¿Que testear?[1..16] Qualquer otra cosa para salir.: ')
  if toTest not in [str(x) for x in range (1,17)]:
    my_exit()

  # insert_user() es el único que no necesita datos.
  if toTest != 1:
    print 'Provisionando con datos.'
    list_of_user_Ids, list_of_question_Ids, list_of_response_Ids = provision_data()

  list_of_tests = {1: test1, 2: test2, 3: test3, 4: test4, 5: test5, 6: test6, 7: test7, 8: test8, 9: test9, 10: test10, 11: test11, 12: test12, 13: test13, 14: test14, 15: test15, 16: test16}

  print
  print '==================================='
  print '==================================='

  print 'Testing', toTest+':'
  list_of_tests[int(toTest)](list_of_user_Ids, list_of_question_Ids, list_of_response_Ids)
  my_exit()
