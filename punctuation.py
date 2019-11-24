import nltk, re
from spellchecker_contextual import *

nltk.download('nps_chat')
posts = nltk.corpus.nps_chat.xml_posts()[:10000]

# from pattern.en import tag

def propern(word):
	if (len(known({word}))==0):
		return True
	else:
		return False

def truecase(text):

    truecased_sent = [] # list of truecased sentences
    # apply POS-tagging
    tagged_sent = nltk.pos_tag([word.lower() for word in nltk.word_tokenize(text)])
    # infer capitalization from POS-tags
    normalized_sent = [w.capitalize() if t in ["NNP", "NNPS"] else w for (w,t) in tagged_sent]
    normalized_sent = [w.capitalize() if propern(w) else w for (w,t) in tagged_sent]
    # capitalize first word in sentence
    normalized_sent[0] = normalized_sent[0].capitalize()
    # use regular expression to get punctuation right
    pretty_string = re.sub(" (?=[\.,'!?:;])", "", ' '.join(normalized_sent))
    # return pretty_string
    return pretty_string

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)

def punctuation(line):
	line1 = re.sub("(?<=\S)[\.!?]", "", line)

	sentense_class = classifier.classify(dialogue_act_features(line1))
	if (sentense_class in ["whQuestion", "ynQuestion"]) :
		lineres = re.sub("(?<=\S)[\.!?]+", "?", line)
	# elif (sentense_class=="Statement"):
		# lineres = re.sub("(?<=\S)[\.!?]", ".", line)
	elif (sentense_class in ["Emphasis", "Greet", "Emotion"]):
		lineres = re.sub("(?<=\S)[\.!?]+", "!", line)
	else:
		lineres = re.sub("(?<=\S)[\.!?]+", ".", line)
	return lineres


def main(line):
	a = truecase(line)
	b = punctuation(a)
	return b
