import json
from urllib.parse import *
import urllib3
import requests

gram4 = {}
with open('w4_.txt', 'r', encoding='ISO-8859-1') as f:
	lines = f.read().splitlines()
	for line in lines:
		l = line.split('\t')    	
		gram4[' '.join(l[1:])] = int(l[0])

data = []
with open('dict_of_trigrams.json') as f:
    for line in f:
        data.append(json.loads(line))

data = data[0]

def trigram_freq(words):
	trigram = words[0] + ' ' + words[1] + ' ' + words[2]
	try:
		return data[trigram]
	except KeyError:
		return 0


def gram4_freq(words):
	g4 = ' '.join(words)
	try:
		return gram4[g4]
	except KeyError:
		return 0


def ngramFreq(ngram): #ngram is a list of n words
	n = len(ngram)
	ngram = " ".join(ngram)
	encoded_query = quote(ngram)
	params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': n}
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
	return freq


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

def correction3(options): 
	"Most probable spelling correction for word."

	options.sort(reverse=True, key=ngramFreq)
	if(trigram_freq(options[0])==0):
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
