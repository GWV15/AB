#!/usr/bin/python

# GWV 15/16 Abgabe
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009

# Imports
import sys
import getopt
import random


def askForStart(dic, answer=""):
    first_question = "Where do you want to start? (word in txt) "
    following_question = " is not in the wordlist. Choose another. "

    if answer == "":
        answer = input(first_question)

    while (answer not in dic.keys()) or answer is "":
        answer = input('"' + answer + '"' + following_question)

    return answer


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


def buildDictSlow(text_file):
    wordlist = [line.rstrip('\n') for line in open(text_file)]
    wordset = set(wordlist)

    dictionary = {word: [wordlist[min(len(wordlist) - 1,
                  wordlist.index(word)+1)]] for word in wordset}

    return dictionary


def builtDict(text_file):
    dictionary = {}

    previous = ""
    for word in text_file:
        word = word.rstrip('\n')

        # Filter some words out
        if word in []:
            next

        if previous not in dictionary:
            dictionary[previous] = [word]
        else:
            dictionary[previous].append(word)

        previous = word

    return dictionary


def countWords(dictionary, word):
    wordcount = {}

    for nextword in dictionary.get(word):
        if nextword not in wordcount:
            wordcount[nextword] = 1
        else:
            wordcount[nextword] += 1

    return wordcount


def generateSentence(wstart, length, dic):
    sentence = [wstart]

    while len(sentence) < length:
        sentence.append(random.choice(dic.get(sentence[-1])))

    return sentence


def buildSentenceString(sentence_list, no_space_list):
    sentence_string = sentence_list[0]

    for word in sentence_list[1:]:
        if word not in no_space_list:
            word = " " + word
        sentence_string = sentence_string + word

    if sentence_string[-1] != '.':
        sentence_string = sentence_string + '.'

    return sentence_string


def evalCmdArg(cmd_list):
    input_file = ""
    word_number = ""
    start_word = ""

    # text file needed
    if len(sys.argv) < 2:
        print("The first argument has to be the text file.")
        sys.exit(2)
    else: 
        try:
            input_file = open(sys.argv[1])
        except IOError:
            print("The text file could not be read")
            sys.exit(2)

        # one of two optional arguments given
        if len(sys.argv) == 3:
            try:
                word_number = int(sys.argv[2])
            except ValueError:
                # the second argument is not the word number
                start_word = str(sys.argv[2])

        # two of two optional arguments given
        elif len(sys.argv) >= 4:
            try:
                word_number = int(sys.argv[2])
                start_word = str(sys.argv[3])
            except ValueError:
                # the second argument is not the word number
                start_word = str(sys.argv[2])
                word_number = int(sys.argv[3])

    return input_file, start_word, word_number


def main():
    input_file, start_word, word_number = evalCmdArg(sys.argv)

    dic = builtDict(input_file)
    start_word = askForStart(dic, start_word)
    word_number = askForNumber(3, 500, word_number)

    sentence_list = generateSentence(start_word, word_number, dic)
    sentence_string = buildSentenceString(sentence_list, ['.', ',', ';', ':'])
    print(sentence_string)

# Run the main method
if __name__ == "__main__":
    main()
