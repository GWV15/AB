#!/usr/bin/python

# GWV 15/16 Abgabe
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009

# Imports
import sys
import random


def getWordList(dic):
    words = []
    for key in dic.keys():
        for word in key.split("#")[1:]:
            words.append(word)
    return words


# Ask for first word
def askForStart(dic, answer=""):
    first_question = "Where do you want to start? (word in txt) "
    following_question = " is not in the wordlist. Choose another. "

    words = getWordList(dic)

    if answer == "":
        answer = input(first_question)

    if answer == "random":
        answer = random.choice(words)

    while (answer not in words) or answer is "":
        answer = input('"' + answer + '"' + following_question)

    return answer


# Ask for number of words
def askForNumber(min, max, init_val=0):
    try:
        word_number = int(init_val)
    except ValueError:
        word_number = 0

    question = "How many words? "
    while word_number > max or word_number < min:
        try:
            word_number = int(input(question))
        except ValueError:
            continue

    return word_number


# Build a dictionary
#
# every word (combination of length ngramlvl) in text_file is a key.
# For each key, value is a list with possible following words
def builtDict(text_file, ngramlvl):
    dictionary = {}

    lastlist = []
    for word in text_file:
        word = word.rstrip('\n')

        # Filter some words out
        if word in []:
            next

        key = genKey(lastlist)
        if key not in dictionary:
            dictionary[key] = [word]
        else:
            dictionary[key].append(word)

        if len(lastlist) >= ngramlvl - 1:
            lastlist.pop(0)

        lastlist.append(word)

    return dictionary


def genKey(wordlist):
    key = ""
    for item in wordlist:
        key = key + "#" + item
    return key


# This is were the magic happens
# generate a sentence (list).
def generateSentence(wstart, ngramlvl, length, dic):
    if 2 < ngramlvl:
        possible_keys = []
        for x in dic.keys():
            if x is '':
                continue
            words = x.split("#")[1:]
            if words[0] == wstart:
                possible_keys.append(words)

        sentence = random.choice(possible_keys)
    else:
        sentence = [wstart]

    while len(sentence) < length or sentence is []:
        key = genKey(sentence[-(ngramlvl-1):])
        if key not in dic:
            sentence = sentence[:-1]
            continue
        sentence.append(random.choice(dic.get(key)))

    return sentence


# Turn the sentence list into a string
# (and make some cosmetic changes)
def buildSentenceString(sentence_list, no_space_list):
    sentence_string = sentence_list[0]
    for word in sentence_list[1:]:
        if word not in no_space_list:
            word = " " + word
        sentence_string = sentence_string + word

    if sentence_string[-1] in no_space_list:
        sentence_string = sentence_string[:-1]

    sentence_string = sentence_string + '.'

    return sentence_string


# Evaluate the arguments given to the program
def evalCmdArg(cmd_list):
    input_file = ""
    ngramlvl = ""
    word_number = ""
    start_word = ""

    # text file needed
    if len(sys.argv) < 3:
        print("The first argument has to be the text file. The second one the n-gram level.")
        sys.exit(2)
    else:
        try:
            input_file = open(sys.argv[1])
        except IOError:
            print("The text file could not be read")
            sys.exit(2)

        try:
            ngramlvl = int(sys.argv[2])
        except ValueError:
            print("The n n-gram lvl could not be read")
            sys.exit(2)

        # one of two optional arguments given
        if len(sys.argv) == 4:
            try:
                word_number = int(sys.argv[3])
            except ValueError:
                # the second argument is not the word number
                start_word = str(sys.argv[3])

        # two of two optional arguments given
        elif len(sys.argv) >= 5:
            try:
                word_number = int(sys.argv[3])
                start_word = str(sys.argv[4])
            except ValueError:
                # the second argument is not the word number
                start_word = str(sys.argv[3])
                word_number = int(sys.argv[4])

    return input_file, ngramlvl, start_word, word_number


# Run the program
#
# Usage:
#  $> markov_chain.py path/to/textfile ngramlvl [NumOfWords] [FirstWord]
#
def main():
    input_file, ngramlvl, start_word, word_number = evalCmdArg(sys.argv)

    dic = builtDict(input_file, ngramlvl)
    start_word = askForStart(dic, start_word)
    word_number = askForNumber(3, 500, word_number)

    sentence_list = generateSentence(start_word, ngramlvl, word_number, dic)
    sentence_string = buildSentenceString(sentence_list, ['.', ',', ';', ':'])
    print(sentence_string)


# Run the main method
if __name__ == "__main__":
    main()
