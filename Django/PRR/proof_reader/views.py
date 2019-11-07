from django.shortcuts import render
from django.views import generic
from nltk.corpus import wordnet
from django.http import JsonResponse
import json
from . import spellchecker	

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'proof_reader/index.html'
    def get_queryset(self):
        wordnet.ensure_loaded()
        # Wordnet incorporates a lazy corpus model, which starts loading
        # only on first call to itself, which can cause some issues with
        # multithreading
        return
        

def processArray(request):
    process_arr = request.GET['process_arr']

    words = process_arr.split(' ')

    suggest = spellchecker.suggestions(words)
    print(suggest)
    
    return JsonResponse({"spell":suggest}, safe=False)