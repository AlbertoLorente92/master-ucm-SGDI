# -*- coding: utf-8 -*-
"""
Autores: Hristo Ivanov, Alberto Lorente
Grupo 3

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no 
haber colaborado de ninguna manera con otros grupos, haber compartido el ćodigo 
con otros ni haberlo obtenido de una fuente externa.
"""

#################################################################
## Es necesario añadir los parámetros adecuados a cada función ##
#################################################################

import pymongo
from pymongo import MongoClient
import json, ast
from bson import Binary, Code
from bson.json_util import dumps



client = MongoClient()
db = client.pruebas

# 1. Añadir un usuario
def insert_user(_id, nombre, apellidos, experiencia, fecha, direccion):
  user = form_usuario(_id, nombre, apellidos, experiencia, fecha, direccion)
  if not user:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete user.'})
  try:
    result = db.usuarios.insert_one(user)  
  except pymongo.errors.DuplicateKeyError, e:
    return json.dumps({'status' : 1, 'msg' : 'Duplicate Key Error.'})
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : str(result.inserted_id)})
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'})

# 2. Actualizar un usuario
def update_user(_id, nombre, apellidos, experiencia, fecha, direccion):
  user = form_usuario(_id, nombre, apellidos, experiencia, fecha, direccion)
  if not user:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete user.'})
  result = db.usuarios.replace_one({'_id':_id}, user)
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.matched_count})
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged update.'})


# 3. Añadir una pregunta
def add_question( titulo, tags, fecha, texto, idusuario):
  question = form_question( titulo, tags, fecha, texto, idusuario)
  if not question:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete question.'})
  try:
    result = db.preguntas.insert_one(question)
  except pymongo.errors.DuplicateKeyError, e:
    return json.dumps({'status' : 1, 'msg' : 'Duplicate Key Error.'})
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : str(result.inserted_id)})
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'})


# 4. Añadir una respuesta a una pregunta.
def add_answer(fecha, texto, idusuario, idpregunta):
  answer = form_answer(fecha, texto, idusuario, idpregunta)
  if not answer:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete answer.'})
  try:
    result =  db.contestaciones.insert_one(answer)
  except pymongo.errors.DuplicateKeyError, e:
    return json.dumps({'status' : 1, 'msg' : 'Duplicate Key Error.'})
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : str(result.inserted_id)})
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'})
    
# 5. Comentar una respuesta.
def add_comment(fecha, texto, idusuario, idcontestacion):
  comment = form_comment(fecha, texto, idusuario)
  if not comment:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete comment.'})
  # $push for lists and $addtoSet for Sets
  result = db.contestaciones.update_one({'_id':idcontestacion},{'$addToSet' :{'comentario':comment}})
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.matched_count})
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'})


# 6. Puntuar una respuesta.
def score_answer(fecha, nota, idusuario, idcontestacion):
  score = form_score(fecha, nota, idusuario)
  if not score:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete comment.'})
  result = db.contestaciones.update_one({'_id':idcontestacion, 'valoracion.idusuario' : {'$ne' : idusuario}},\
                                        {'$addToSet' :{'valoracion':score}})
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.matched_count})
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'})


# 7. Modificar una puntuacion de buena a mala o viceversa.
def update_score(fecha, nota, idusuario, idcontestacion):
  score = form_score(fecha, nota, idusuario)
  if not score:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete comment.'})
  result = db.contestaciones.update_one({'_id':idcontestacion, 'valoracion.idusuario':idusuario},\
                                        {'$set' :{'valoracion.$.nota':nota}})
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.matched_count})
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'})


# 8. Borrar una pregunta junto con todas sus respuestas, comentarios y 
# puntuaciones
def delete_question(idpregunta):
    deleteQuestion = db.preguntas.remove({'_id':idpregunta})
    deleteAnswerAndComments = db.contestaciones.remove({'idpregunta':idpregunta})
    """los delete de arriba no tienen funciones para poder hacer esto....
    print deleteQuestion.items
    if not deleteQuestion.hasWriteError() and not deleteAnswerAndComments.hasWriteError():
      return json.dumps({'result': 'question, answer and comments deleted'})
    else:
      if deleteQuestion.hasWriteError():
        return json.dumps({'result': deleteQuestion.writeError.errmsg})
      else:
        return json.dumps({'result': deleteAnswerAndComments.writeError.errmsg})"""


# 9. Visualizar una determinada pregunta junto con todas sus contestaciones
# y comentarios. A su vez las contestaciones vendran acompañadas de su
# numero de puntuaciones buenas y malas.
def get_question(idpregunta):
    question = dumps(db.preguntas.find({'_id': idpregunta},{'_id':0,'titulo':1,'texto':1,'idusuario':1}))
    answer = dumps(db.contestaciones.find({'idpregunta':idpregunta},{'texto':1,'idusuario':1,'valoracion.nota':1,'_id':0}))
    jsonQ = byteify(json.loads(question))[0]
    data = byteify(json.loads(answer))[0]
    valoraciones = data['valoracion']
    bad = 0
    good = 0
    for val in valoraciones:
      if val['nota'] == 'bad':
        bad = bad + 1
      else:
        good =  good + 1
    jsonA = json.dumps({'respuesta':{'idusuario': data['idusuario'],'texto': data['texto'], 'buena': good, 'mala': bad}})
    jsonQ['respuesta'] = jsonA
    return jsonQ

# 10. Buscar preguntas con unos determinados tags y mostrar su titulo, su autor
# y su numero de contestaciones.
def get_question_by_tag(tags):
    jsonPreguntas = []
    for tag in tags:
      jsonPreguntas.append({'tags': tag})      
    question = byteify(json.loads(dumps(db.preguntas.find({'$or': jsonPreguntas},{'titulo':1,'idusuario':1,'_id':1}))))
    idPreguntas = []
    idP = [[0 for x in range(len(question))] for x in range(2)]
    i = 0
    for q in question:
      idPreguntas.append({'idpregunta': q['_id']})
      idP[i][0] = q['_id']
      idP[i][1] = 0
      i = i + 1
    answer = byteify(json.loads(dumps(db.contestaciones.find({'$or': idPreguntas},{'idpregunta':1}))))
    for a in answer:
      i = 0
      for i1,i2 in idP:    
        if i1 == a['idpregunta']:
          idP[i][1] = idP[i][1] + 1
        i = i + 1
    i = 0
    for q in question:
      for i1,i2 in idP:
        if i1 == q['_id']:
          question[i]['numrespuestas']= i2
      i = i +1   
    return question 

# 11. Ver todas las preguntas o respuestas generadas por un determinado usuario.
def get_entries_by_user(idusuario):
    question = byteify(json.loads(dumps(db.preguntas.find({'idusuario':idusuario},{'titulo':1,'texto':1,'_id':0}))))
    answer = byteify(json.loads(dumps(db.contestaciones.find({'idusuario':idusuario},{'texto':1,'_id':0}))))
    jsonExit = byteify(json.loads(dumps({})))
    jsonExit['questions']=question
    jsonExit['answers']=answer
    return jsonExit

# 12. Ver todas las puntuaciones de un determinado usuario ordenadas por 
# fecha. Este listado debe contener el tıtulo de la pregunta original 
# cuya respuesta se puntuo.
def get_scores(idusuario):
    scores = byteify(json.loads(dumps(db.contestaciones.find({'valoracion.idusuario':'drmane'},{'valoracion':{'$elemMatch':{'idusuario':'drmane'}},'idpregunta':1,'valoracion.fecha':1,'_id':0}).sort('valoracion.fecha'))))
    i = 0
    for x in scores:
      question = byteify(json.loads(dumps(db.preguntas.find({'_id':x['idpregunta']},{'titulo':1,'_id':0}))))[0]
      scores[i]['titulo']=question['titulo']
      i = i + 1
    return question


# 13. Ver todos los datos de un usuario.
def get_user(idusuario):
    usuario = byteify(json.loads(dumps(db.usuarios.find({'_id':idusuario}))))
    return usuario


# 14. Obtener los alias de los usuarios expertos en un determinado tema.
def get_uses_by_expertise(tema):
    usuario = byteify(json.loads(dumps(db.usuarios.find({'experiencia':tema},{'_id':1}))))
    return usuario


# 15. Visualizar las n preguntas mas actuales ordenadas por fecha, incluyendo
# el numero de contestaciones recibidas.
def get_newest_questions(n):
    questions = byteify(json.loads(dumps(db.preguntas.find().sort('fecha').limit(n))))
    i = 0
    for x in questions:
      answer = byteify(json.loads(dumps(db.contestaciones.find({'idpregunta':x['_id']}).count())))
      questions[i]['numrespuestas']=answer
      i = i + 1
    return questions


# 16. Ver n preguntas sobre un determinado tema, ordenadas de mayor a menor por
# numero de contestaciones recibidas.
def get_questions_by_tag(n, tema):
    questions = byteify(json.loads(dumps(db.preguntas.find({'tags':tema}).limit(n))))
    i = 0
    for x in questions:
      answer = byteify(json.loads(dumps(db.contestaciones.find({'idpregunta':x['_id']}).count())))
      questions[i]['numrespuestas']=answer
      i = i + 1
    return sorted(questions, key=lambda k: k['numrespuestas'], reverse=True)
    
################################################################################
############################  FUNCIONES AUXILIARES  ############################
################################################################################
# Convierte las salidas a UTF-8
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


# Incluir aqui el resto de funciones necesarias
def form_usuario(_id, nombre, apellidos, experiencia, fecha, direccion):
  # Direccion debe tener los siguientes campos.
  if not 'pais' in direccion or not 'cuidad' in direccion or not 'cp' in direccion:
    return None
  # Experiencia puede ser vacio: un novato que quiere aprender.
  if not all([_id, nombre, apellidos, fecha]):
    return None
  user = 	{
		"_id": _id,
		"nombre": nombre,
		"apellidos": apellidos,
		"experiencia": experiencia,
		"fecha": fecha,
		"direccion": direccion,
	}
  return user

def form_question(titulo, tags, fecha, texto, idusuario):
  if not all([titulo, fecha, texto, idusuario]):
    return None
  question = {
    "titulo": titulo,    
    "tags": tags,
    "fecha": fecha,
    "texto": texto,
    "idusuario": idusuario,
  }
  return question

def form_answer(fecha, texto, idusuario, idpregunta):
  if not all([fecha, texto, idusuario]):
    return None
  respuesta = {
		"fecha": fecha,
		"texto": texto,
		"idusuario": idusuario,
    "idpregunta": idpregunta,
    "valoracion": [],
    "comentario": [],
  }
  return respuesta

def form_comment(fecha, texto, idusuario):
  if not all([fecha, texto, idusuario]):
    return None
  comment = {
		"fecha": fecha,
		"texto": texto,
		"idusuario": idusuario,
  }
  return comment

def form_score(fecha, nota, idusuario):
  if not all([fecha, nota, idusuario]):
    return None
  score = {
		"fecha": fecha,
		"nota": nota,
		"idusuario": idusuario,
  }
  return score
################################################################################
############################  TEST #############################################
################################################################################

print insert_user( 
  'awesome_dude',
  'The Dude', 
  'Jeff The Dude Letrotski',
  ['python', 'orm'],
  '14-03-2015',
  {
    'pais' : 'spain',
    'cuidad' : 'madrid',
    'cp' : '28005',
  },
  )
print update_user( 
  'awesome_dude',
  'The Dude', 
  'Jeff The Dude Letrotski',
  ['python', 'orm', 'c++'],
  '14-03-2016',
  {
    'pais' : 'spain',
    'cuidad' : 'madrid',
    'cp' : '28005',
  }
  )
print add_question( 
  'Random Q',
  ['random'],
  '15-01-2016',
  'Win or lose',
  'AlbertoLorente92'
  )

print add_comment(
  '15-15-15',
  'Texto',
  'AlbertoLorente92',
  4
)

print score_answer(
  '15-15-14',
  'good',
  'hristoivanov',
  4
)

print update_score(
  '20-20-14',
  'good',
  'hristoivanov',
  4
)


print delete_question(1)
print get_question(1)
print get_question_by_tag(['json','fortran'])
print get_entries_by_user('linmdotor')
print get_scores('drmane')
print get_user('drmane')
print get_uses_by_expertise('java')
print get_newest_questions(2)
print get_questions_by_tag(2, 'linux')
