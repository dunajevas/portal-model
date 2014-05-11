# coding=utf-8
# http://norvig.com/spell-correct.html

import re, collections

def words(text):
    return re.findall('[a-ž]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

from_articles = words(file('dictionaries/dictionary.txt').read())
swear_words = words(file('dictionaries/swear-words.txt').read())
NWORDS = train(from_articles + swear_words)
#NWORDS = train(words(file('data/debug.txt').read()))

alphabet_all = u"aąbcčdeęėfghiįjklmnopqrsštuųūvwxyzž"
alphabet_lt = u"ąčęėįšųūzž"



def edits1(word, alphabet = alphabet_all):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2.encode('utf8') for e1 in edits1(word) for e2 in edits1(e1) if e2.encode('utf8') in NWORDS)

def editsLT(word, alphabet = alphabet_lt):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   return set(replaces)

def known(words):
    return set(w.encode('utf8') for w in words if w.encode('utf8') in NWORDS)

# 1 stage leaves the word if it is known
# 2 stage edits letters by trying modifications with only lithuanian specific symbols without changing length of the word
# 3, 4 stages are all other kind of edits
def correct(word):
    w
    candidates = known([word]) or known(editsLT(word)) or known(edits1(word)) or known_edits2(word) or set[word]
    # debug
    # print candidates
    return max(candidates, key=NWORDS.get)