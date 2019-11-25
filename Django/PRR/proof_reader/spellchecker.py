import json
import re
from collections import Counter

def words(text): return re.findall(r'\S+', text.lower())
WORDS = Counter(words(open('dictionary50k.txt').read()))

with open('dict50k_freq.json', 'r') as fp:
    data_dict = json.load(fp)

def freq_dict(word):
    return data_dict[word]

def candidates(word):
	a = known({word})
	if(len(a)==1):
		return (a)
	else:
		
		b = known(edits1(word).union(edits2(word)))
		# c = known(edits2(word))
		# l1, l2 = len(b), len(c)
		d = [word]
		if (len(b)>=15):
			b = b[:15]

		return (b or d)

	# if (l1<=10):
	# 	if (l2<=5):
	# 		g = set(b).union(set(c))
	# 		return (a or list(g) or d)
	# 	else:
	# 		g = set(b).union(set(c[:5]))
	# 		return (a or list(g) or d)
	# else:
	# 	if (l2<=5):
	# 		g = set(b[:10]).union(set(c))
	# 		return (a or list(g) or d)
	# 	else:
	# 		g = set(b[:10]).union(set(c[:5]))
	# 		return (a or list(g) or d)

def known(words):
	a = set(w for w in words if w in WORDS)
	ab = list(a)
	ab.sort(reverse=True, key=freq_dict)
	return ab

def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def suggestions(sentence):
    arr_suggestions = []
    for word in sentence:
        processed_word = re.findall(r'\b(\S+)\b', word.lower())
        arr_suggestions.append(candidates(processed_word[0]))

    return arr_suggestions

####################################################################################################

data = []
with open('dict_of_trigrams.json') as f:
    for line in f:
        data.append(json.loads(line))
data = data[0]

def trigram_freq(words):
	trigram = words[0] + ' ' + words[1] + ' ' + words[2]
	# trigram = words.join(" ")
	try:
		return data[trigram]
	except KeyError:
		return 0

# sugg_sentences is array of array of alternatives, each term represents suggestions for words
def trigram_suggestions(sugg_sentences):
	returnarr = []
	for i in range(1, len(sugg_sentences)-1):
		a = sugg_sentences[i-1]
		b = sugg_sentences[i]
		c = sugg_sentences[i+1]

		options = []
		for x1 in range(len(a)):
			for x2 in range(len(b)):
				for x3 in range(len(c)):
					options.append([a[x1], b[x2], c[x3]])
		returnarr.append(correction(options))
	return returnarr

def correction(options): 
    options.sort(reverse=True, key=trigram_freq)
    if (len(options)>3):
    	return [options[0], options[1], options[2]]
    else:
    	return options
    # return max(options, key=trigram_freq)

# def trig_sugg(sentence):
# 	if (len(sentence)>2):
# 		a = suggestions(sentence)
# 		return trigram_suggestions(a)
# 	else:
# 		a = suggestions(sentence)
# 		return(a)						###############

def jhc(sentence):
	x = suggestions(sentence)
	a = trigram_suggestions(x)
	b = [{} for i in range(len(sentence))]
	
	for i in range(len(a)):
		t = a[i]

		for j in range(len(t)):
			l0 = t[j][0]
			l1 = t[j][1]
			l2 = t[j][2]
			freq = trigram_freq(a[i][j])
			try:
				b[i][l0]+=freq
			except KeyError:
				b[i][l0]=freq

			try:
				b[i+1][l1]+=freq
			except KeyError:
				b[i+1][l1]=freq

			try:
				b[i+2][l2]+=freq
			except KeyError:
				b[i+2][l2]=freq

	def freqq(word):
		return b[i][word]
	r = []
	for i in range(len(b)):
		r.append(list(b[i].keys()))
		if (len(r[i])==1) and (r[i][0]==sentence[i]):
			r[i]=[]
		else:
			r[i].sort(reverse=True, key=freqq)
			if (len(r[i])>5):
				r[i] = r[i][:5]

	return r

def main(sentence):

	if len(sentence)>2:
		return jhc(sentence)
	else:
		a = suggestions(sentence)
		for i in range(len(a)):
			if (len(a[i])>5):
				a[i] = a[i][:5]
			elif (len(a[i])==1) and (a[i][0]==sentence[0]):
				a[i]=[]
		return a
