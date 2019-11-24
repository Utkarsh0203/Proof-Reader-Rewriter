# import nltk
from pattern.en import tag
import numpy as np
from ngrams import *


w_word_list=['why','what','when','which','whose','whom','how','where','who']
ds_word_list=['this','that']
dp_word_list=['these','those']

# gram4 = {}
# with open('w4_.txt', 'r', encoding='ISO-8859-1') as f:
# 	lines = f.read().splitlines()
# 	for line in lines:
# 		l = line.split('\t')    	
# 		gram4[' '.join(l[1:])] = int(l[0])

# data = []
# with open('dict_of_trigrams.json') as f:
#     for line in f:
#         data.append(json.loads(line))

# data = data[0]

# def trigram_freq(words):
# 	trigram = words[0] + ' ' + words[1] + ' ' + words[2]
# 	try:
# 		return data[trigram]
# 	except KeyError:
# 		return 0


# def gram4_freq(words):
# 	g4 = ' '.join(words)
# 	try:
# 		return gram4[g4]
# 	except KeyError:
# 		return 0

def w_sugg(sent):
	ret = []
	tagged = [tag(x)[0] for x in sent]
	print(tagged)
	nouns = [i for i in range(len(tagged)) if tagged[i][1][0:2]=='NN']
	print(nouns)
	for i in range(len(sent)):
		if sent[i] in w_word_list:
			if len(sent) <4:
				options = [ [q if x==sent[i] else x for x in sent] for q in w_word_list]
			elif i == len(sent)-1:
				options = [[sent[i-3], sent[i-2], sent[i-1], q] for q in w_word_list]
				options = [ [q if x==sent[i] else x for x in sent] for q in w_word_list]
				ret.append(((np.array(correction4(options)) )[:,1]).tolist())

			elif i == len(sent)-2:
				options = [[sent[i-2], sent[i-1], q, sent[i+1]] for q in w_word_list]
				options = [ [q if x==sent[i] else x for x in sent] for q in w_word_list]
				ret.append(((np.array(correction4(options)) )[:,1]).tolist())
				

			elif i == len(sent)-3:
				options = [[sent[i-1], q, sent[i+1], sent[i+2]] for q in w_word_list]
				ret.append(((np.array(correction4(options)) )[:,1]).tolist())

			else:
				options = [[q, sent[i+1], sent[i+2], sent[i+3]] for q in w_word_list]
				ret.append(((np.array(correction4(options)) )[:,0]).tolist())
			


		elif (sent[i] in ds_word_list) or (sent[i] in dp_word_list):
			closest_noun = -10
			for j in nouns:
				if abs(closest_noun-i)>= abs(j-i):
					closest_noun = j

			if closest_noun!=-10:
				print('yo')

				if ('S' in tagged[closest_noun][1]) and (sent[i] in ds_word_list):
					print('yo')
					ret.append(dp_word_list)
					if sent[i+1] == 'is' or sent[i-1]=='is':
						ret.append(['are'])
				elif 'S' not in tagged[closest_noun][1] and sent[i] in dp_word_list:
					ret.append(ds_word_list)
					if sent[i+1] == 'are' or sent[i-1]=='are':
						ret.append(['is'])
				else:
					ret.append([])
			else:
				if (sent[i] in ds_word_list) and (sent[i+1]=='are' or sent[i-1]=='are'): 
					ret.append(dp_word_list)
				elif (sent[i] in dp_word_list) and (sent[i+1]=='is' or sent[i-1]=='is'):
					ret.append(ds_word_list)
				else:
					ret.append([])
		elif i==len(ret):
			ret.append([])
	
	return ret

def correction4(options): 
	"Most probable spelling correction for word."

	options.sort(reverse=True, key=ngramFreq)
	if(gram4_freq(options[0])==0):
		d = {}
		for x in options:
			d[' '.join(x)] = ngramFreq(x)
		def f(x):
			return d[' '.join(x)]
		options.sort(reverse=True, key=f)

	print(options[0])
	if len(options)<3:
		return options
	else:
		return [options[0], options[1], options[2]]
	# return max(options, key=freq)


##############################################################################################

# def ngramFreq(ngram): #ngram is a list of n words
# 	n = len(ngram)
# 	ngram = " ".join(ngram)
# 	encoded_query = quote(ngram)
# 	params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': n}
# 	params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
# 	# print(params)
# 	response = {}
# 	while True:
# 		try:
# 			# print("trying1")
# 			temp = requests.get('https://api.phrasefinder.io/search?' + params)
# 			assert temp.status_code == 200
# 			response = temp.json()
# 			break
# 		except:
# 			# print("trying2")
# 			continue	
# 	freq = 0
# 	if bool(response):
# 		r = response['phrases']
# 		for i in r:
# 			freq += i['mc']		
# 	return freq
