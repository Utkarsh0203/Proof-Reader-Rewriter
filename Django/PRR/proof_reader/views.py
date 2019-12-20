from django.shortcuts import render
from django.views import generic
from nltk.corpus import wordnet
from django.http import JsonResponse
import json
from . import spellchecker,  verbTense, active_passive, make_adj_json, adjective_order, article_checker, pronouns, synonyms
import re

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'proof_reader/index.html'
    def get_queryset(self):
        wordnet.ensure_loaded()
        # Wordnet incorporates a lazy corpus model, which starts loading
        # only on first call to itself, which can cause some issues with
        # multithreading
        return

check2count=0

def processArray(request):
    global check2count  
    process_arr = request.GET['process_arr']
    # check = request.GET['check']
    # print(check)
    # print(process_arr[len(process_arr)-1])
    check = int(process_arr[len(process_arr)-1])
    process_arr = process_arr[0:-1]
    # orig.append(process_arr)
    # print(process_arr)
    words = process_arr.split(' ')


    # if check==3:
    #     for i in range(len(words)-1):
    #         words[i] = re.findall(r'\b(\S+)\b', words[i].lower())[0]
    # else:
    for i in range(len(words)):
        words[i] = re.findall(r'\b(\S+)\b', words[i].lower())[0]

    print("#######################################")
    # print(words)
    # for i in range(len(words)):
    #     words[i] = words[i]
    suggest=[]
    if check==1:
        suggest = spellchecker.main(words)
    elif check==2:
        # check2count+=1
        # print('check2count:', check2count)
        # if check2count==1:
        #     print('article:', words)
        #     suggest = article_checker.article_check(words)
        # elif check2count==2:
        #     suggest = verbTense.main(words)
        # elif check2count==3:
        #     suggest = pronouns.w_sugg(words)

        suggest = article_checker.article_check(words)
    elif check==3:
        suggest = verbTense.main(words)

    elif check==4:
        suggest = pronouns.w_sugg(words)

    elif check==5:
        suggest = synonyms.main(words)
        # for i in range(len(words)):
        #     suggest.append(a[i]+b[i]+c[i])

    # elif check==3:
    #     suggest = punctuation.main(words)
    if check==9:
        suggest = active_passive.active_passive(process_arr)

    # print(suggest)
    
    return JsonResponse({"mat":suggest}, safe=False)