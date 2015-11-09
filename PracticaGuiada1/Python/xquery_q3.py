#Grupo 3
#Hristo Ivanov Ivanov
#Alberto Lorente Sánchez
import eulexistdb.db

db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

q = """
for $e in doc("/db/sgdi/factbook.xml")/mondial/country
    let $cap := $e/@capital/string()
    let $aux := <elem>
            {
                for $city in $e/city
                    where $city/@id/string() = $cap
                    return <elem>  <country>{$e/@name/string()}</country>  {$city/name}  </elem>
            }
            {
                for $city in $e/province/city
                    where $city/@id/string() = $cap
                    return <elem>  <country>{$e/@name/string()}</country>  {$city/name}  </elem>
            }
        </elem>
    return $aux
"""

r = db.query(q, how_many=0)

nodes = r.results

i=0
for node in nodes:
    i+=1
    if node.text:
        print i, (node[0][0].text, node[0][1].text)






