import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from pattern.en import conjugate, lemma, tag, parse, referenced, lexeme
import urllib3
import requests
from urllib.parse import quote
import json
import string

adjective_ordering={}

with open("adjective_order.json") as f:
	adjective_ordering = json.load(f)

# print(adjective_ordering)

def order_adjectives(sentence,i1,i2):#sentence=list of words, i1,i2= indexes of adj substring
	temp={}
	for adj in sentence[i1:i2]:
		temp[adj]=adjective_ordering[adj]
	sorted_adjs = sorted(temp.items(), key = lambda x:x[1])
	print(sorted_adjs)

try:
	order_adjectives("I bought a red brand new bike".split(),3,6)
except:
	#bigramOrder(sent,i1,i2)
	pass