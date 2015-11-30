#!/usr/bin/python

# GWV 15/16 Abgabe
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009

# Imports
import sys

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


def askForStart(cli_arg, first_question, following_question, wordlist):
    if cli_arg > 1 and len(sys.argv) > cli_arg:
        answer = sys.argv[cli_arg]
    else:
        answer = input(first_question + " (word in wordlist)")

    # Ask until valid answer is given
    while (answer not in wordlist):
        answer = input(following_question + " (word in wordlist)")
    return answer


def buildDictSlow(wordlist):
    wordset = set(wordlist)
    dictionary = {word:[wordlist[min(len(wordlist)-1,wordlist.index(word)+1)]] for word in wordset}
    return dictionary

def builtDict(text_file):
    dictionary = {}
    previous = ""
    for word in open(text_file):
        word = word.rstrip('\n')

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


# ## Main method ##############################


def main():
    # Load the field
    if len(sys.argv) < 2:
        print("There has to be at least one command line argument. \
            It should be a text file containig words.")
        return None
    else:
        wordlist = [line.rstrip('\n') for line in open(sys.argv[1])]
        dic = builtDict(sys.argv[1])
        print(sorted(countWords(dic, 'als').items(), key=lambda x: x[1]))

    where_to_begin = askForStart(2, "Where do you want to start?",
        "This word is not in the wordlist. Choose another.", data)
    print("You are starting at ", where_to_begin)

# Run the main method
if __name__ == "__main__":
    main()
