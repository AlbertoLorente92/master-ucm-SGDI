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
import json
from collections import Counter
from bson import json_util
from datetime import datetime


from bson import Binary, Code
from bson.json_util import dumps


client = MongoClient()
db = client.sgdi_grupo_03

# 1. Añadir un usuario
def insert_user(_id, nombre, apellidos, experiencia, direccion):
  user = form_usuario(_id, nombre, apellidos, experiencia, direccion)
  if not user:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete user.'}, default=json_util.default)
  try:
    result = db.usuarios.insert_one(user)  
  except pymongo.errors.DuplicateKeyError, e:
    return json.dumps({'status' : 1, 'msg' : 'Duplicate Key Error: '+_id}, default=json_util.default)
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.inserted_id}, default=json_util.default)
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'}, default=json_util.default)

# 2. Actualizar un usuario
def update_user(_id, nombre, apellidos, experiencia, direccion):
  user = form_usuario(_id, nombre, apellidos, experiencia, direccion, fecha=False)
  if not user:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete user.'}, default=json_util.default)
  result = db.usuarios.replace_one({'_id':_id}, user)
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.matched_count}, default=json_util.default)
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged update.'}, default=json_util.default)


# 3. Añadir una pregunta
def add_question( titulo, tags, texto, idusuario):
  question = form_question( titulo, tags, texto, idusuario)
  if not question:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete question.'}, default=json_util.default)
  if json.loads(get_user(idusuario))['status'] != 0:
    return json.dumps({'status' : 1, 'msg' : 'Incorect Userid.'}, default=json_util.default)
  try:
    result = db.preguntas.insert_one(question)
  except pymongo.errors.DuplicateKeyError, e:
    return json.dumps({'status' : 1, 'msg' : 'Duplicate Key Error.'}, default=json_util.default)
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.inserted_id}, default=json_util.default)
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'}, default=json_util.default)


# 4. Añadir una respuesta a una pregunta.
def add_answer(texto, idusuario, idpregunta):
  answer = form_answer(texto, idusuario, idpregunta)
  if not answer:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete answer.'}, default=json_util.default)
  if json.loads(get_user(idusuario))['status'] != 0:
    return json.dumps({'status' : 1, 'msg' : 'Incorect Userid.'}, default=json_util.default)
  try:
    result =  db.contestaciones.insert_one(answer)
  except pymongo.errors.DuplicateKeyError, e:
    return json.dumps({'status' : 1, 'msg' : 'Duplicate Key Error.'}, default=json_util.default)
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.inserted_id}, default=json_util.default)
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'}, default=json_util.default)
    
# 5. Comentar una respuesta.
def add_comment(texto, idusuario, idcontestacion):
  comment = form_comment(texto, idusuario)
  if not comment:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete comment.'}, default=json_util.default)
  if json.loads(get_user(idusuario))['status'] != 0:
    return json.dumps({'status' : 1, 'msg' : 'Incorect Userid.'}, default=json_util.default)
  # $push for lists and $addtoSet for Sets
  result = db.contestaciones.update_one({'_id': idcontestacion},{'$addToSet' :{'comentario':comment}})
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.matched_count}, default=json_util.default)
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'}, default=json_util.default)


# 6. Puntuar una respuesta.
def score_answer(nota, idusuario, idcontestacion):
  score = form_score(nota, idusuario)
  if not score:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete comment.'}, default=json_util.default)
  if json.loads(get_user(idusuario))['status'] != 0:
    return json.dumps({'status' : 1, 'msg' : 'Incorect Userid.'}, default=json_util.default)
  result = db.contestaciones.update_one({'_id':idcontestacion, 'valoracion.idusuario' : {'$ne' : idusuario}},\
                                        {'$addToSet' :{'valoracion':score}})
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.matched_count}, default=json_util.default)
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged insert.'}, default=json_util.default)


# 7. Modificar una puntuacion de buena a mala o viceversa.
def update_score(nota, idusuario, idcontestacion):
  score = form_score(nota, idusuario)
  if not score:
    return json.dumps({'status' : 1, 'msg' : 'Incomplete comment.'}, default=json_util.default)
  result = db.contestaciones.update_one({'_id':idcontestacion, 'valoracion.idusuario':idusuario},\
                                        {'$set' :{'valoracion.$.nota':nota}})
  if result.acknowledged:
    return json.dumps({'status' : 0, 'msg' : result.matched_count}, default=json_util.default)
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged update.'}, default=json_util.default)


# 8. Borrar una pregunta junto con todas sus respuestas, comentarios y 
# puntuaciones
def delete_question(idpregunta):
  deleteQuestion = db.preguntas.delete_one({'_id':idpregunta})
  deleteAnswerAndComments = db.contestaciones.delete_many({'idpregunta':idpregunta})
  if deleteQuestion.acknowledged and deleteAnswerAndComments.acknowledged:
    msg  = str(deleteQuestion.deleted_count)+' questions removed, plus '
    msg += str(deleteAnswerAndComments.deleted_count)+' answers remover.'
    return json.dumps({'status' : 0, 'msg' : msg}, default=json_util.default)
  else:
    return json.dumps({'status' : 2, 'msg' : 'Not acknowledged delete.'}, default=json_util.default)

# 9. Visualizar una determinada pregunta junto con todas sus contestaciones
# y comentarios. A su vez las contestaciones vendran acompañadas de su
# numero de puntuaciones buenas y malas.
def get_question(idpregunta):
  question = db.preguntas.find_one({'_id': idpregunta})
  if not question:
    return json.dumps({'status' : 1, 'msg' : 'No question with id '+str(idpregunta)}, default=json_util.default)
  question['answers'] = []
  answers = db.contestaciones.find({'idpregunta':idpregunta})
  for ans in answers:
    valoraciones = [x['nota'] for x in ans['valoracion']]
    valoraciones = Counter(valoraciones)
    ans['resumen_valoraciones'] = valoraciones
    question['answers'].append(ans)

  return json.dumps({'status' : 0, 'result ': question}, indent=4, sort_keys=True, default=json_util.default)


# 10. Buscar preguntas con unos determinados tags y mostrar su titulo, su autor
# y su numero de contestaciones.
def get_question_by_tag(tags):
  questions = db.preguntas.find({'tags' : {'$all' : tags }}, {'_id':1, 'titulo':1, 'idusuario':1})
  _questions = []
  for qu in questions:
    qu['number_of_answers'] = db.contestaciones.count({'idpregunta' : qu['_id']})
    _questions.append(qu)
  return json.dumps({'status' : 0, 'result ': _questions}, indent=4, sort_keys=True, default=json_util.default)


# 11. Ver todas las preguntas o respuestas generadas por un determinado usuario.
def get_entries_by_user(idusuario):
  questions = db.preguntas.find({'idusuario':idusuario})
  questions = [qu for qu in questions]
  answers = db.contestaciones.find({'idusuario':idusuario})
  answers= [an for an in answers]
  user_info = {'questions' : questions, 'answers' : answers}
  return json.dumps({'status' : 0, 'result ': user_info}, indent=4, sort_keys=True, default=json_util.default)

# 12. Ver todas las puntuaciones de un determinado usuario ordenadas por 
# fecha. Este listado debe contener el tıtulo de la pregunta original 
# cuya respuesta se puntuo.
def get_scores(idusuario):
  scores = db.contestaciones.find({'valoracion.idusuario' : idusuario},\
      {'valoracion':{'$elemMatch':{'idusuario':idusuario}},'idpregunta':1, 'texto' : 1,'_id':0})\
      .sort('valoracion.fecha')
  _scores = []
  for cs in scores:
    cs['question_title'] = db.preguntas.find_one({'_id' : cs['idpregunta']}, {'titulo' : 1, '_id' : 0})['titulo']
    del cs['idpregunta']
    _scores.append(cs)
  return json.dumps({'status' : 0, 'result ':  _scores}, indent=4, sort_keys=True, default=json_util.default)


# 13. Ver todos los datos de un usuario.
def get_user(idusuario):
  usuario = db.usuarios.find_one({'_id' : idusuario})
  if not usuario:
    return json.dumps({'status' : 1, 'msg' : 'No user with id '+str(idusuario)}, default=json_util.default)
  return json.dumps({'status' : 0, 'result ': usuario}, indent=4, sort_keys=True, default=json_util.default)


# 14. Obtener los alias de los usuarios expertos en un determinado tema.
def get_uses_by_expertise(tema):
  usuarios = db.usuarios.find({'experiencia':tema},{'_id':1})
  usuarios = [us['_id'] for us in usuarios]
  if not usuarios:
    return json.dumps({'status': 1, 'msg': 'No user with experience in ' + tema}, default=json_util.default)
  return json.dumps({'status': 0, 'result': usuarios}, indent=4, sort_keys=True, default=json_util.default)

# 15. Visualizar las n preguntas mas actuales ordenadas por fecha, incluyendo
# el numero de contestaciones recibidas.
def get_newest_questions(n):
  questions = db.preguntas.find({},limit=n,sort=[('fecha',pymongo.DESCENDING)])
  if not questions:
    return json.dumps({'status': 1, 'msg': 'There is no questions'}, default=json_util.default)
  _questions = []
  for q in questions:
    q['num_respuestas'] = db.contestaciones.find({'idpregunta':q['_id']}).count()
    _questions.append(q)
  return json.dumps({'status':0, 'result': _questions}, indent=4, sort_keys=True, default=json_util.default)
    
# 16. Ver n preguntas sobre un determinado tema, ordenadas de mayor a menor por
# numero de contestaciones recibidas.
def get_questions_by_tag(n, tema):
  questions = db.preguntas.find({'tags':tema})
  _questions = []
  for q in questions:
    q['num_respuestas'] = db.contestaciones.find({'idpregunta':q['_id']}).count()
    _questions.append(q)
  if not _questions:
    return json.dumps({'status': 1, 'msg': 'There is no questions with tag '+tema}, default=json_util.default)
  _questions.sort(key=lambda x: x['num_respuestas'], reverse=True)
  return json.dumps({'status':0, 'result': _questions[:n]}, indent=4, sort_keys=True, default=json_util.default)

################################################################################
############################  FUNCIONES AUXILIARES  ############################
################################################################################
# Incluir aqui el resto de funciones necesarias
def form_usuario(_id, nombre, apellidos, experiencia, direccion, fecha=True):
  # Direccion debe tener los siguientes campos.
  if not 'pais' in direccion or not 'cuidad' in direccion or not 'cp' in direccion:
    return None
  # Experiencia puede ser vacio: un novato que quiere aprender.
  if not all([_id, nombre, apellidos]):
    return None
  user = 	{
		"_id": _id,
		"nombre": nombre,
		"apellidos": apellidos,
		"experiencia": experiencia,
		"direccion": direccion,
	}
  if fecha:
    user['fecha'] = datetime.now()
  return user

def form_question(titulo, tags, texto, idusuario):
  if not all([titulo, texto, idusuario]):
    return None
  question = {
    "titulo": titulo,    
    "tags": tags,
    "fecha": datetime.now(),
    "texto": texto,
    "idusuario": idusuario,
  }
  return question

def form_answer(texto, idusuario, idpregunta):
  if not all([texto, idusuario]):
    return None
  respuesta = {
		"fecha": datetime.now(),
		"texto": texto,
		"idusuario": idusuario,
    "idpregunta": idpregunta,
    "valoracion": [],
    "comentario": [],
  }
  return respuesta

def form_comment(texto, idusuario):
  if not all([texto, idusuario]):
    return None
  comment = {
		"fecha": datetime.now(),
		"texto": texto,
		"idusuario": idusuario,
  }
  return comment

def form_score(nota, idusuario):
  if not all([nota, idusuario]):
    return None
  score = {
		"fecha": datetime.now(),
		"nota": nota,
		"idusuario": idusuario,
  }
  return score
