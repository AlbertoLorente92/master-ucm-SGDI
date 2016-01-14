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

client = MongoClient()
db = client.pruebas

# 1. Añadir un usuario
def insert_user( user ):
  db.usuarios.insert(user)  


# 2. Actualizar un usuario
def update_user():
    pass


# 3. Añadir una pregunta
def add_question():
    pass


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


################################################################################
############################  TEST #############################################
################################################################################

user_1 = 	{
		"_id": "awesome_dude",
		"nombre": "The Dude",
		"apellidos": "Jeff 'The Dude' Letrotski",
		"experiencia": ["python","orm"],
		"fecha": "14-03-2014",
		"direccion": {
			"pais": "spain",
			"ciudad": "madrid",
			"cp": "28005"
		}
	}

insert_user( user_1 )
