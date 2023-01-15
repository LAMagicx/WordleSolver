from random import choice
from decimal import Decimal as Dec
from itertools import product as P
from math import log
import json

"""
fr
raies 4.3672047
aires 4.319663
tares 4.318756
tarie 4.311094
taies 4.299254
salie 4.2800035
rates 4.2744207
saite 4.268165
sanie 4.2616177
lares 4.258471
en
raise 4.074
slate 4.059
crate 4.044
irate 4.042
trace 4.041
arise 4.035
stare 4.025
snare 4.0
arose 3.998
least 3.987
"""

word_freq = json.loads(open("word_freq.json", "r").readline())
letter_frequency = {'a': 0.08457883369330453, 'b': 0.02427645788336933, 'c': 0.04120950323974082, 'k': 0.01814254859611231, 's': 0.057796976241900645, 'e': 0.10652267818574514, 't': 0.06298056155507559, 'y': 0.0367170626349892, 'o': 0.0651403887688985, 'h': 0.033606911447084234, 'r': 0.07766738660907127, 'i': 0.057969762419006476, 'd': 0.033952483801295896, 'l': 0.06211663066954644, 'u': 0.04034557235421166, 'v': 0.013218142548596112, 'n': 0.04967602591792657, 'g': 0.026868250539956805, 'p': 0.031706263498920084, 'm': 0.027300215982721383, 'f': 0.019870410367170625, 'x': 0.0031965442764578834, 'w': 0.016846652267818573, 'z': 0.0034557235421166306, 'j': 0.002332613390928726, 'q': 0.002505399568034557}

def getWordArray(word, guess):
    a = [0 for _ in range(len(word))]
    for i in range(len(guess)):
        if guess[i] in word:
            if guess.count(guess[i], 0, i+1) <= word.count(guess[i]):
                a[i] = 1
        if i < len(word):
            if guess[i] == word[i]:
                a[i] = 2
    return a

def bestWord(word, words):
    e = E(word, words)
    print("Testing word: " + word + " : " + str(e))
    return {word: e}

def getBestWords(words, all_words):
    scores = {}
    for word in all_words:
        scores.update({word: E(word, all_words)})
        print("Testing word: " + word + " : " + str(round(scores[word],3)))
    print('\n', end="\r")
    #scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

    return scores

def getBestWord(words, all_words, l=5):
    """
    d = {}
    for i in range(l):
        d.update({i:{}})
        for j in 'abcdefghijklmnopqrstuvwxyz':
            d[i].update({j:0})
    for word in words:
        for i in range(l):
            char = word[i]
            d[i][char] += 1
    for i in range(l):
        for key in d[i]:
            d[i][key] = d[i][key]/len(words)
    """
    scores = {}
    for word in all_words:
        scores.update({word: E(word, all_words)})
        print("Testing word: " + word + " : " + str(round(scores[word],3)), end="\r")
    print('\n', end="\r")
    scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    scores_10 = {k:scores[k] for k in list(scores)[:10]}
    for key in scores_10:
        print(key, round(scores_10[key],3))
		#print(key, round(scores_10[key],3), str(round(Dec(word_freq[key]*100),l))+ "%")

    return list(scores.keys())[0]

def splice(words, out_letters, in_letters, regex):
    filtered_words = []
    for word in words:
        add = True
        if len(word) == len(regex):
            for l in out_letters:
                if l in word:
                    add = False
            for i in range(len(regex)):
                if regex[i] not in ' .' and i < len(word):
                    if regex[i] != word[i]:
                        add = False
            for i in range(len(in_letters)):
                if i < len(word):
                    for l in in_letters[i]:
                        if word[i] == l or l not in word:
                            add = False
        else:
            add=False
        if add:
            filtered_words.append(word)

    return filtered_words

def getInfo(word, array):
    not_contains = ''
    contains = ['' for i in range(len(word))]
    positions = list('.'*len(word))

    for i in range(len(word)):
        if array[i] == 0:
            not_contains += word[i]
        elif array[i] == 1:
            contains[i] += word[i]
        elif array[i] == 2:
            positions[i] = word[i]
    return not_contains, contains, positions

def possibleWords(word, words, array):
    not_contains, contains, positions = getInfo(word, array)
    return splice(words, not_contains, contains, ''.join(positions))

def E(word, words):
    all_combinations = list(P([0,1,2], repeat=len(word)))
    score = 0
    for array in all_combinations:
        p = len(possibleWords(word, words, array))/len(words)
        if p != 0:
            score += p * log(1 / p)
    return score


