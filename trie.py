from trie_node import TrieNode
from trie_leaf import TrieLeaf
from scrabble_statics import wordValue, charIndex

class Trie:

    # Initiate Tree: started with just a single root node
    def __init__(self):
        self.root = TrieNode()
    
    # Insert the value of a Suffix (which is a Trie of prefix letters in backward order)
    def insertSuffix(self, node, prefix_and_value):
        if node.suffix is None:
            node.suffix = TrieNode()
        self.recurseAddWord(0, prefix_and_value[0][::-1], None, 0, node.suffix, self.insertValue, prefix_and_value[1])
    
    def insertValue(self, node, value):
        node.value = value
    
    # Insert all the suffixes of a word to the Suffix Tree
    def addWord(self, word):
        # Insert the full word
        self.recurseAddWord(0, word, None, 0, self.root, self.insertValue, wordValue(word))

        # Insert the suffixes
        for i in range(1, len(word)):
            self.recurseAddWord(0, word[i:], None, 0, self.root, self.insertSuffix, (word[:i], wordValue(word)))
    
    # Insert a new node and continue spanning other node until the suffix ends
    def recurseAddWord(self, index, word, parent_node, parent_node_index, current_node, insertFunction, insert_value):
        subword_index = 0
        subword = current_node.subword + ','
        wordp = word + '.'

        # Iterate for every element in the subword
        while subword[subword_index] == wordp[index]:
            subword_index += 1
            index += 1
        difference = subword[subword_index] + wordp[index]
        
        # If finish at the same time: insert the value of word/suffix
        if difference == ',.':
            insertFunction(current_node, insert_value)
        
        # If the current_node subword is finished successfully
        elif difference[0] == ',':
            # If current_node is a leaf: make a new leaf containing the rest of the subword of the inserted word
            if current_node.isLeaf():
                # Creating the new node and copy current_node's content to it
                new_node = TrieNode(subword=current_node.subword, value=current_node.value)
                new_node.suffix = current_node.suffix

                # The current_node becomes a leaf with value of the inserted subword
                current_node.suffix = None
                current_node.value = -1
                current_node.subword = word[index + 1:]
                insertFunction(current_node, insert_value)

                # Repoint the references
                new_node.nodes[charIndex(word[index])] = current_node
                parent_node.nodes[parent_node_index] = new_node
            
            # If current_node is not a leaf
            else:
                prefix_char_index = charIndex(word[index])

                # If the current_node's node does not exist: make a leaf
                if current_node.nodes[prefix_char_index] is None:
                    current_node.nodes[prefix_char_index] = TrieLeaf(word[index + 1:])
                    insertFunction(current_node.nodes[prefix_char_index], insert_value)

                # If current_node's node exist: search next node
                else:
                    self.recurseAddWord(index + 1, word, current_node, prefix_char_index, current_node.nodes[prefix_char_index], insertFunction, insert_value)
        
        # If the word is finished successfully: create a new node between current node & its parent & give that new node value of the inserted word
        elif difference[1] == '.':
            # Creating the new node & giving it word's value
            new_node = TrieNode(subword=current_node.subword[:subword_index])
            insertFunction(new_node, insert_value)
            
            # Repoint the references
            new_node.nodes[charIndex(current_node.subword[subword_index])] = current_node
            current_node.subword = current_node.subword[subword_index + 1:]
            parent_node.nodes[parent_node_index] = new_node
        
        # If the value of difference is anything else, it means the current node & word matches different letter: split current node into 2, 1 contains leaf of current word, the other 1 contains the rest of the current node
        else:
            # Creating the new node
            new_node = TrieNode(subword=current_node.subword[:subword_index])

            # Moving the current node to be the new node's child
            new_node.nodes[charIndex(current_node.subword[subword_index])] = current_node
            current_node.subword = current_node.subword[subword_index + 1:]

            # Creating the new leaf containing the newly inserted word value
            new_leaf = TrieLeaf(word[index + 1:])
            insertFunction(new_leaf, insert_value)

            # Moving the new leaf to be the new node's other child
            new_node.nodes[charIndex(word[index])] = new_leaf

            # Moving parent to point to the new node instead of the current node
            parent_node.nodes[parent_node_index] = new_node
    
    # Search if the word exists (main)
    def searchWord(self, word):
        return self.recurseSearchWord(word, 0, self.root)
    
    # Search if the word exists (recursive)
    def recurseSearchWord(self, word, index, current_node):
        subword_index = 0
        subword = current_node.subword + ','
        wordp = word + '.'

        # Iterate for every element in the subword
        while subword[subword_index] == wordp[index]:
            subword_index += 1
            index += 1
        difference = subword[subword_index] + wordp[index]

        # If word's node is found: return its value
        if difference == ',.':
            return current_node.value
        
        # If the current_node subword is finished successfully, go to next node
        elif difference[0] == ',':
            # If leaf then next node doesn't exist so return -2 (indicating not found)
            if current_node.isLeaf():
                return -2
            
            # Otherwise
            else:
                prefix_char_index = charIndex(word[index])

                # If the current_node's node not exist, means not found
                if current_node.nodes[prefix_char_index] is None:
                    return -2

                # If current_node's node exist: go to next node
                else:
                    return self.recurseSearchWord(word, index + 1, current_node.nodes[prefix_char_index])
        
        # If difference consist of different letters or contains '.', it means the word is not found
        else:
            return -2
    
    # Instead of getting the value of the word, gets the node object instead (main)
    def searchWordNode(self, word, start_node):
        return self.recurseSearchWordNode(word, 0, start_node)
    
    # Gets the node object of a word (recursive)
    def recurseSearchWordNode(self, word, index, current_node):
        subword_index = 0
        subword = current_node.subword + ','
        wordp = word + '.'

        # Iterate for every element in the subword
        while subword[subword_index] == wordp[index]:
            subword_index += 1
            index += 1
        difference = subword[subword_index] + wordp[index]

        # If word's node is found: return its node & subword index (to check if the word exists or just part of the subword of the node)
        if difference == ',.':
            return current_node, subword_index
        
        # If the current_node subword is finished successfully, go to next node
        elif difference[0] == ',':
            # If leaf then next node doesn't exist
            if current_node.isLeaf():
                return None, -1
            
            # Otherwise
            else:
                prefix_char_index = charIndex(word[index])

                # If the current_node's node not exist, means not found
                if current_node.nodes[prefix_char_index] is None:
                    return None, -1

                # If current_node's node exist: go to next node
                else:
                    return self.recurseSearchWordNode(word, index + 1, current_node.nodes[prefix_char_index])
        
        # If word finished successfully: return the node & its subword index
        elif difference[1] == '.':
            return current_node, subword_index
        
        # If difference consist of different letters it means the word's node doesn't exist
        else:
            return None, -1
    
    # Get the next/child node given a current node & a letter
    def searchNextNode(self, letter, node, subword_index):
        # If already at the end of subword: go to next node if possible
        if subword_index == len(node.subword):
            letter_index = charIndex(letter)

            # If node is a leaf, there is no next node
            if node.isLeaf() or node.nodes[letter_index] is None:
                return None, -1
            
            # Return next node & start the index back at 0
            return node.nodes[letter_index], 0
        
        # If subword not end yet but the current letter matches: just add the index & return the same node
        elif node.subword[subword_index] == letter:
            return node, subword_index + 1
        
        # Return None if the letter in the subword didn't match
        return None, -1
    
    # Print all the words (just the prefix) of a given suffix for testing purposes (main)
    def searchSuffix(self, word):
        return self.recurseSearchSuffix(word, 0, self.root)
    
    # Print all the words (just the prefix) of a given suffix for testing purposes (recursive)
    def recurseSearchSuffix(self, word, index, current_node):
        subword_index = 0
        subword = current_node.subword + ','
        wordp = word + '.'

        # Iterate for every element in the subword
        while subword[subword_index] == wordp[index]:
            subword_index += 1
            index += 1
        difference = subword[subword_index] + wordp[index]

        # If word's node is found
        if difference == ',.':
            wordlist = []

            # If it has suffix, perform DFS
            if current_node.suffix is not None:
                self.depthFS(current_node.suffix, '', wordlist)
            print(wordlist)
        
        # If the current_node subword is finished successfully, go to next node
        elif difference[0] == ',':
            # If leaf then next node doesn't exist
            if current_node.isLeaf():
                return -1
            
            # Otherwise
            else:
                prefix_char_index = charIndex(word[index])

                # If the current_node's node not exist
                if current_node.nodes[prefix_char_index] is None:
                    return -1

                # If current_node's node exist: go to next node
                else:
                    return self.recurseSearchSuffix(word, index + 1, current_node.nodes[prefix_char_index])
        
        # If difference consist of different letters or contains '.', it means the word is not found
        else:
            return -1
    
    # Returns a list containing all subwords contained within a Trie
    def depthFS(self, node, word, wordlist):
        # If leaf: stop recursion
        if node.isLeaf():
            wordlist.append(node.subword[::-1] + word)
            return
        
        # If the node's value is greater than 0, that means the word exists, so add to list
        if node.value > 0:
            wordlist.append(node.subword[::-1] + word)
        
        # Recursion for every letter
        for i in range(26):
            if node.nodes[i] is not None:
                self.depthFS(node.nodes[i], chr(i + 65) + node.subword[::-1] + word, wordlist)