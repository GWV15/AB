#!/usr/bin/python

# GWV 15/16 Abgabe
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009

# Imports
import sys
import random

# Constants

# Functions


def askForAnswer(cli_arg, first_question, following_question, answers=[]):
    if cli_arg > 1 and len(sys.argv) > cli_arg:
        answer = sys.argv[cli_arg]
    else:
        answer = input(first_question + " (" + "|".join(answers) + ") ")

    # Ask until valid answer is given
    while(answer not in answers):
        answer = input(following_question + " (" + "|".join(answers) + ") ")

    return answer


def askForStart(cli_arg, first_question, following_question, dic):
    if cli_arg > 1 and len(sys.argv) > cli_arg:
        answer = sys.argv[cli_arg]
    else:
        answer = input(first_question + " (word in wordlist) ")

    # Ask until valid answer is given
    while (answer not in dic.keys()):
        answer = input(following_question + " (word in wordlist) ")
    return answer


def buildDictSlow():
    wordlist = [line.rstrip('\n') for line in open(sys.argv[1])]
    wordset = set(wordlist)
    dictionary = {word:[wordlist[min(len(wordlist)-1,wordlist.index(word)+1)]] for word in wordset}
    return dictionary


def builtDict(text_file):
    dictionary = {}
    previous = ""
    for word in open(text_file):
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


# ## Main method ##############################


def main():
    # Load the field
    if len(sys.argv) != 4:
        if len(sys.argv) == 3:
            dic = builtDict(sys.argv[1])
            where_to_begin = random.choice(list(dic.keys()))
            number = int(sys.argv[2])

        else:
            print("Usage: text-file Start-word(optional) Length \n")
            return None
    else:
        dic = builtDict(sys.argv[1])
        where_to_begin = str(sys.argv[2])
        number = int(sys.argv[3])

        # print(sorted(countWords(dic, 'als').items(), key=lambda x: x[1]))

    #where_to_begin = askForStart(2, "Where do you want to start?",
    #                             "This word is not in the wordlist.\
    #                             Choose another.", dic)
    #print("You are starting at ", where_to_begin)

    #number = int(input("How many words should the sentence contain?"))
    #while number > 500 or number < 3:
    #    number = int(input("Again. How many words?"))

    sentence_string = ""
    for word in generateSentence(where_to_begin, number, dic):
        sentence_string = sentence_string + " " + word
    print(sentence_string)

# Run the main method
if __name__ == "__main__":
    main()
