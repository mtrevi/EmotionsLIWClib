# -*- coding: utf-8 -*-
"""
Preprocessing text (Tokenizing words and sentences, clean text, removing stopwords, stemming and lemmatization)
__author__ : Michele Trevisiol @trevi
"""

import re
import unicodedata
from nltk import clean_html
from nltk import SnowballStemmer
from nltk import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')



''' Convert from UNICODE to ASCII '''
def toASCII(string):
  return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore')

''' Based on nltk, so the value of the language is compatible 
    with the dictionaries of nltk (e.g., 'english' not 'en')
    @input string:
    @output string with dictionary name '''
def get_language(string):
  languages_ratios = {}
  tokens = wordpunct_tokenize(string)
  words = [word.lower() for word in tokens]
  for language in stopwords.fileids():
    stopwords_set = set(stopwords.words(language))
    words_set = set(words)
    common_elements = words_set.intersection(stopwords_set)
    languages_ratios[language] = len(common_elements) # language "score"
  ## Finally, we only have to get the “key” with biggest “value”:
  return max(languages_ratios, key=languages_ratios.get)

def get_language_langid(string, verbose=False):
  import langid
  ## dictionary
  lang_code = {'en':'english', 'es':'spanish', 'it':'italian', 'fr':'french', 'ru':'russian', 'tr':'turkish', 'no':'norwegian', 'da':'danish', 'fi':'finnish', 'nl':'dutch', 'de':'german', 'pt':'portuguese', 'hu':'hungarian', 'sv':'swedish'}
  ## detect language
  if len(string) == 0:
    return ''
  lang_score = langid.classify(string)
  ## get language code
  if not lang_code.has_key(lang_score[0]):
    if verbose:
       print >> sys.stderr, 'Language not supported: %s' %str(lang_score)
    return ''
  return lang_score[0]

def get_best_language(string, default='english', verbose=False):
  lang = get_language_langid(string, verbose=False)
  if len(lang) <= 2:
    lang = get_language(string)
  if len(lang) <= 2:
    return default
  return lang

def tokenize_string(text,lower=False):
  toker = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)
  return toker.tokenize(text.lower()) if lower else toker.tokenize(text)

def remove_puntuation_hardly(text, lower=False):
  tokenizer = RegexpTokenizer(r'\w+')
  return tokenizer.tokenize(text)

def remove_punctuation(text, lower=False):
  tokens = tokenize_string(text,lower)
  return [w for w in tokens if w not in list(string.puntuation)]

def remove_punctuation_and_number(text, lower=False):
  l_words = tokenize_string(text,lower)
  # punctuation and numbers to be removed
  punctuation = re.compile(r'[-.?!,":;()|0-9]')
  out_words = []
  for word in l_words:
    word = punctuation.sub('', word)
    if len(word) > 0:
       out_words.append(word)
  return out_words

''' Tokenize text into words.
  @input string: string
  @param lower: convert to lowercase or not
  @output: list of words '''
def tokenize2words(string, lower=False, decode='utf-8'):
  if lower:
    return tokenizer.tokenize(string.decode('utf-8').lower())
  else:
    return tokenizer.tokenize(string.decode('utf-8'))

''' Tokenizing (Document to list of sentences. Sentence to list of words.) 
   Tokenizes into sentences, then strips punctuation/abbr, converts to lowercase and tokenizes words'''
def tokenize2sentences2words(str):
  return [word_tokenize(" ".join(re.findall(r'\w+', t, flags = re.UNICODE | re.LOCALE)).lower()) 
    for t in sent_tokenize(str.replace("'", ""))]

''' Removing stopwords. 
   @input l_words: list of words
   @input lang: language
   @output content: outputs list of words '''
def remove_stopwords(l_words, lang=''):
  if len(l_words) == 0:
    return []
  test = ' '.join(l_words)
  ## get language if not defined
  if len(lang) == 0:
    lang = get_best_language(' '.join(l_words))
  ## set english as default if language is not identified
  if len(lang) <= 2:
    lang = 'english'
  ## remove stopwords
  l_stopwords = stopwords.words(lang)
  content = [w for w in l_words if w.lower() not in l_stopwords]
  return content


''' Stem all words with stemmer of type, return encoded as "encoding" '''
def stemming(words_l, type="PorterStemmer", lang="english", encoding="utf8"):
  supported_stemmers = ["PorterStemmer","SnowballStemmer","LancasterStemmer","WordNetLemmatizer"]
  if type is False or type not in supported_stemmers:
    return words_l
  else:
    l = []
    if type == "PorterStemmer":
       stemmer = PorterStemmer()
       for word in words_l:
          l.append(stemmer.stem(word).encode(encoding))
    if type == "SnowballStemmer":
       stemmer = SnowballStemmer(lang)
       for word in words_l:
          l.append(stemmer.stem(word).encode(encoding))
    if type == "LancasterStemmer":
       stemmer = LancasterStemmer()
       for word in words_l:
          l.append(stemmer.stem(word).encode(encoding))
    if type == "WordNetLemmatizer": #TODO: context
       wnl = WordNetLemmatizer()
       for word in words_l:
          l.append(wnl.lemmatize(word).encode(encoding))
    return l