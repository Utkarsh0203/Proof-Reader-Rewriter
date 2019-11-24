from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer 
from pattern.en import conjugate,lemma,lemexe
import json
print("ok")
  
lemmatizer = WordNetLemmatizer() 


slang=[machau,infi]#iitb slang
references=[[talented],[infinite]]#corresponding LISTS of english references
slang_dict=dict(zip(slang,references))#dictionary of iitb slang

verb_list=["VB","VBD","VBG","VBN","VBP","VBZ"]
stop_words=["be","is","are","do","have","why","what","was","where","who","that","here","there","how","when"]
pattern_aliases=["inf","1sg","2sg","3sg","pl","part","p","1sgp","2sgp","3gp","ppl","ppart"]

def aliasa(word):
	base_form=lemmatizer.lemmatize(word,wn.VERB)
	for alias in pattern_aliases:
		if conjugate(base_form,alias)==word:
			return alias

def synonyms(word): #returns set of synonyms of the word
	
	synonyms=set()
	base_form=word
	alias="nullAlias"

	if word in slang_dict:
		for syn in slang_dict[word]:
			synonyms.add(syn)
		return synonyms

	if is_verb(word):
		base_form=lemmatizer.lemmatize(word,wn.VERB)
		alias=aliasa(word)
	
	for synset in wn.synsets(base_form):
		for syn in synset.lemma_names():	
			if not alias=="nullAlias":				
				synonyms.add(conjugate(syn,alias))
			else:
				synonyms.add(syn)
	
	return synonyms	

def is_verb(word):
	return pos_tag([word])[0][1] in verb_list

	
