from createUser import *
from createQuestion import *
from createResponse import *
from consultas import *
import json

import pymongo
from pymongo import MongoClient

from bson.objectid import ObjectId

import time

while True:
  drop = raw_input('Drop existing collections.[yes,no]:')
  if drop == 'yes':
    db.usuarios.drop()
    db.preguntas.drop()
    db.contestaciones.drop()
    break
  if drop == 'no':
    break

list_of_user_Ids = []
list_of_question_Ids = []
list_of_response_Ids = []

#1
print 'Insertar 30 usuarios generados aleatoriamente.'
for x in range(0,30):
  time.sleep(.05)
  user = create_user()
  response = insert_user(user['_id'],user['nombre'],user['apellidos'],user['experiencia'],user['direccion'])
  response = json.loads(response)
  if response['status'] == 0:
    list_of_user_Ids.append(response['msg'])
  print '    ', response


#2 Con ids que sames que existen.
print 'Ejecutar 10 veces update_user() con Ids que si estan la tabla.'
for x in range(0,10):
  time.sleep(.05)
  user = create_user()
  user['_id'] = random.choice(list_of_user_Ids)
  response = update_user(user['_id'],user['nombre'],user['apellidos'],user['experiencia'],user['direccion'])
  response = json.loads(response)
  print '    ', response


#2 Intentando Ids aleatorios.
print 'Ejecutar 10 veces update_user() con Ids generados aleatoriamente.'
for x in range(0,10):
  time.sleep(.05)
  user = create_user()
  response = update_user(user['_id'],user['nombre'],user['apellidos'],user['experiencia'],user['direccion'])
  response = json.loads(response)
  print '    ', response

#3 Insertar 30 preguntas generadas aleatoriamente, utilizando usuarios que existen.
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

#3 Insertar 30 preguntas generadas aleatoriamente, utilizando usuarios aleatorios.
print 'Insertar 30 preguntas generadas aleatoriamente, utilizando usuarios aleatorios.'
for x in range(0,30):
  time.sleep(.05)
  question = create_question()
  response = add_question(question['titulo'],question['tags'],question['texto'],question['idusuario'])
  response = json.loads(response)
  if response['status'] == 0:
    list_of_question_Ids.append(ObjectId(response['msg']['$oid']))
  print '    ', response

#4 Insertar 60 respuestas aleatorias.
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

#4 Insertar 60 respuestas aleatorias, utilizando usuarios aleatorios.
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

#5 Insertar 60 comentarios aleatorios.
print 'Insertar 60 comentarios aleatorios.'
for x in range(0,60):
  time.sleep(.05)
  comment = create_comment()
  comment ['idcontestacion'] = random.choice(list_of_response_Ids)
  comment ['idusuario']  = random.choice(list_of_user_Ids)
  response = add_comment(comment['texto'],comment['idusuario'],comment['idcontestacion'])
  response = json.loads(response)
  print '    ', response

#5 Insertar 60 comentarios aleatorios, utilizando usuarios aleatorios.
print 'Insertar 60 comentarios aleatorios, utilizando usuarios aleatorios.'
for x in range(0,60):
  time.sleep(.05)
  comment = create_comment()
  comment ['idcontestacion'] = random.choice(list_of_response_Ids)
  response = add_comment(comment['texto'],comment['idusuario'],comment['idcontestacion'])
  response = json.loads(response)
  print '    ', response

