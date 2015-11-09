#Grupo 3
#Hristo Ivanov Ivanov
#Alberto Lorente Sánchez
import eulexistdb.db

db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

q = """for $e in doc("/db/sgdi/factbook.xml")/mondial/country 
           return <elem>{$e/@name/string()}</elem>"""

r = db.query(q, how_many=0)

nodes = r.results

i=0
for node in nodes:
    i+=1
    print i, node.text 


