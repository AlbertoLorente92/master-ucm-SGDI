from mrjob.job import MRJob
from scipy.spatial import distance
from collections import Counter
import csv
import os


class MRWordCount(MRJob):

  def read_file(self, filename):
    infile = open(filename, 'r')
    reader = csv.reader(infile)
    lista = list(reader)
    return [[float(y) for y in x[:-1]]+[x[-1]] for x in lista[1:]]

  def distancia(self, i1, i2):
    if len(i1) == len(i2):
      return distance.euclidean(i1[:-1], i2[:-1])
    if len(i1) == len(i2)-1:
      return distance.euclidean(i1[:], i2[:-1])
    if len(i1)-1 == len(i2):
      return distance.euclidean(i1[:-1], i2[:])
    print 'Epic Fail.'

  def mapper_init(self):
    # Archivo de test.
    self.test_set = self.read_file(curr_path+'/iris_test.csv')
  def mapper(self, key, line):
    # line es una entrada del archivo de entremaniento.
    if line.split(',')[0] == 'sepal length' : return 
    train_line = [float(x) for x in line.split(',')[:-1]] + line.split(',')[-1:]
    # Calculamos la distancia entre la entrada de
    # entrenamineto y todas las entradas de test.
    for test in self.test_set:
      # Devolvemos esa distancia utilizando la entrada de test
      # como 'key', de tal manera que las distancias para cada entrada
      # de test se juntaran en el reducer/combiner.
      yield test, (train_line[-1], self.distancia(test, train_line))

  def combiner_init(self):
    # La k que queremos utilizar en el 'knn'.
    self.k = 10
  def combiner(self, key, values):
    # Ordenamos por distancia y tan solo devolvemos las 10 menores.
    yield key, sorted(values, key=lambda tup: tup[1])[:self.k]

  def reducer_init(self):
    self.k = 10
  def reducer(self, key, values):
    # Aplanamos la lista.
    values = [val for sublist in values for val in sublist]
    # Volvemos a coger los 10 primeros.
    dist_min = sorted(values, key=lambda tup: tup[1])[:self.k]
    aux=Counter([x[0] for x in dist_min])
    # Devolvemos la entrada de test con su clase más probable.
    yield (key, max(aux, key=aux.get))
    
curr_path = os.getcwd()
if __name__ == '__main__':
    MRWordCount.run()
