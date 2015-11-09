from mrjob.job import MRJob
import re
import os
from collections import Counter
import operator

class MRWordCount(MRJob):

  def mapper(self, key, line):
    line = re.sub('".*"', '', line)
    line = re.sub(' +', ' ', line)
    word = line.split(' ');
    if word[3] == '-': word[3] = '0'

    if re.match('4..', word[2]) or re.match('5..', word[2]): word[2] = 1
    else: word[2] = 0

    yield word[0], [1, int(word[3]), word[2]]

  def combiner(self, key, values):
    yield key, map(sum,zip(*values))

  def reducer(self, key, values):
    yield key, map(sum,zip(*values))

if __name__ == '__main__':
    MRWordCount.run()
