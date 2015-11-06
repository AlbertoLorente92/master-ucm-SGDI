from mrjob.job import MRJob


class MRWordCount(MRJob):

	# Fase MAP (line es una cadena de texto)
  def mapper(self, key, line):
    words = [x for x in line.split(",")]
    yield "" + words[1] + words[2] , float(words[8])

	# Fase REDUCE (key es una cadena texto, values un generador de valores)
  def reducer(self, key, values):
    Mmax = values.next()
    Mmin = Mmax
    for val in values:
      if Mmax < val:
        Mmax = val
      if Mmin > val:
        Mmin = val
       
    yield key, (Mmin, Mmax)


if __name__ == '__main__':
    MRWordCount.run()
