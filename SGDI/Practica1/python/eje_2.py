# Grupo 3
# Alberto Lorente
# Hristo Ivanov

from mrjob.job import MRJob


class MRWordCount(MRJob):

	# Fase MAP (line es una cadena de texto)
  def mapper(self, key, line):
    words = [x for x in line.split("	")]
    if words[4] == "--":
        return
    if float(words[2]) < 2.0:
      yield 155, words[0]

	# Fase REDUCE (key es una cadena texto, values un generador de valores)
  def reducer(self, key, values):
    aux = list(values)
    yield len(aux), aux


if __name__ == '__main__':
    MRWordCount.run()
