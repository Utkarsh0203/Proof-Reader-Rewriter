from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer 
  
lemmatizer = WordNetLemmatizer() 


slang=[]#iitb slang
references=[]#corresponding LISTS of english references
slang_dict=dict(zip(slang,references))#dictionary of iitb slang

verb_list=['VB','VBD','VBG','VBN','VBP','VBZ']

def synonyms(word): #returns set of synonyms of the word
	
	synonyms=set()
	base_form=word

	if word in slang_dict:
		for syn in slang_dict[word]:
			synonyms.add(syn)
		return synonyms

	if is_verb(word):
		base_form=lemmatizer.lemmatize(word,wn.VERB)

	
	for synset in wn.synsets(base_form):
		for syn in synset.lemma_names():					
			synonyms.add(syn)
	
	return synonyms

def get_trigrams(sentence,word_ind):#sentence is a list of words, returns trigrams in which the given word occurs along with its pos in trigram
	trigrams=[]
	
	t=sentence[word_ind-2:word_ind+1]
	if len(t)==3:
		trigrams.append([a, 2])
	t=sentence[word_ind-1:word_ind+2]
	if len(t)==3:
		trigrams.append([a, 1])
	t=sentence[word_ind:word_ind+3]
	if len(t)==3:
		trigrams.append([a, 0])
	
	return trigrams

#def frequency(trigrams):#finds total freq of trigrams



def is_verb(word):
	return pos_tag([word])[0][1] in verb_list
	
