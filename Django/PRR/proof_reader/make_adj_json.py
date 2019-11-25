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

adjective_ordering={}
adjective_ordering[0]=["whole","enough","little","all","few","most","much","some","single","double","several","full","a lot","lot","many"]+ "abundant, considerable, few, extra, multiple, heavy, empty, myriad, many, numerous, substantial, bountiful".split(", ")#quantity
adjective_ordering[1]='''adorable, brand, attractive, alluring, beautiful, bewildered, bright, confident, cheerful, cultured, clumsy, dull, dynamic, disillusioned, elegant, 
	energetic, fair, fancy, filthy, gentle, glamorous, handsome, hurt, ill-mannered, jolly, lovely, magnificent, neat, nervous, pleasant,
 perfect, smiling, splendid, self-assured, thoughtful, tense, timid, upset, vivacious, wonderful, worried, aggressive, ambitious, amused, brave, cruel, 
 combative, co-operative, cowardly, dangerous, diligent, determined, disagreeable, evil, erratic, frank, fearless, friendly, generous, gifted, helpful, 
 harmonious, hesitant, jealous, knowing, kind-hearted, mysterious, naughty, pleasing, placid, punctual, quiet, rigid, successful, sincere, selfish, talented, 
 unbiased, witty, wise, warm, happy, unhappy, cheerful, sad, excited, delighted, angry, afraid, angry, anxious, bad, bored, calm, confused, comfortable, creepy, 
 epressed, disturbed, dominating, deceitful, elated, faithful, fine, frustrated, good, gloomy, horrible, happy, hungry, ill, kind, lively, mature, nice, proud, 
 peaceful, protective, sorrowful, silly, sore, tired, troubled, unwell, unhappy, vengeful, wicked, weary, wrong, zestful'''.split(", ")#quality
adjective_ordering[2]="big, large, colossal, gigantic, huge, miniature, mammoth, tiny, small, petite, tall, thin, great, tiny, long, thick, short".split(", ")#size
adjective_ordering[3]="ancient, modern, brief, early, annual, fast, old, late, rapid, slow, swift, young, annually, monthly, quarterly, fortnightly, weekly, new, latest, up-to-date, second-hand, brand-new".split(", ")#age
adjective_ordering[4]="broad, crooked, circular, distorted, rectangular, spherical, triangular, round, square, flat, hollow, narrow, skinny, wide".split(", ")#shape
adjective_ordering[5]="aqua, black, white, blue, gold, crimson, cyan, red, green, yellow, magenta, orange, pink, turquoise".split(", ")#color
# adjective_ordering[6]=set([])#proper
temp={}

for key,lst in adjective_ordering.items():
	for item in lst:
		# print(item)
		temp[item]=key

with open("adjective_order.json", 'w') as outfile:
	json.dump(temp, outfile)