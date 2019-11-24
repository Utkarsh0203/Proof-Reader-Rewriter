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

lemmatizer = WordNetLemmatizer() 

verb_list=["VB","VBD","VBG","VBN","VBP","VBZ"]
pattern_aliases=["inf","1sg","2sg","3sg","pl","part","p","1sgp","2sgp","3gp","ppl","ppart"]
auxiliary_verbs_base=str(["be","do","have","will","may","might","can","would","shall","should"])

s="The guard is a honest person."
words=s.split()
tags=tag(s)
# print(tags)

trigram="who are you".split()
# trigram_freq={}

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
			print("trying2")
			continue	
	freq = 0
	if bool(response):
		r = response['phrases']
		for i in r:
			freq += i['mc']		
	# print(freq)
	return freq

# def pattern_alias(word):
# 	base_form=lemmatizer.lemmatize(word,wn.VERB)
# 	for alias in pattern_aliases:
# 		if conjugate(base_form,alias)==word:
# 			return alias

def getTrigrams(sentence,word_ind):#sentence is a list of words, returns trigrams in which the given word occurs along with its pos in trigram
	trigrams=[]
	
	t=sentence[word_ind-2:word_ind+1]
	if len(t)==3:
		trigrams.append([t,2])
	t=sentence[word_ind-1:word_ind+2]
	if len(t)==3:
		trigrams.append([t,1])
	t=sentence[word_ind:word_ind+3]
	if len(t)==3:
		trigrams.append([t,0])
	
	return trigrams

def getFourgram(sentence,word_ind):

	return [sentence[word_ind-1:word_ind+3],1]

s="These is very good"
sent=pos_tag(word_tokenize(s))

def tenseChecker(sentence,ind):#sentence is a list of words, ind = index of verb
	trigrams=[]
	fourgrams=[]
	fourgram_freq={}
	b = len(sentence[ind-1:ind+3])>=4
	if b:
		fourgrams=getFourgram(sentence,ind)
	trigram_freq={}
	trigrams=getTrigrams(sentence,ind)
	# print(trigrams)
	for tri,i in trigrams:
		key = tri[i]
		temp = tri
		# print(tri)
		word_tenses=lexeme(key)
		# print(word_tenses)
		for tense in word_tenses:
			temp[i]=tense
			# print(temp)
			if tense in trigram_freq.keys():
				trigram_freq[tense]+=trigramFreq(temp)
				# print(trigramFreq(temp))
			else:
				trigram_freq[tense]=trigramFreq(temp)
	sorted_tenses = sorted(trigram_freq.items(), key = lambda x:x[1], reverse=True)

	for tense in word_tenses:
		temp=fourgrams[0]
		temp[fourgrams[1]]=tense
		if tense in fourgram_freq.keys():
				fourgram_freq[tense]+=trigramFreq(temp)
				# print(trigramFreq(temp))
		else:
			fourgram_freq[tense]=trigramFreq(temp)
	sorted_tenses_4 = sorted(fourgram_freq.items(), key = lambda x:x[1], reverse=True)

	print(sorted_tenses)
	print(sorted_tenses_4)

tenseChecker(s.split(),1)
# tenseChecker(s.split(),2)
# data = []
# with open('ok.json') as f:
#     for line in f:
#         data.append(json.loads(line))
# data = data[0]

# def trigram_freq(words):
# 	trigram = words[0] + ' ' + words[1] + ' ' + words[2]
# 	try:
# 		return data[trigram]
# 	except KeyError:
# 		return 0
# # sugg_sentences is array of array of alternatives, each term represents suggestions for words
# def trigram_suggestions(sugg_sentences):
#     for i in range(1, len(sugg_sentences)-1):
#         a = sugg_sentences[i-1]
#         b = sugg_sentences[i]
#         c = sugg_sentences[i+1]

#         options = []
#         for x1 in range(len(a)):
#         	for x2 in range(len(b)):
#         		for x3 in range(len(c)):
#         			options.append([a[x1], b[x2], c[x3]])
#         print(correction(options))


# def freq(trigram): 
#     return trigram_freq(trigram)

# def correction(options): 
#     "Most probable spelling correction for word."
#     options.sort(key=freq)
#     return options[-1], options[-2], options[-3]
#     # return max(options, key=freq)		