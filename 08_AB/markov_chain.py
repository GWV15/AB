#!/usr/bin/python

# GWV 15/16 Abgabe
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009

# Imports
import sys

# Constants

# Functions


def askForAnswer(cli_arg, firstQuestion, followingQuestion, answers=[]):
    if cli_arg > 1 and len(sys.argv) > cli_arg:
        answer = sys.argv[cli_arg]
    else:
        answer = input(firstQuestion + " (" + "|".join(answers) + ") ")

    # Ask until valid answer is given
    while(answer not in answers):
        answer = input(followingQuestion + " (" + "|".join(answers) + ") ")

    return answer


def askForStart(cli_arg, firstQuestion, followingQuestion, wordlist):
    if cli_arg > 1 and len(sys.argv) > cli_arg:
        answer = sys.argv[cli_arg]
    else:
        answer = input(firstQuestion + " (word in wordlist)")

    # Ask until valid answer is given
    while (answer not in wordlist):
        answer = input(followingQuestion + " (word in wordlist)")

    return answer


# ## Main method ##############################


def main():
    # Load the field
    # Load the field
    if len(sys.argv) >= 2:
        wordlist = [line.rstrip('\n') for line in open(sys.argv[1])]
    else:
        print("There has to be at least one command line argument. \
            It should be a text file containig words.")
        return
    print(sys.argv[1])

    # where_to_begin = askForStart(2, "Where do you want to start",
    #    "This word is not in the wordlist", wordlist)


# Run the main method
if __name__ == "__main__":
    main()
