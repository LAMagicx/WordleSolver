from itertools import permutations as P

words  = [word.strip() for word in open("liste_english.txt", "r").readlines()]
mots = [word.strip() for word in open("liste_francais.txt", "r",encoding='utf-8',errors='ignore').readlines()]



