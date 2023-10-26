from trie import Trie
from scrabble_statics import *

WORD_DICTIONARY = Trie()
with open('dictionary_v1.txt') as file_handler:
    for line in file_handler:
        if line != '':
            WORD_DICTIONARY.addWord(line.rstrip().upper())

print('READY!')
while True:
    x = input()
    value = WORD_DICTIONARY.searchWord(x.upper())
    print(value)
    WORD_DICTIONARY.searchSuffix(x.upper())