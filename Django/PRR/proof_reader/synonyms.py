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
import threading
from ngrams import *
  
lemmatizer = WordNetLemmatizer() 

s="Who is responsible for completing this product?"
slang=[]#iitb slang
references=[]#corresponding english references
slang_dict=dict(zip(slang,references))#dictionary of iitb slang

verb_list=['VB','VBD','VBG','VBN','VBP','VBZ']
stop_words=["be","is","are","do","have","why","what","was","where","who","that","here","there","how","when"]
pattern_aliases=["inf","1sg","2sg","3sg","pl","part","p","1sgp","2sgp","3gp","ppl","ppart"]

def synonyms(word): #returns set of synonyms of the word
	
	synonyms=set()
	base_form=word
	alias="null"

	if word in slang_dict:
		for syn in slang_dict[word]:
			synonyms.add(syn)
		return synonyms
	if word in stop_words:
		return synonyms

	else:

		if is_verb(word):
			base_form=lemmatizer.lemmatize(word,wn.VERB) #base form has more synonyms
			for a in pattern_aliases:
				if conjugate(base_form,a)==word:
					alias=a
					break
	
		for synset in wn.synsets(base_form):
			for syn in synset.lemma_names():	
				if "_" not in syn:
					if alias!="null":				
						synonyms.add(conjugate(syn,alias))
					else:
						synonyms.add(syn)
	
	return synonyms


def is_verb(word):
	return pos_tag([word])[0][1] in verb_list
	
	
def getTrigrams(sentence,word_ind):#sentence is a list of words, returns trigrams in which the given word occurs along with its pos in trigram
	trigrams=[]
	
	t=sentence[word_ind-2:word_ind+1]
	if len(t)==3:
		trigrams.append([t, 2])
	t=sentence[word_ind-1:word_ind+2]
	if len(t)==3:
		trigrams.append([t, 1])
	t=sentence[word_ind:word_ind+3]
	if len(t)==3:
		trigrams.append([t, 0])
	
	return trigrams

def trigramFreq(trig): #trig is a list of 3 words
	trigram = " ".join(trig)
	encoded_query = quote(trigram)
	params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3}
	params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
	# print(params)
	response = {}
	while True:
		try:
			# print("trying1")
			temp = requests.get('https://api.phrasefinder.io/search?' + params)
			assert temp.status_code == 200
			# print("freq of trigram " + trigram + " is ")
			response = temp.json()
			break
		except:
			# print("trying2")
			continue	
	freq = 0
	if bool(response):
		r = response['phrases']
		for i in r:
			freq += i['mc']		
	# print(freq)
	return freq

def contextOrder(sentence,ind, f=trigram_freq):#sentence is a list of words, ind = index of word
	trigrams=[]
	trigram_freq1={}
	trigrams=getTrigrams(sentence,ind)
	for tri,i in trigrams:
		key = tri[i]
		temp = tri
		# print(tri)
		syns=synonyms(key)
		# print(word_tenses)
		for syn in syns:
			temp[i]=syn
			# print(temp)
			if syn in trigram_freq1.keys():
				trigram_freq1[syn]+=f(temp)
				# print(trigramFreq(temp))
			else:
				trigram_freq1[syn]=f(temp)
	sorted_tenses = sorted(trigram_freq1.items(), key = lambda x:x[1], reverse=True)
	if(sorted_tenses[0][1]==0):
		return contextOrder(sentence, ind, ngramFreq)
	else:
		return [x for x,q in sorted_tenses]

	# print(sorted_tenses)
	# t=sentence
	# t[ind]=sorted_tenses[0]
	# print(t)

print(contextOrder(s.split(),4))