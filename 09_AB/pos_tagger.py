#!/usr/bin/python

# GWV 15/16 Abgabe
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009

# Imports
import sys


# Build a dictionary
#
# every word (combination of length ngramlvl) in text_file is a key.
# For each key, value is a list with possible following words
def buildDicts(data_file):
    dict_tags = {}
    dict_words = {}

    prev_tag = '$.'
    for line in data_file:

        word_tag = line.strip().split('\t')
        if len(word_tag) < 2:
            continue

        word = word_tag[0]
        tag = word_tag[1]

        if len(tag) != 0:
            if word not in dict_words:
                dict_words[word] = [tag]
            else:
                dict_words[word].append(tag)

            if prev_tag not in dict_tags:
                dict_tags[prev_tag] = [tag]
            else:
                dict_tags[prev_tag].append(tag)
            prev_tag = tag

    return dict_tags, dict_words


# This is were the magic happens
# generate a sentence (list).
def tagText(text, dict_words, dict_tags):
    tags = ['$.']

    for word in text:
        if word not in dict_words:
            print(word + " not in dictionary. Previous tag: " + tags[-1])
            
            newtag = dict_tags[tags[-1]][0]
            print("Inserting " + newtag + " instead")
            
            tags.append(newtag)

        else:
            tags.append(dict_words[word][0])

    return tags[1:]


# Evaluate the arguments given to the program
def evalCmdArg(cmd_list):
    data_file = ""
    text_file = ""

    # text file needed
    if len(sys.argv) < 2:
        print("Too few arguments. The first argument has to be the data file.\
               The second mey be the text to tag.")
        sys.exit(2)

    try:
        data_file = open(sys.argv[1])
    except IOError:
        print("The data file could not be read")
        sys.exit(2)

    if len(sys.argv) == 3:
        text_file = sys.argv[2]

    if len(sys.argv) > 3:
        print("Too many arguments. The first argument has to be the data file.\
               The second may be the text to tag.")

    return data_file, text_file


def splitText(text):
    words = []
    word = ""

    for char in text.strip():
        if char == ' ':
            words.append(word)
            word = ""
            next
        elif char in ['.', ',', ';', ':', '!', '?']:
            words.append(word)
            word = char
        else:
            word = word + char

    return words


# Run the program
#
# Usage:
#  $> pos_tagger.py path/to/trainingdata "TEXT_TO_TAG"
#
def main():
    data_file, text = evalCmdArg(sys.argv)

    dict_tags, dict_words = buildDicts(data_file)

    words = splitText(text)

    tags = tagText(words, dict_words, dict_tags)

    print(text)
    print(tags)


# Run the main method
if __name__ == "__main__":
    main()
