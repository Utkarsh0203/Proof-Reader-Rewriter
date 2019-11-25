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


s="this is apple."

# print(pos_tag(word_tokenize(s)))

def article_check(sentence):#sentence is a list of words
	
	s = " ".join(sentence)
	words=s.split()
	tags=tag(s)
	# print(tags)

	pos1=[]#positions of NP,NNP
	pos2=[]
	ans1=[]
	ans2=[]

	cnt=0
	b = False #determiner in stack
	f = False #1st NN/JJ/RR seen
	pronoun = False

	for i in range(len(tags)):
		word,pos = tags[i]
		if pos=="PRP$" or pos=="POS" or word=="i":
			pronoun = True

		elif word=="the" or word=="a" or word=="an":
			pos1.append([i,0,0])
			# cnt+=1
			# print(cnt)
			b=True
		elif (pos=="NN" or pos=="NNS" or pos=="NNP" or pos=="NNPS" or pos == "JJ" or pos =="JJR" or pos =="JJS" or pos=="RR" or pos=="RBR" or pos=="RBS"):
			if not pronoun:
				if b:
					if not f:
						pos1[cnt][1]=i
						pos1[cnt][2]=pos
						cnt+=1
						f=True
					if pos=="NN" or pos=="NNS" or pos=="NNP" or pos=="NNPS":
						b=False
						f=False
				else:
					pos2.append([i,pos])
			else:
				pronoun=False

	# print("pos1",pos1)
	# print("pos2",pos2)

	adj=False
	adject=False
	first=True
# insertPos=False

	for indDT,indN,pos in pos1:
		word  = tags[indN][0]
		dt=referenced(word).split()[0]
		DT=aORthe(dt,word)
		ans1.append([indDT,indN,DT])
		# if pos=="JJ" or pos=="JJR" or pos =="JJS" or pos=="RR" or pos=="RBR" or pos =="RBS":
		# 	if first:
		# 		# insertPos=indN-1
		# 		adj=pos
		# 		adject=word
		# 		first=False

		# if pos=="NN":
		# 	if adj=="JJS" or adj=="RBS":
		# 		# dt=referenced(tags[indN][0])
		# 		ans1.append([indDT,indN,"the"])
		# 		adj=False
		# 		first=True
		# 		adject=False
		# 	elif adj=="JJ" or adj=="JJR" or adj=="RBR" or adj=="RR":
		# 		dt=referenced(adject).split()[0]
		# 		DT=aORthe(dt,adject)
		# 		ans1.append([indDT,indN,DT])
		# 		adj=False
		# 		first=True
		# 		adject=False
		# 	else:
		# 		dt=referenced(word).split()[0]
		# 		DT=aORthe(dt,word)
		# 		ans1.append([indDT,indN,DT])
		# 		adj=False
		# 		first=True
		# 		adject=False

	adj=False
	adject=False
	first=True
	insertPos=False

	for indN,pos in pos2:
		word  = tags[indN][0]
		if pos=="JJ" or pos=="JJR" or pos =="JJS":
			if first:
				insertPos=indN
				adj=pos
				adject=word
				first=False

		elif pos=="NN":
			if adj=="JJS" or adj=="RBS":
				# dt=referenced(tags[indN][0])
				ans2.append([insertPos,indN,"the"])
				adj=False
				first=True
				adject=False
			elif adj=="JJ" or adj=="JJR" or adj=="RBR" or adj=="RR":
				dt=referenced(adject).split()[0]
				DT=aORthe(dt,adject)
				ans2.append([insertPos,indN,DT])
				adj=False
				first=True
				adject=False
			else:
				dt=referenced(word).split()[0]
				DT=aORthe(dt,word)
				ans2.append([insertPos,indN,DT])
				adj=False
				first=True
				adject=False



	s1=""
	for ws in words:
		s1=s1+ws+" "

	# print("replace: (insertPos,-,dt)")
	# print(ans1)
	aans1=[[] for word in sentence]
	for insertPos,nounPOS,dt in ans1:
		aans1[insertPos]=dt
	# print(aans1)
	# print("insert: (insertPos,-,dt)")
	aans2=[[] for word in sentence]
	for insertPos,nounPOS,dt in ans2:
		# print(insertPos, nounPOS, dt)
		# print(insertPos==False)
		if not insertPos:
			aans2[nounPOS]=[dt1+" "+words[nounPOS] for dt1 in dt]
		else:
			aans2[insertPos]=[dt1+" "+words[insertPos] for dt1 in dt]

	# print(aans2)
	# print(aans1)
	f_ans = []
	for i in range(len(aans2)):
		f_ans.append(aans2[i]+aans1[i])

	return f_ans



#if noun is improper, it needs to have an article, suggestions: reference, the
##how to decide between the/a? check bigram frequency: if "the" is more, substitute
#

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

def aORthe(dt,word):# compare freq of "the word" and "dt word", returns decreasing tuple
	if trigramFreq(("the"+word).split())>trigramFreq((dt+word).split()):
		return ["the",dt]
	else:
		return [dt]

def massNoun(noun):#returns true if noun is uncountable
	return False


