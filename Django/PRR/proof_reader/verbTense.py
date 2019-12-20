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

threads = [] 
trigram_freq1={}
fourgram_freq={}

lemmatizer = WordNetLemmatizer() 

verb_list=["VB","VBD","VBG","VBN","VBP","VBZ"]
modal_verbs=[lemma(verb) for verb in ["is","do","have","can","may","might","shall","should","will","would","must"]]
trigram="who are you".split()


def trigramFreq(trig): #trig is a list of 3 words
	# print(trig)
	trigram = " ".join(trig)
	encoded_query = quote(trigram)
	params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3}
	params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
	# print(params)
	response = {}
	while True:
		try:
			print("trying1")
			temp = requests.get('https://api.phrasefinder.io/search?' + params)
			assert temp.status_code == 200
			print("freq of trigram " + trigram + " is ")
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
	print(freq)
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

def getFourgrams(sentence,word_ind):
	fourgrams=[]

	f=sentence[word_ind-1:word_ind+3]
	if len(f)==4:
		fourgrams.append([f,1])
	f=sentence[word_ind-2:word_ind+2]
	if len(f)==4:
		fourgrams.append([f,2])

	return fourgrams

s="These is very good"
s1="who is responsible for completing this product"
sent=pos_tag(word_tokenize(s))

def tenseChecker(sentence,ind):#sentence is a list of words, ind = index of verb
	global threads
	trigrams=[]
	fourgrams=[]
	fourgrams=getFourgrams(sentence,ind)
	# print("OOOOKKK")
	# print(fourgrams)
	if fourgrams:
		# print("FOUR")
		for four,i in fourgrams:
			key = four[i]
			temp = four
		# print(tri)
			word_tenses=lexeme(key)
		# print(word_tenses)
			for tense in word_tenses:
				temp[i]=tense
			# print(temp)
				t = threading.Thread(target = threadOutput, args = (temp,tense,False, ))
				# t.setDaemon(True)
				t.start()
				threads.append(t)

		for t in threads:
			t.join()

		sorted_tenses_4 = sorted(fourgram_freq.items(), key = lambda x:x[1], reverse=True)
		# print(sorted_tenses_4)
		return sorted_tenses_4

	else:
		# trigram_freq1={}
		# print("THREE")
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
				t = threading.Thread(target = threadOutput, args = (temp,tense,True, ))
				# t.setDaemon(True)
				t.start()
				threads.append(t)
				
		for t in threads:
			t.join()

		sorted_tenses = sorted(trigram_freq1.items(), key = lambda x:x[1], reverse=True)
		# print(sorted_tenses)
		return sorted_tenses
	
def threadOutput(tri,syn,tof):#tof=> three not 4
	if tof:
		if syn in trigram_freq1.keys():
					trigram_freq1[syn]+=trigramFreq(tri)
				# print(trigramFreq(temp))
		else:
			trigram_freq1[syn]=trigramFreq(tri)
	else:
		if syn in fourgram_freq.keys():
					fourgram_freq[syn]+=trigramFreq(tri)
				# print(trigramFreq(temp))
		else:
			fourgram_freq[syn]=trigramFreq(tri)

# tenseChecker(s1.split(),4)
# tenseChecker(s.split(),1)

def main(sentence):
	global trigram_freq1
	global fourgram_freq
	next1 = True
	tags=pos_tag(sentence)
	print(tags)
	out = [[] for tag in tags]
	for i in range(len(tags)):
		if tags[i][1] in verb_list:
			if lemma(tags[i][0]) not in modal_verbs:
				f = tenseChecker(sentence,i)
				print(f)
				a = [suggestion for suggestion,f in sorted(f, key = lambda x:x[1], reverse=True)]
				if a:
					a.remove(tags[i][0])
					out[i]=a[:4]
				
				threads = []
				trigram_freq1 = {}
				fourgram_freq = {}

	for i in range(len(tags)):
		if tags[i][1] in verb_list:
			if lemma(tags[i][0]) in modal_verbs:
				f = tenseChecker(sentence,i)
				print(f)
				a = [suggestion for suggestion,f in sorted(f, key = lambda x:x[1], reverse=True)]
				if a:
					a.remove(tags[i][0])
					out[i]=a[:4]
				
				threads = []
				trigram_freq1 = {}
				fourgram_freq = {}
	
			
	print(out)
	return out



# data = []
# with open('ok.json') as f:
#     for line in f:
#         data.append(json.loads(line))
# data = data[0]

# def trigram_freq1(words):
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