import random
from createUser import *

questions = [
  'How to trim Strings in _? ',
  'How to cast from Integer to String in _? ',
  '_ or imagination for scripting? ',
  'Does Santa use _? ',
  'Where _ comes from? ',
  'Is _ the best language? ',
  'Is _ the best language to learn programing? ',
  'Is _ the best language for Web programing? ',
  'Who hates _? ',
  '_, who hates it? ',
  'Is the content of this page generated randomly?',
  'Why the responses to the questions are all unrelated?',
  'Is the average user of this page mentally disabled?',
  ]

languages = ['Python', 'C++', 'C', 'C#', 'PHP', 'Ada', 'Haskell', 'Prolog', 'Lisp', 'R', 'Java', 'JavaScript', 'Matlab', 'BASIC', 'COBOL', 'Bash', 'Erlang', 'Go', 'Pascal', 'Perl', 'Prolog', 'Ruby', 'Rust']

def create_title():
  return random.choice(questions).replace('_', random.choice(languages))

def create_question():
  title   = create_title()
  text    = title+title+title+title
  userId = get_name_lastname_alias()[2]
  tags    = get_expertises_tags()
  return {"titulo": title, "tags": tags, "texto": text, "idusuario": userId}
