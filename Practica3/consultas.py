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

from pymongo import MongoClient
import json

client = MongoClient()
db = client.pruebas

# 1. Añadir un usuario
def insert_user(_id, nombre, apellidos, experiencia, fecha, direccion):
  user = form_usuario(_id, nombre, apellidos, experiencia, fecha, direccion)
  if not user:
    return json.dumps({'result' : 'Incomplete user.'})
  # TODO try, catch  duplicate key error index
  result = db.usuarios.insert_one(user)  
  if result.acknowledged:
    return json.dumps({'result' : result.inserted_id})
  else:
    return json.dumps({'result' : 'Not acknowledged insert.'})

# 2. Actualizar un usuario
def update_user(_id, nombre, apellidos, experiencia, fecha, direccion):
  user = form_usuario(_id, nombre, apellidos, experiencia, fecha, direccion)
  if not user:
    return json.dumps({'result' : 'Incomplete user.'})
  # TODO try, catch posible errors
  result = db.usuarios.replace_one({'_id':_id}, user)
  if result.acknowledged:
    return json.dumps({'result' : result.matched_count})
  else:
    return json.dumps({'result' : 'Not acknowledged insert.'})


# 3. Añadir una pregunta
def add_question( titulo, tags, fecha, texto, idusuario):
  question = form_question( titulo, tags, fecha, texto, idusuario)
  if not question:
    return json.dumps({'result' : 'Incomplete question.'})
  # TODO try, catch  duplicate key error index
  result = db.preguntas.insert_one(question)  
  if result.acknowledged:
    return json.dumps({'result' : result.inserted_id})
  else:
    return json.dumps({'result' : 'Not acknowledged insert.'})


# 4. Añadir una respuesta a una pregunta.
def add_answer():
    pass


# 5. Comentar una respuesta.
def add_comment():
    pass


# 6. Puntuar una respuesta.
def score_answer():
    pass


# 7. Modificar una puntuacion de buena a mala o viceversa.
def update_score():
    pass


# 8. Borrar una pregunta junto con todas sus respuestas, comentarios y 
# puntuaciones
def delete_question():
    pass


# 9. Visualizar una determinada pregunta junto con todas sus contestaciones
# y comentarios. A su vez las contestaciones vendran acompañadas de su
# numero de puntuaciones buenas y malas.
def get_question():
    pass


# 10. Buscar preguntas con unos determinados tags y mostrar su titulo, su autor
# y su numero de contestaciones.
def get_question_by_tag():
    pass


# 11. Ver todas las preguntas o respuestas generadas por un determinado usuario.
def get_entries_by_user():
    pass


# 12. Ver todas las puntuaciones de un determinado usuario ordenadas por 
# fecha. Este listado debe contener el tıtulo de la pregunta original 
# cuya respuesta se puntuo.
def get_scores():
    pass


# 13. Ver todos los datos de un usuario.
def get_user():
    pass


# 14. Obtener los alias de los usuarios expertos en un determinado tema.
def get_uses_by_expertise():
    pass


# 15. Visualizar las n preguntas mas actuales ordenadas por fecha, incluyendo
# el numero de contestaciones recibidas.
def get_newest_questions():
    pass


# 16. Ver n preguntas sobre un determinado tema, ordenadas de mayor a menor por
# numero de contestaciones recibidas.
def get_questions_by_tag():
    pass
    
    
################################################################################
############################  FUNCIONES AUXILIARES  ############################
################################################################################

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

def form_question( titulo, tags, fecha, texto, idusuario):
  if not all([titulo, fecha, texto, idusuario]):
    return None
  question = {
    "titulo": titulo    
    "tags": tags,
    "fecha": fecha,
    "texto": texto,
    "idusuario": idusuario,
  }
  return question



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
  },
  )

print insert_question( 
  'How to ',
  'The Dude', 
  'Jeff The Dude Letrotski',
  ['python', 'orm', 'c++'],
  '14-03-2016',
  {
    'pais' : 'spain',
    'cuidad' : 'madrid',
    'cp' : '28005',
  },
  )
