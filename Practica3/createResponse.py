import random
from createUser import *
responses = [
  'Yes.',
  'No.',
  'No, it\'s Eminem.',
  'Yes, it\'s Santa.',
  'Stop asking questions.',
  'Hello.',
  'Its all random.',
  ]

comments = ['Stupid.', 'Bad response.', 'Good response.', 'Smart.', 'Not related.', 'Is this random?', 'Solid 5/7']
scores = ['good', 'bad']

def create_response():
  text = random.choice(responses)
  userId = get_name_lastname_alias()[2]
  return {
		"texto": text,
		"valoracion":[],
		"idusuario": userId,
		"idpregunta": None, # In the test we will query first for this value.
		"comentario": []
	}

def create_comment():
  text = random.choice(responses)
  userId = get_name_lastname_alias()[2]
  return {"texto": text, "idusuario": userId}

def create_score():
  score = random.choice(scores)
  userId = get_name_lastname_alias()[2]
  return { "nota": score, "idusuario": userId}
