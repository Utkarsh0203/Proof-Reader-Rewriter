"""Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html
Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php
"""

import re
from collections import Counter
from nltk.corpus import words as wordlist
aa = wordlist.words()

def words(text): return re.findall(r'\S+', text.lower())

WORDS = Counter(words(open('dictionary_lower.txt').read()))

def candidates(word):
    "Generate possible spelling corrections for word."
    a = list(known([word]) or known(edits1(word)) or known(edits2(word)) or (set([word])))
    if ((len(a) is 1) and (a[0] in WORDS)):
        return []
    else:
        return a

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def suggestions(sentence):
    arr_suggestions = []
    for word in sentence:
        processed_word = re.findall(r'\b(\S+)\b', word.lower())
        arr_suggestions.append(candidates(processed_word[0]))

    return arr_suggestions
