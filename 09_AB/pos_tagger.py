#!/usr/bin/python

# GWV 15/16 Abgabe
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009

# Imports
import sys


# Build a dictionary
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

    print(text)
    for word in text:
        if word not in dict_words:
            print(word + " not in dictionary. Previous tag: " + tags[-1])
            
            #newtag = dict_tags[tags[-1]][0]
            newtag = max(zip((dict_tags[tags[-1]].count(item) for item in set(dict_tags[tags[-1]])), set(dict_tags[tags[-1]])))[-1]
            print("Inserting " + newtag + " instead")
            
            tags.append(newtag)

        else:
            tags.append(findMostProbable(dict_tags, dict_words, word, tags[-1]))

    return tags[1:]


def findMostProbable(dict_tags, dict_words, word, prev_tag):
    wordtags = dict_words[word]
    tagtags = dict_tags[prev_tag]
    freq_word_tag = zip((wordtags.count(item) for item in set(wordtags)), set(wordtags))
    most_word_tag = max(freq_word_tag)
    freq_tag_tag = zip((tagtags.count(item) for item in set(wordtags)), set(wordtags))
    most_tag_tag = max(freq_tag_tag)
    probability_word = most_word_tag[0]/len(wordtags)
    probability_tag = most_tag_tag[0]/len(tagtags)
    
    combinedProbability = [((wordtags.count(tag)/len(wordtags)) * (tagtags.count(tag)/len(tagtags)), tag) for tag in list(set(wordtags) & set(tagtags))]

    print("------\n" + "Looking at word " + word)
    print("Previous Tag: '" + prev_tag + "' has most probable successor with frequency: ")
    print(most_tag_tag)
    print("out of " + str(len(tagtags)) + " possible tag(s)")
    print("Probability based on tag: " + str(probability_tag) + "\n" + "---")

    print("Word '" + word + "' has most probable tag with frequency: ")
    print(most_word_tag)
    print("out of " + str(len(wordtags)) + " possible tag(s)")
    print("Probability based on word: " + str(probability_word) + "\n" + "-------")
    print("Combined probabilities: " + str(combinedProbability) + "\n")

    return max(combinedProbability)[-1]

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

    for word in text.split():
        if word[-1] in ['.', ',', ';', ':', '!', '?']:
            words.append(word[:-1])
            words.append(word[-1])
        else:
            words.append(word)
    if '' in words:
        words.remove('')
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
