from squares import Squares

class Game:

    # Find the possible tile to place of a given square
    def findOneLetterCandidates(self, row, col, best):
        row_candidates = set()
        column_candidates = set()
        previous_letter = ''
        
        # For every tile in bot's rack
        for tile in self.bot_tiles:
            if tile is not None and tile.letter != previous_letter:
                previous_letter = tile.letter
                
                # Put the tile into the board
                self.scrabble_board[row][col].botAssignTile(tile)
                self.temp_tiles[0] = tile

                # Check if the word made is a valid candidate both vertically & horizontally
                horizontal_word = self.getWordHorizontal(row, col)
                vertical_word = self.getWordVertical(row, col)
                horizontal_score = self.getWordScore(horizontal_word)
                vertical_score = self.getWordScore(vertical_word)

                # If the word made is valid both horizontally & vertically
                if horizontal_score >= 0 and vertical_score >= 0:
                    score = horizontal_score + vertical_score
                    
                    # Update the score & configuration to be made if finding new top score
                    if score > best['score']:
                        best['score'] = score
                        best['config'] = tuple(self.temp_tiles)
                        best['position'] = [tile.square.getCoordinate() for tile in self.temp_tiles]

                        # Some logging on updated best score
                        cstr = ''
                        for conf in best['config']:
                            if conf is not None:
                                cstr += ('[' + conf.letter + ':' + str(conf.square.getCoordinate()) + '] ')
                        print(cstr)
                        print('score:', best['score'])
                        print('h, v:', horizontal_word + ',' + vertical_word)
                        print('-------------')
                
                # If vertically the word is valid & horizontally it is a suffix of other words: add tile to row candidate
                if horizontal_score >= -1 and vertical_score >= 0:
                    row_candidates.add(previous_letter)
                
                # If horizontally the word is valid & vertically it is a suffix of other words: add tile to column candidate
                if horizontal_score >= 0 and vertical_score >= -1:
                    column_candidates.add(previous_letter)
                
                # remove the previously added tile to go back to original board state
                self.scrabble_board[row][col].botRemovetile()
        
        return row_candidates, column_candidates
            
    # To check if the tiles placed in the board is at least attached to another 1 already placed tile in the board
    def checkAttached(self, row, col, visited):
        if (row, col) in visited or row < 0 or row > 14 or col < 0 or col > 14 or not self.scrabble_board[row][col].hasTile():
            return False
        if self.scrabble_board[row][col].letter_tile.isLocked():
            return True
        visited.add((row, col))
        if self.checkAttached(row + 1, col, visited) or self.checkAttached(row - 1, col, visited) or self.checkAttached(row, col + 1, visited) or self.checkAttached(row, col - 1, visited):
            return True
        return False
    
    # Finding all candidate 1 tile moves to be made (main function)
    def findAllCandidates(self, row, col, best):
        # Candidates of row, column
        candidates = [{}, {}]
        self.temp_tiles.append(None)
        self.findAllCandidatesRecurse(row, col, set(), candidates, best)
        self.resetTempTile()
        return candidates
    
    # Finding all candidate 1 tile moves to be made (recursive function)
    def findAllCandidatesRecurse(self, row, col, visited, candidates, best):
        if (row, col) in visited or row < 0 or row > 14 or col < 0 or col > 14:
            return
        visited.add((row, col))

        # If the square is empty: check the possible tiles to cover it
        if not self.scrabble_board[row][col].hasTile():
            row_candidates, column_candidates = self.findOneLetterCandidates(row, col, best)
            candidates[0][(row, col)] = row_candidates
            candidates[1][(row, col)] = column_candidates
            return
        
        # Search the board to the left, right, top, and bottom
        self.findAllCandidatesRecurse(row + 1, col, visited, candidates, best)
        self.findAllCandidatesRecurse(row - 1, col, visited, candidates, best)
        self.findAllCandidatesRecurse(row, col + 1, visited, candidates, best)
        self.findAllCandidatesRecurse(row, col - 1, visited, candidates, best)
    
    # Find horizontal words backwards (reverse Trie search)
    def findAllWordsHorizontalBefore(self, row, col, candidates, word_node_and_index, best):
        if col < 0 or self.scrabble_board[row][col].hasTile() or (row, col) in candidates:
            return False

        previous_letter = ''
        one_update = False
        for i in range(7):
            if self.bot_tiles[i] is not None and self.bot_tiles[i].letter != previous_letter:
                # Place the tile into the board
                self.scrabble_board[row][col].botAssignTile(self.bot_tiles[i])
                
                # Get the next node that goes to the current bot tile letter
                word_node, node_subword_index = self.word_dictionary.searchNextNode(self.bot_tiles[i].letter, *word_node_and_index)

                # If the next node is find
                if word_node is not None:

                    # Place the tile into the board & remove it from the bot's rack
                    self.temp_tiles.append(self.bot_tiles[i])
                    self.bot_tiles[i] = None

                    # Search possible backward tile to be placed
                    updated = self.findAllWordsHorizontalBefore(row, col - 1, candidates, (word_node, node_subword_index), best)
                    
                    # If there isn't any update going on further recursion, then do this, otherwise, prune
                    if not updated:
                        # Find the vertical scores
                        score2, wrd = self.getWords(self.getWordVertical)
                        
                        if score2 >= 0:
                            # Do this if horizontal word is valid
                            if word_node.value > 0 and len(word_node.subword) == node_subword_index:
                                # Get horizontal score
                                bgws = self.botGetWordScore(word_node.value)
                                
                                score = bgws + score2

                                # Update if its the new highscore
                                if score > best['score']:
                                    best['score'] = score
                                    best['config'] = tuple(self.temp_tiles)
                                    best['position'] = [tile.square.getCoordinate() for tile in self.temp_tiles]
                                    one_update = True

                                    # Logging the updated move configuration
                                    cstr = ''
                                    for conf in best['config']:
                                        if conf is not None:
                                            cstr += ('[' + conf.letter + ':' + str(conf.square.getCoordinate()) + '] ')
                                    print(cstr)
                                    print('score:', score)
                                    print('ori:', word_node.value)
                                    print('s1:', bgws)
                                    print('s2:', score2)
                                    print(wrd)
                                    print('-------------')
                    else:
                        one_update = True
                    
                    # Return tile to rack
                    self.bot_tiles[i] = self.temp_tiles.pop()
                    
                # Remove tile from board
                self.scrabble_board[row][col].botRemovetile()
        return one_update
    
    # Find vertical words backwards (Trie search)
    def findAllWordsVerticalBefore(self, row, col, candidates, word_node_and_index, best):
        if row < 0 or self.scrabble_board[row][col].hasTile() or (row, col) in candidates:
            return False

        previous_letter = ''
        one_update = False
        for i in range(7):
            if self.bot_tiles[i] is not None and self.bot_tiles[i].letter != previous_letter:
                self.scrabble_board[row][col].botAssignTile(self.bot_tiles[i])
                word_node, node_subword_index = self.word_dictionary.searchNextNode(self.bot_tiles[i].letter, *word_node_and_index)
                if word_node is not None:
                    self.temp_tiles.append(self.bot_tiles[i])
                    self.bot_tiles[i] = None
                    updated = self.findAllWordsVerticalBefore(row - 1, col, candidates, (word_node, node_subword_index), best)
                    if not updated:
                        score2, wrd = self.getWords(self.getWordHorizontal)
                        if score2 >= 0:
                            if word_node.value > 0 and len(word_node.subword) == node_subword_index:
                                bgws = self.botGetWordScore(word_node.value)
                                score = bgws + score2
                                if score > best['score']:
                                    best['score'] = score
                                    best['config'] = tuple(self.temp_tiles)
                                    best['position'] = [tile.square.getCoordinate() for tile in self.temp_tiles]
                                    one_update = True

                                    cstr = ''
                                    for conf in best['config']:
                                        if conf is not None:
                                            cstr += ('[' + conf.letter + ':' + str(conf.square.getCoordinate()) + '] ')
                                    print(cstr)
                                    print('score:', score)
                                    print('ori:', word_node.value)
                                    print('s1:', bgws)
                                    print('s2:', score2)
                                    print(wrd)
                                    print('-------------')
                                
                    else:
                        one_update = True
                    self.bot_tiles[i] = self.temp_tiles.pop()
                self.scrabble_board[row][col].botRemovetile()
        return one_update
    
    # Find Horizontal Words Forward (Suffix Tree search)
    def findAllWordsHorizontalAfter(self, row, col, candidates, word_node_and_index, best):
        # Search next node until finding empty tile or the right end of the board
        for i in range(col, 15):
            # If the square contains a locked tile, continue to the next one
            if self.scrabble_board[row][col].hasTile() and self.scrabble_board[row][col].letter_tile.isLocked():
                word_node_and_index = self.word_dictionary.searchNextNode(self.scrabble_board[row][col].letter_tile.letter, *word_node_and_index)
                # Return false when the word is invalid
                if word_node_and_index[0] is None:
                    return False
                col += 1
            else:
                break
        
        if col > 14:
            return False

        previous_letter = ''
        one_update = False

        # If the current substring is a suffix: search inside the suffix's Trie
        if len(word_node_and_index[0].subword) == word_node_and_index[1] and word_node_and_index[0].suffix is not None:
            self.findAllWordsHorizontalBefore(row, self.temp_tiles[0].square.getCoordinate()[1] - 1, candidates, (word_node_and_index[0].suffix, 0), best)
        
        for i in range(7):
            # If bot tile exist, square at (row, col) is not beside any square with locked tile or beside square(s) with locked tile but the bot tile's letter is a candidate of that square, then search further
            if self.bot_tiles[i] is not None and ((row, col) not in candidates or self.bot_tiles[i].letter in candidates[(row, col)]) and self.bot_tiles[i].letter != previous_letter:
                # Assign the bot tile to the board
                self.scrabble_board[row][col].botAssignTile(self.bot_tiles[i])
                
                # Search next node at the letter the bot tile contains
                word_node, node_subword_index = self.word_dictionary.searchNextNode(self.bot_tiles[i].letter, *word_node_and_index)
                
                # If next node is found
                if word_node is not None:
                    # Assign bot tile to the board & remove it from bot's rack
                    self.temp_tiles.append(self.bot_tiles[i])
                    self.bot_tiles[i] = None
                    
                    # Search possible forward tile to be placed
                    updated = self.findAllWordsHorizontalAfter(row, col + 1, candidates, (word_node, node_subword_index), best)
                    
                    # If there isn't any update going on further recursion, then do this, otherwise, prune
                    if not updated and (col >= 14 or not self.scrabble_board[row][col + 1].hasTile()):
                        # Find the vertical scores
                        score2, wrd = self.getWords(self.getWordVertical)

                        if score2 >= 0:
                            # Do this if horizontal score is valid
                            if word_node.value > 0 and len(word_node.subword) == node_subword_index:
                                # Get horizontal score
                                bgws = self.botGetWordScore(word_node.value)
                                score = bgws + score2

                                # Update if its the new highscore
                                if score > best['score']:
                                    best['score'] = score
                                    best['config'] = tuple(self.temp_tiles)
                                    best['position'] = [tile.square.getCoordinate() for tile in self.temp_tiles]
                                    one_update = True

                                    # Logging the updated move configuration
                                    cstr = ''
                                    for conf in best['config']:
                                        if conf is not None:
                                            cstr += ('[' + conf.letter + ':' + str(conf.square.getCoordinate()) + '] ')
                                    print(cstr)
                                    print('score:', score)
                                    print('ori:', word_node.value)
                                    print('s1:', bgws)
                                    print('s2:', score2)
                                    print(wrd)
                                    print('-------------')
                    else:
                        one_update = True
                    
                    # Return tile to rack
                    self.bot_tiles[i] = self.temp_tiles.pop()
                
                # Remove tile from board
                self.scrabble_board[row][col].botRemovetile()
        return one_update
    
    # Find Vertical Words Forward (Suffix Tree search)
    def findAllWordsVerticalAfter(self, row, col, candidates, word_node_and_index, best):
        for i in range(row, 15):
            if self.scrabble_board[row][col].hasTile() and self.scrabble_board[row][col].letter_tile.isLocked():
                word_node_and_index = self.word_dictionary.searchNextNode(self.scrabble_board[row][col].letter_tile.letter, *word_node_and_index)
                if word_node_and_index[0] is None:
                    return False
                row += 1
            else:
                break
        if row > 14:
            return False
        
        previous_letter = ''
        one_update = False
        updated_suffix = False
        if len(word_node_and_index[0].subword) == word_node_and_index[1] and word_node_and_index[0].suffix is not None:
            self.findAllWordsVerticalBefore(self.temp_tiles[0].square.getCoordinate()[0] - 1, col, candidates, (word_node_and_index[0].suffix, 0), best)
        
        for i in range(7):
            if self.bot_tiles[i] is not None and ((row, col) not in candidates or self.bot_tiles[i].letter in candidates[(row, col)]) and self.bot_tiles[i].letter != previous_letter:
                self.scrabble_board[row][col].botAssignTile(self.bot_tiles[i])
                word_node, node_subword_index = self.word_dictionary.searchNextNode(self.bot_tiles[i].letter, *word_node_and_index)
                if word_node is not None:
                    self.temp_tiles.append(self.bot_tiles[i])
                    self.bot_tiles[i] = None
                    
                    updated = self.findAllWordsVerticalAfter(row + 1, col, candidates, (word_node, node_subword_index), best)
                    
                    if not (updated or updated_suffix) and (row >= 14 or not self.scrabble_board[row + 1][col].hasTile()):
                        score2, wrd = self.getWords(self.getWordHorizontal)
                        if score2 >= 0:
                            if word_node.value > 0 and len(word_node.subword) == node_subword_index:
                                bgws = self.botGetWordScore(word_node.value)
                                score = bgws + score2
                                if score > best['score']:
                                    best['score'] = score
                                    best['config'] = tuple(self.temp_tiles)
                                    best['position'] = [tile.square.getCoordinate() for tile in self.temp_tiles]
                                    one_update = True

                                    cstr = ''
                                    for conf in best['config']:
                                        if conf is not None:
                                            cstr += ('[' + conf.letter + ':' + str(conf.square.getCoordinate()) + '] ')
                                    print(cstr)
                                    print('score:', score)
                                    print('ori:', word_node.value)
                                    print('s1:', bgws)
                                    print('s2:', score2)
                                    print(wrd)
                                    print('-------------')
                    else:
                        one_update = True
                    self.bot_tiles[i] = self.temp_tiles.pop()
                
                self.scrabble_board[row][col].botRemovetile()
        return one_update
    
    # Bot move
    def botFind(self):
        best = {'score': 0, 'config': None}
        candidates = self.findAllCandidates(7, 7, best)

        self.temp_tiles.append(None)
        
        # Row candidates
        for (row, col) in candidates[0]:
            print('candidate:', row, col, candidates[0][(row, col)])
            previous_letter = ''

            # If before this (row, col) square there are already locked tiles in place, find the last node of the word made by those already locked tiles
            word_node_root, node_subword_index_root = self.getWordLastNodeHorizontal(row, col)
            
            for i in range(7):
                # Only perform search if the tile is in row candidate
                if self.bot_tiles[i] is not None and self.bot_tiles[i].letter in candidates[0][(row, col)] and self.bot_tiles[i].letter != previous_letter:
                    # Assign tile to the board & find the next node at bot tile's letter
                    self.scrabble_board[row][col].botAssignTile(self.bot_tiles[i])
                    word_node, node_subword_index = self.word_dictionary.searchNextNode(self.bot_tiles[i].letter, word_node_root, node_subword_index_root)
                    
                    if word_node is not None:
                        # Assign tile to the board & remove tile from bot's rack
                        self.temp_tiles[0] = self.bot_tiles[i]
                        self.bot_tiles[i] = None
                        
                        # Do forward search
                        self.findAllWordsHorizontalAfter(row, col + 1, candidates[0], (word_node, node_subword_index), best)

                        # Return tile to the bot's rack
                        self.bot_tiles[i] = self.temp_tiles[0]
                    
                    # Remove tile from the board
                    self.scrabble_board[row][col].botRemovetile()
        
        # Column candidates
        for (row, col) in candidates[1]:
            print('candidate:', row, col, candidates[1][(row, col)])
            previous_letter = ''
            word_node_root, node_subword_index_root = self.getWordLastNodeVertical(row, col)
            
            for i in range(7):
                if self.bot_tiles[i] is not None and self.bot_tiles[i].letter in candidates[1][(row, col)] and self.bot_tiles[i].letter != previous_letter:
                    self.scrabble_board[row][col].botAssignTile(self.bot_tiles[i])
                    word_node, node_subword_index = self.word_dictionary.searchNextNode(self.bot_tiles[i].letter, word_node_root, node_subword_index_root)
                    if word_node is not None:
                        self.temp_tiles[0] = self.bot_tiles[i]
                        self.bot_tiles[i] = None
                        self.findAllWordsVerticalAfter(row + 1, col, candidates[1], (word_node, node_subword_index), best)
                        self.bot_tiles[i] = self.temp_tiles[0]
                    self.scrabble_board[row][col].botRemovetile()

        self.resetTempTile()

        # Bot passes if there is no possible move
        if best['score'] <= 0:
            print('bot passed')
            self.current_word_score_bot = 0
            return False
        
        # Otherwise bot performs the move to the board
        else:
            # The bot moves its tiles from bot's rack to the board
            self.temp_tiles = best['config']
            for i, tile in enumerate(self.temp_tiles):
                del tile.square
                self.scrabble_board[best['position'][i][0]][best['position'][i][1]].assignTile(tile)
            
            # Remove placed bot tiles from bot's rack
            for i in range(7):
                if self.bot_tiles[i] is not None and hasattr(self.bot_tiles[i].square, 'square') and self.bot_tiles[i].square is not None:
                    self.bot_tiles[i] = None
            
            # Update bot's score
            self.current_word_score_bot = best['score']
            self.current_score_bot += self.current_word_score_bot

            return True
    
    # Gets the number of new tiles placed on a given row
    def checkRow(self, row, col, direction):
        if col < 0 or col > 14 or not self.scrabble_board[row][col].hasTile():
            return 0
        if self.scrabble_board[row][col].getTile().isLocked():
            return self.checkRow(row, col + direction, direction)
        else:
            return 1 + self.checkRow(row, col + direction, direction)
    
    # Gets the number of new tiles placed on a given column
    def checkCol(self, row, col, direction):
        if row < 0 or row > 14 or not self.scrabble_board[row][col].hasTile():
            return 0
        if self.scrabble_board[row][col].getTile().isLocked():
            return self.checkCol(row + direction, col, direction)
        else:
            return 1 + self.checkCol(row + direction, col, direction)
    
    # Getting score of given word added with the modifiers on the squares
    def botGetWordScore(self, word_score):
        letter_modifier_score = 0
        multiplier = 1
        for temp_tile in self.temp_tiles:
            square_type = temp_tile.square.getSquareType()
            if square_type[1] == 'L':
                letter_modifier_score += temp_tile.getTileScoreModified()
            elif square_type[1] == 'W':
                multiplier *= temp_tile.getTileScoreModified()

        if word_score > 0:
            bingo = 0
            if len(self.temp_tiles) == 7:
                bingo = 50
            return (word_score + letter_modifier_score) * multiplier + bingo
        return word_score
    
    # Getting score of given word added with the modifiers on the squares
    def getWordScore(self, word):
        if len(word) > 1:
            letter_modifier_score = 0
            multiplier = 1
            for temp_tile in self.temp_tiles:
                square_type = temp_tile.square.getSquareType()
                if square_type[1] == 'L':
                    letter_modifier_score += temp_tile.getTileScoreModified()
                elif square_type[1] == 'W':
                    multiplier *= temp_tile.getTileScoreModified()
            
            word_score = self.word_dictionary.searchWord(word)
            if word_score > 0:
                bingo = 0
                if len(self.temp_tiles) == 7:
                    bingo = 50
                return (word_score + letter_modifier_score) * multiplier + bingo
            return word_score

        return 0
    
    # Get the score of word, but it is guaranteed that there is only at max 1 score modifier
    def getWordScoreOne(self, word, tile):
        word_score = self.word_dictionary.searchWord(word)
        
        if word_score > 0:
            square_type = tile.square.getSquareType()
            if square_type[1] == 'L':
                word_score +=  tile.getTileScoreModified()
            elif square_type[1] == 'W':
                word_score *= tile.getTileScoreModified()

        return word_score
    
    # Get the vertical word placed on a given column
    def getWordVertical(self, row, col):
        word = self.scrabble_board[row][col].getTile().getLetter()

        row_idx = row - 1
        while row_idx >= 0 and self.scrabble_board[row_idx][col].hasTile():
            word = self.scrabble_board[row_idx][col].getTile().getLetter() + word
            row_idx -= 1

        row_idx = row + 1
        while row_idx < 15 and self.scrabble_board[row_idx][col].hasTile():
            word = word + self.scrabble_board[row_idx][col].getTile().getLetter()
            row_idx += 1
        
        return word
    
    def botGetWordHorizontal(self, row, col):
        word = self.scrabble_board[row][col].getTile().getLetter()

        col_idx = col - 1
        while col_idx >= 0 and self.scrabble_board[row][col_idx].hasTile():
            word = self.scrabble_board[row][col_idx].getTile().getLetter() + word
            col_idx -= 1

        col_idx = col + 1
        while col_idx < 15 and self.scrabble_board[row][col_idx].hasTile():
            word = word + self.scrabble_board[row][col_idx].getTile().getLetter()
            col_idx += 1
        
        word_node, node_subword_index = self.word_dictionary.searchWordNode(word)
        return word_node, node_subword_index
    
    # Find the last previous horizontal word node in a given row
    def getWordLastNodeHorizontal(self, row, col):
        word = ''

        # Get prefix
        col_idx = col - 1
        while col_idx >= 0 and self.scrabble_board[row][col_idx].hasTile():
            word = self.scrabble_board[row][col_idx].getTile().getLetter() + word
            col_idx -= 1
        
        # If prefix isn't found, use root instead
        if col_idx == col - 1:
            return self.word_dictionary.root, 0
        
        # Else, return the last node
        return self.word_dictionary.searchWordNode(word, self.word_dictionary.root)
    
    # Find the last previous vertical word node in a given column
    def getWordLastNodeVertical(self, row, col):
        word = ''

        # Get prefix
        row_idx = row - 1
        while row_idx >= 0 and self.scrabble_board[row_idx][col].hasTile():
            word = self.scrabble_board[row_idx][col].getTile().getLetter() + word
            row_idx -= 1
        
        # If prefix isn't found, use root instead
        if row_idx == row - 1:
            return self.word_dictionary.root, 0
        
        # Else, return the last node
        return self.word_dictionary.searchWordNode(word, self.word_dictionary.root)    

    # Get the horizontal word placed on a given row
    def getWordHorizontal(self, row, col):
        word = self.scrabble_board[row][col].getTile().getLetter()

        col_idx = col - 1
        while col_idx >= 0 and self.scrabble_board[row][col_idx].hasTile():
            word = self.scrabble_board[row][col_idx].getTile().getLetter() + word
            col_idx -= 1

        col_idx = col + 1
        while col_idx < 15 and self.scrabble_board[row][col_idx].hasTile():
            word = word + self.scrabble_board[row][col_idx].getTile().getLetter()
            col_idx += 1
        
        return word
    
    def getWordsV1(self, getWordInAxis):
        score = 0
        words = []
        for temp_tile in self.temp_tiles:
            new_score, new_word = getWordInAxis(*temp_tile.square.getCoordinate())
            if new_score == -1:
                return -1, None
            if new_word is not None:
                words.append(new_word)
            score += new_score
        return score, words
    
    # Find multiple words (either horizontal or vertical) and each of their score given the list of their rows or columns
    def getWords(self, getWordInAxis):
        score = 0
        words = []

        # Iterate for each new tile currently placed in the board
        for temp_tile in self.temp_tiles:
            # This can either find horizontal words or vertical words
            new_word = getWordInAxis(*temp_tile.square.getCoordinate())
            if len(new_word) == 1:
                continue
            
            new_score = self.getWordScoreOne(new_word, temp_tile)
            
            # If the word is invalid: return nothing since this move is not legal
            if new_score < 0:
                return -1, None
            
            # Otherwise, add the word to the list & add the score to later be returned
            if new_word is not None:
                words.append(new_word)
            score += new_score

        return score, words
    
    # Check if the player made a legal move or not
    def checkMove(self):

        # Game State First: check if touching entrance
        if not self.scrabble_board[7][7].hasTile():
            return False

        temp_tiles_length = len(self.temp_tiles)

        # Check if no tiles placed
        if temp_tiles_length == 0:
            return False
        
        start_coordinate = self.temp_tiles[0].square.getCoordinate()
        
        if self.scrabble_board[7][7].letter_tile.isLocked():
            # Game State Mid: check if attached to at least 1 previous tile
            if not self.checkAttached(*start_coordinate, set()):
                return False
            
        # Game State First: check if word length is greater than 1
        elif temp_tiles_length == 1:
            return False
        
        # Check if all placed tiles is in 1 row or 1 column and connected
        row_check = -1 + self.checkRow(*start_coordinate, 1) + self.checkRow(*start_coordinate, -1)
        col_check = -1 + self.checkCol(*start_coordinate, 1) + self.checkCol(*start_coordinate, -1)
        score = 0
        score2 = -1

        # If number of found new tiles in a row is the same as number of placed new tiles, then this rule checks
        if row_check == temp_tiles_length:
            # Check if the horizontal word is valid
            word = self.getWordHorizontal(*start_coordinate)
            score = self.getWordScore(word)
            if score < 0:
                return False
            
            # Get vertical scores and words
            score2, words = self.getWords(self.getWordVertical)
        
        # If number of found new tiles in a column is the same as number of placed new tiles, then this rule checks
        elif col_check == temp_tiles_length:
            # Check if the vertical word is valid
            word = self.getWordVertical(*start_coordinate)
            score = self.getWordScore(word)
            if score <= 0:
                return False
            
            # Get horizontal scores and words
            score2, words = self.getWords(self.getWordHorizontal)

        # Check if the other axis is valid
        if score2 == -1:
            return False
        
        words.append(word)
        
        print(words)
        print(score, score2)

        # Update the score that will be given if this move is entered
        self.current_word_score = score + score2

        return True
    
    # Initiation
    def __init__(self, scrabble_board, word_dictionary, bot_tiles):
        self.scrabble_board = scrabble_board
        self.resetTempTile()
        self.bot_tiles = bot_tiles
        self.word_dictionary = word_dictionary
        self.current_score = 0
        self.current_word_score = 0
        self.current_score_bot = 0
        self.current_word_score_bot = 0
    
    # Add the tile to the list of new tiles currently in the board after moving it from the rack
    def addTempTile(self, tile):
        if tile.square.getSquareType() == 'RA':
            self.temp_tiles.append(tile)
    
    # Delete the tile from the list of new tiles currently in the board
    def delTempTile(self, tile):
        for i, temp_tile in enumerate(self.temp_tiles):
            if temp_tile is tile:
                del self.temp_tiles[i]
                break
    
    # Empty the list of new tiles currently in the board
    def resetTempTile(self):
        self.temp_tiles = []
    
    # Lock the tiles after confirming a valid move
    def lockTiles(self):
        for temp_tile in self.temp_tiles:
            temp_tile.lock()
        self.resetTempTile()
    
    # Add the player's score
    def addCurrentScore(self):
        self.current_score += self.current_word_score
        self.current_word_score = 0
    
    # Get bot's total score and recent score
    def getBotScores(self):
        return self.current_score_bot, self.current_word_score_bot
    
    # Get player's current score that they can make according to current board state
    def getCurrentScore(self):
        return self.current_score
    
    # Get the number of new tiles currently placed in the board
    def getTempTilesLength(self):
        return len(self.temp_tiles)
    
    # Reset the player's current score that they can make according to current board state
    def resetCurrentWordScore(self):
        self.current_word_score = 0