import multiprocessing
from pprint import pprint
from functools import reduce
from multiprocessing import Pool
import tempfile
import os
import json


def is_palindrome(s):
    return s == s[::-1]

def split_file( filepath, parts ):
   # reads line by line and distributes between files
   # create temp files:
   f_parts = list()
   for i in range(parts):
      t = tempfile.NamedTemporaryFile(prefix="split", delete=False)
      f_parts.append({'name': t.name, 'fd': open(t.name,"w+")})
   
   with open(filepath, "r") as f_in:
      p = 0
      s = f_in.readline()
      while len(s) > 0:
         f_parts[p]['fd'].write(s)
         s = f_in.readline()
         p = p + 1
         if p == parts:
               p = 0
    
   return list(map(lambda x: x['name'], f_parts))

def count_words(filepath):
   result = {}
   result['WORD_COUNTS'] = {}
   result['PALINDROMS'] = 0
   result['TOTAL'] = 0
   result['LONGEST'] = list()
   result['TOTAL_LEN'] = 0
   
   with open(filepath, 'r') as f:
      words = [word.strip() for word in f.read().split()]
      for word in words:
         result['TOTAL'] += 1
         result['TOTAL_LEN'] += len(word)
         if word not in result['WORD_COUNTS']:
            result['WORD_COUNTS'][word] = 0
            if is_palindrome(word):
               result['PALINDROMS'] += 1
         result['WORD_COUNTS'][word] += 1
         
         if not result['LONGEST']:
            result['LONGEST'].append(word)
         elif len(word) > len(result['LONGEST'][0]):
            result['LONGEST'] = list()
            result['LONGEST'].append(word)
         elif len(word) == len(result['LONGEST'][0]):
            result['LONGEST'].append(word)

      return result


def merge_counts(result1, result2):
   for word, count in result2['WORD_COUNTS'].items():
      if word not in result1['WORD_COUNTS']:
         result1['WORD_COUNTS'][word] = 0
      result1['WORD_COUNTS'][word] += result2['WORD_COUNTS'][word]
   result1['PALINDROMS'] += result2['PALINDROMS']   
   result1['TOTAL'] += result2['TOTAL']
   result1['TOTAL_LEN'] += result2['TOTAL_LEN']

   if result1['LONGEST']:
      if len(result1['LONGEST'][0]) < len(result2['LONGEST'][0]):
         result1['LONGEST'] = result2['LONGEST']
      elif len(result1['LONGEST'][0]) == len(result2['LONGEST'][0]):
         result1['LONGEST'].extend(result2['LONGEST'])
   else:
      result1['LONGEST'] = result2['LONGEST']
   
   result1['AVG_LENGHT'] = int (result1['TOTAL_LEN'] / result1['TOTAL'])
   return result1


def process(fileName, threads):
   file_pool = split_file(fileName, threads)
   pool = multiprocessing.Pool(threads)
   per_doc_counts = list(pool.map(count_words, file_pool))
   for item in file_pool:
      os.unlink(item)
   result = reduce(merge_counts, 
                  [ {'WORD_COUNTS':{}, 'PALINDROMS': 0, 'TOTAL':0, 'LONGEST': list(), 'TOTAL_LEN': 0 } ] + per_doc_counts)
   return result

