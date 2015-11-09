from mrjob.job import MRJob
import re
import os
from collections import Counter
import operator

class MRWordCount(MRJob):

	# Fase MAP (line es una cadena de texto)
  def mapper(self, key, line):
    line = re.sub("[^a-z]", " ", line.lower()) 
    words = line.split()
    for word in words:
      yield word, os.environ['map_input_file']

	# Fase REDUCE (key es una cadena texto, values un generador de valores)
  def reducer(self, key, values):
    aux = Counter(values)
    if max(aux.values()) > 20:
       yield key, sorted(aux.items(), key=lambda x: x[1], reverse=True)

if __name__ == '__main__':
    MRWordCount.run()
