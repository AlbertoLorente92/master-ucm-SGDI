#Grupo 3
#Hristo Ivanov Ivanov
#Alberto Lorente Sánchez
import eulexistdb.db

db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

q = """
for $e in doc("/db/sgdi/factbook.xml")/mondial/country
    let $a := <id_pais> {$e/@id/string()} </id_pais>
    let $b := <codigo_pais> {$e/@datacode/string()} </codigo_pais>
    return <elem><elem>{$e/@name/string()}</elem> {$a} {$b} </elem>
"""

r = db.query(q, how_many=0)

nodes = r.results

i=0
for node in nodes:
    i+=1
    print i, (node[0].text, node[1].text, node[2].text)

