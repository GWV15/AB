#!/usr/bin/python

# GWV 15/16 Abgabe
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009 

# Imports

# Constants

# Functions

def askForAnswer(cli_arg, firstQuestion, followingQuestion, answers=[]):
	if cli_arg > 1 and len(sys.argv) > cli_arg: answer = sys.argv[cli_arg]
	else: answer = input(firstQuestion + " (" + "|".join(answers) + ") ")
	# Ask until valid answer is given
	while(answer not in answers):
		answer = input(followingQuestion + " (" + "|".join(answers) + ") ")
	return answer

def askForStart(cli_arg, firstQuestion, followingQuestion, wordlist):
	if clie_arg > 1 and len(sys.argv) > cli_arg: answer = sys.argv[cli_arg]
	else: answer = input(firstQuestion + " (word in wordlist)")
	# Ask until valid answer is given
	while (answer not in wordlist):
		answer = input(followingQuestion + " (word in wordlist)"
	return answer

def main():
	# Load the field
	if len(sys.argv) >= 2: field = [list(line.rstrip('\n')) for line in open(sys.argv[1])]
	else:
		print("There has to be at least one command line argument. It should be the wordlist.")
		return
	print(sys.argv[1])

	# Some Info
	print("Number of lines: ", start, searchFor(start,field))

	whereToBegin = askForStart(2, "Where do you want to start", "This word is not in the wordlist", wordlist)

# Run the main method
if __name__ == "__main__":
    main()

