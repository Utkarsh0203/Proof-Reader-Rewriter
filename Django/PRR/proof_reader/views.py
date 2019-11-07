from django.shortcuts import render
from django.views import generic
from nltk.corpus import wordnet
from django.http import JsonResponse
import json


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

    print(process_arr[0])
    
    l = {"1":1,"2":2,"3":3}
    m = {"4":4,"5":5,"6":6}
    n = {"7":7,"8":8,"9":9}
    s = [l,m,n]
    sj = json.dumps(s)
    return JsonResponse({"spell":s}, safe=False)