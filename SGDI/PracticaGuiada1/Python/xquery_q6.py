#Grupo 3
#Hristo Ivanov Ivanov
#Alberto Lorente Sánchez
import eulexistdb.db

db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

q = """
for $e in doc("/db/sgdi/factbook.xml")/mondial/country
    let $aux := <elem>
            {
                for $city in $e/city
                    return <elem>  <country>{$e/@name/string()}</country>  {$city/name}  </elem>
            }
            {
                for $city in $e/province/city
                    return <elem>  <country>{$e/@name/string()}</country>  {$city/name}  </elem>
            }
        </elem>
    where $e/@inflation > 20.0
    return $aux
"""

r = db.query(q, how_many=0)

nodes = r.results

i=0
for node in nodes:
    for node_1 in node:
        i+=1
        print i, {'pais':node_1[0].text, 'cuidad':node_1[1].text}
