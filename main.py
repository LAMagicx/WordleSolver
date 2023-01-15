from sys import argv
from script import *
from multiprocessing import Pool

words  = [word.strip() for word in open("liste_english.txt", "r").readlines()]
mots = [word.strip() for word in open("liste_francais.txt", "r",encoding='utf-8',errors='ignore').readlines()]


WORDS = words

def best(words, cores=8):
    inputs = []
    for word in words:
        inputs.append([word, words])
    res =  {}
    with Pool(cores) as p:
        res.update(p.starmap(bestWord, inputs))

    res = dict(sorted(res.items(), key=lambda item: item[1]))

    for key in res:
        print(key, res[key])

    getBestWords(words, words)

def solve(words):
    excluded_letters = ''
    included_letters = ['' for i in range(50)]
    positioned_letters = '.....'

    for tries in range(6):
        guess = input("Guess: ")
        while len(guess) == 0 or guess not in words:
            print("not a valid guess\n")
            guess = input("Guess: ")
        array = [int(i) for i in list(input("Array: "))]
        nc, c, p = getInfo(guess, array)

        excluded_letters += nc
        for i in range(len(guess)):
            included_letters[i] += c[i]
        positioned_letters = p

        #print(excluded_letters)
        #print(included_letters)
        #print(''.join(positioned_letters))

        words = splice(words, excluded_letters, included_letters, ''.join(positioned_letters))

        print(' ')
        if words: 
            guess = getBestWord(words, possibleWords(guess, words, array))
            print("Try:   " + guess)
        else:
            print("void")

def play(words):
    word = choice(words)
    excluded_letters = ''
    included_letters = ['' for i in range(50)]
    positioned_letters = '.....'

    for tries in range(6):
        guess = input("Guess: ")
        while len(guess) == 0 or guess not in words:
            print("not a valid guess\n")
            guess = input("Guess: ")

        if guess == word:
            print("you win!")
            break

        array = getWordArray(word, guess)

        nc, c, p = getInfo(guess, array)

        excluded_letters += nc
        for i in range(len(guess)):
            included_letters[i] += c[i]
        positioned_letters = p

        words = splice(words, excluded_letters, included_letters, ''.join(positioned_letters))

        #print(' ')
        #print("array: " + ''.join([str(i) for i in array]))
        if words: 
            guess = getBestWord(words, possibleWords(guess, words, array))
            print("Try:   " + guess)
        else:
            print("void")
    if tries == 5:
        print("the word was: ", word)

if  __name__ == "__main__" :
    if len(argv) > 1:
        for i in range(len(argv)):
            if argv[i] == "-l" :
                if argv[i+1] == "fr":
                    WORDS = mots
                    print("french activated")
        #WORDS = WORDS[:1000]
        if "solve" in argv:
            solve(WORDS)
        elif "play" in argv:
            play(WORDS)
        elif "best" in argv:
            best(WORDS)

    print(E("hello", WORDS))
