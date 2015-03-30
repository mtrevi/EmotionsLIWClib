# -*- coding: utf-8 -*-
"""
Build LIWC model that exploit the LIWC 2007 dictionary 
to infer positive and negative emotions.
__source__ : http://www.liwc.net/descriptiontable1.php
__author__ : Michele Trevisiol @trevi
"""


import sys
import pickle
from src.TextProcessingSupport import *


POSEMO = 126
NEGEMO = 127
INVERT_CAT = 19
CATEGORIES = [ INVERT_CAT, POSEMO, NEGEMO ]


''' ------------------------- '''
'''   DEFINE LIWC OBJECT      '''
''' ------------------------- '''
class LIWCObj:

   def __init__(self):
      self.cat = {} # cat_id -> cat_name
      self.wordFull = {} # word* -> list(cat_id)
      self.wordRoot = {} # word* -> list(cat_id)

   ''' TODO 
      @input modelpath:
      @output 
      '''
   def load_model(self, modelpath):
      ads = pickle.load( open( modelpath, "rb" ) )


   ''' Build model from LIWC dictionary file.
      @input ifilepath: LIWC dictionary file path 
      @output: categories and words dictionaries
      '''
   def build_model(self, ifilepath):
      reading_cats = -1
      for line in open(ifilepath, 'r'):
         if line[0] == '%':
            reading_cats += 1
            continue
         #~ if reading_cats == 0 then we are reading categories
         b = line.strip().split('\t')
         #~ loading categories
         if reading_cats == 0:
            cId = int( b[0] )
            if cId in CATEGORIES:
               self.cat[ cId ] = b[1]
         else: #~ loading words
            w = b[0]
            catList = []
            for i in range(1,len(b)):
               #~ check if it contains '<of>131/125'
               if ')' in b[i]:
                  b[i] = b[i].split(')')[1]
               if '/' in b[i]:
                  two = b[i].replace('<of>', '').split('/')
                  cid = int(two[0])
                  if self.cat.has_key(cid):
                     catList.append( cid )
                  cid = int(two[1])
                  if self.cat.has_key(cid):
                     catList.append( cid )
               else:
                  cid = int(b[i])
                  if self.cat.has_key(cid):
                     catList.append( cid )
            # add the word in the correct dictionary
            if w.endswith('*'):
               self.wordRoot[ w.replace('*','') ] = catList 
            else:
               self.wordFull[ w ] = catList 
            #
         #
      #
      return len(self.cat), len(self.wordFull)+len(self.wordRoot)

   ''' Given a category, negate it if it is a sentiment.
      '''
   def polaritySwap(self, cat):
      if cat == 126:
         return 127
      if cat == 127:
         return 126
      else:
         return cat

   ''' Retrieve categories of a given text: 
      averaging the emotions for each sentence.
      @input: text
      @params: require stopwords removal and stemming   NOT SUPPORTED
      @output: dictionary with category frequency
      '''
   def getCategoriesFromText(self, text):
      overall_sent = { 'posemo': 0, 'negemo': 0 }
      # sentence pre-processing
      sentences2words = tokenize2sentences2words( text )
      #
      for sentence in sentences2words:
         sent = self.getCategoriesFromSentence( sentence )
         for emo in overall_sent:
            overall_sent[ emo ] += sent[ emo ]
         #
      # 
      return overall_sent


   ''' Retrieve categories of a given sentence.
      @input: text
      @params: require stopwords removal and stemming   NOT SUPPORTED
      @output: dictionary with category frequency
      '''
   def getCategoriesFromSentence(self, l_words, verbose=False):
      cats = { POSEMO: 0, NEGEMO: 0, INVERT_CAT: 0}
      negation = False
      # tokenize if it is a string
      if type(l_words) == str:
         l_words = tokenize2sentences2words( l_words )[0]
      for i in range(0,len(l_words)):
         w = l_words[ i ]
         # find word in wordFull
         if self.wordFull.has_key( w ):
            for cId in self.wordFull[ w ]:
               # negate category if there was a negation before
               if negation:
                  cId = self.polaritySwap( cId )
               cats[ cId ] += 1
               # if the current category is a negation
               # then change the flag
               negation = True if cId == INVERT_CAT else False
               #
            #
         # find word in wordRoot
         for wr in self.wordRoot:
            if w.startswith( wr ):
               for cId in self.wordRoot[ wr ]:
                  # negate category if there was a negation before
                  if negation:
                     cId = self.polaritySwap( cId )
                  cats[ cId ] += 1
                  # if the current category is a negation
                  # then change the flag
                  negation = True if cId == INVERT_CAT else False
               #
            #
         #
      # compute sentence sentiment
      return { 'posemo': cats[ POSEMO ], 'negemo': cats[ NEGEMO ] }


   ''' Unittest. '''
   def unittest(self):
      failed = 0
      # set test sets
      tests = []
      t = 'This pasta sucks, it is made by shit. I don\'t like this pizza.'
      s = {'posemo': 0, 'negemo': 3}
      tests.append( [t,s] )
      t = 'Questa passata fa schifo!'
      s = {'posemo': 0, 'negemo': 0}
      tests.append( [t,s] )
      t = 'This restaurant has all my love but the food is not good and the service is terrible!'
      s = {'posemo': 1, 'negemo': 2}
      tests.append( [t,s] )
      # evaluate tests
      for test, score in tests:
         emos = {'posemo': 0, 'negemo': 0}
         for sent in tokenize2sentences2words( test ):
            curEmos = self.getCategoriesFromSentence( sent )
            for k in emos:
               emos[k] += curEmos[k]
         #
         if score == emos:
            print 'PASSED - (%s) %s' %(str(score),test)
         else:
            print 'FAILED - (%s) %s' %(str(score),test)
            failed += 1
         #
      #
      return False if failed > 0 else True
      ##
