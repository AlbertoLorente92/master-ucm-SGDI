import random

user_lastname = ['SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES', 'MILLER', 'DAVIS', 'GARCIA', 'RODRIGUEZ', 'WILSON', 'MARTINEZ', 'ANDERSON', 'TAYLOR', 'THOMAS', 'HERNANDEZ', 'MOORE', 'MARTIN', 'JACKSON', 'THOMPSON', 'WHITE', 'LOPEZ', 'LEE', 'GONZALEZ', 'HARRIS', 'CLARK', 'LEWIS', 'ROBINSON', 'WALKER', 'PEREZ', 'HALL', 'YOUNG', 'ALLEN', 'SANCHEZ']
user_name = ['JAMES', 'JOHN', 'ROBERT', 'MICHAEL', 'WILLIAM', 'DAVID', 'RICHARD', 'CHARLES', 'JOSEPH', 'THOMAS', 'CHRISTOPHER', 'DANIEL', 'PAUL', 'MARK', 'DONALD', 'GEORGE', 'KENNETH', 'STEVEN', 'EDWARD', 'BRIAN', 'RONALD', 'ANTHONY', 'KEVIN', 'JASON', 'MATTHEW', 'GARY', 'TIMOTHY', 'JOSE', 'LARRY', 'JEFFREY', 'FRANK', 'SCOTT', 'ERIC', 'STEPHEN']


user_address_country = ['Spain', 'Bulgaria', 'France', 'Germany', 'Israel', 'Russia', 'Italy', 'England', 'Ireland', 'Portugal', 'Colombia']
user_address_cities = ['city_0', 'city_1', 'city_2', 'city_3', 'city_4', 'city_5', 'city_6', 'city_7', 'city_8', 'city_9', 'city_10']
user_address_postalCode = ['02800', '12801', '22802', '32803', '42804', '52805', '62806', '72807', '82808', '92809']

expertises = ['json', 'linux', 'mongodb', 'pymongo', 'storm', 'cloud', 'map-reduce', 'sql', 'ada', 'java', 'c', 'c++', 'c#', 'python', 'javascript', 'php', 'vim', 'jquery', 'android', 'matlab']

def create_alias(name, lastname):
  return name.lower()+'_'+lastname.lower()

def get_expertises_tags():
  expertise = [random.choice(expertises) for x in range(0, random.randint(0,6))]
  expertise = list(set(expertise))
  return expertise


def create_address():
  country     = random.choice(user_address_country)
  city        = random.choice(user_address_cities)
  postalCode  = random.choice(user_address_postalCode)
  return {'pais': country, 'cuidad': city, 'cp': postalCode}

def get_name_lastname_alias():
  name      = random.choice(user_name)
  lastname  = random.choice(user_lastname)
  alias     = create_alias(name, lastname)
  return name, lastname, alias

def create_user():
  name, lastname, alias = get_name_lastname_alias()
  expertise = get_expertises_tags()
  address   = create_address()
  return {"_id": alias, "nombre": name, "apellidos": lastname, "experiencia": expertise, "direccion": address}
