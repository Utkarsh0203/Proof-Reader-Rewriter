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
from . import ngrams
import concurrent.futures
  
lemmatizer = WordNetLemmatizer() 
threads = [] 
trigram_freq1={}
fourgram_freq={}

s="Who is responsible for completing this product"
slang=["arbit", "bandi", "chamka", "craxxx", "enthu", "farra", "freshie", "fundae", "infi", "junta", "lukhha", "machaxxx", "matka", "nightout", "polt", "rg", "sophie"]
#iitb slang
references=["arbitrary", "girl", "understood", "cracked", "enthusiasm", "fail-grade", "freshman", "tips", "infinite", "public", "free", "cracked", "post-graduate", "nightout", "politics", "relative-grading", "sophomore"]
#corresponding english references
slang_dict=dict(zip(slang,references))#dictionary of iitb slang

verb_list=['VB','VBD','VBG','VBN','VBP','VBZ']
stop_words=["be","is","are","do","have","why","what","was","where","who","that","here","there","how","when"]
ok_pos=["NN","NNS","NNP","NNPS","JJ","JJS","JJR","RBR","RBS","RR",'VB','VBD','VBG','VBN','VBP','VBZ']
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

def contextOrder(sentence,ind, f=ngrams.trigram_freq):#sentence is a list of words, ind = index of word
	global threads
	trigrams=[]
	fourgrams=[]
	fourgrams=getFourgrams(sentence,ind)
	if fourgrams:
		for four,i in fourgrams:
			key = four[i]
			temp = four
			# print(tri)
			syns=synonyms(key)
			# print(word_tenses)
			for syn in syns:
				temp[i]=syn
				# print(temp)
    			# print(return_value)
				t=threading.Thread(target=threadOutput, args=(f,temp,syn,False, ))
				# trigram_freq1[syn]+=t
				t.daemon=True
				threads.append(t)
				t.start()
				# print(trigramFreq(temp))
			for thread1 in threads:
				thread1.join()

		sorted_tenses = sorted(fourgram_freq.items(), key = lambda x:x[1], reverse=True)
		# print(sorted_tenses)
		if(sorted_tenses[0][1]==0):
			return contextOrder(sentence, ind, ngrams.ngramFreq)
		else:
			return [x for x,q in sorted_tenses]
	else:
		for tri,i in trigrams:
			key = tri[i]
			temp = tri
			# print(tri)
			syns=synonyms(key)
			# print(word_tenses)
			for syn in syns:
				temp[i]=syn
				# print(temp)
    			# print(return_value)
				t=threading.Thread(target=threadOutput, args=(f,temp,syn,False, ))
				# trigram_freq1[syn]+=t
				t.daemon=True
				threads.append(t)
				t.start()
				# print(trigramFreq(temp))
			for thread1 in threads:
				thread1.join()

		sorted_tenses = sorted(trigram_freq1.items(), key = lambda x:x[1], reverse=True)
		# print(sorted_tenses)
		if(sorted_tenses and sorted_tenses[0][1]==0):
			return contextOrder(sentence, ind, ngrams.ngramFreq)
		else:
			return [x for x,q in sorted_tenses]

def threadOutput(f,tri,syn,tof):#tof=> three not 4
	if tof:
		if syn in trigram_freq.keys():
			trigram_freq[syn]+=f(tri)
				# print(trigramFreq(temp))
		else:
			trigram_freq[syn]=f(tri)
	else:
		if syn in fourgram_freq.keys():
			fourgram_freq[syn]+=f(tri)
				# print(trigramFreq(temp))
		else:
			fourgram_freq[syn]=f(tri)

def main(sentence):
	global trigram_freq
	global fourgram_freq
	remove=[]
	tags=pos_tag(sentence)
	print(tags)
	out = [[] for tag in tags]
	for i in range(len(tags)):
		# print(i)
		if tags[i][1] in ok_pos and tags[i][0] not in stop_words:
			f = contextOrder(sentence,i)
			# remove.append(tags[i][0])
			print(f)
			if f:
				f.remove(tags[i][0])
				# print(f,"OK")
			# a = [suggestion for suggestion,f in sorted(f, key = lambda x:x[1], reverse=True)]
			out[i]=f[:6]
			# out[i]
			threads = []
			trigram_freq = {}
			fourgram_freq = {}
			
			i+=1
	# print(out)
	# print(remove)
	return out

# print(contextOrder(s.split(),4))