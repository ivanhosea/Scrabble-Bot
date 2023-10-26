import random
from tile import Tile

class TilesDeck:
    # The amount of tiles in the deck of each letter
    DEFAULT_TILES_DECK = [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6, 4, 6, 4, 2, 2, 1, 2, 1]

    # Initiate a new deck of Tiles
    def __init__(self):
        self.tiles_deck = []
        new_tiles_deck = TilesDeck.DEFAULT_TILES_DECK[:]

        # Add 2 random letter tiles
        new_tiles_deck[random.randint(0, 25)] += 1
        new_tiles_deck[random.randint(0, 25)] += 1

        self.swappable = True

        # Generate the tiles
        for i in range(26):
            ch = chr(i + 65)
            self.tiles_deck += [Tile(ch) for i in range(new_tiles_deck[i])]
        self.size = 100

        # Fisher–Yates Shuffle: to shuffle the Tiles deck
        idx = 99
        while (idx > 0):
            randomIdx = random.randint(0, idx)
            temp_tile = self.tiles_deck[idx]
            self.tiles_deck[idx] = self.tiles_deck[randomIdx]
            self.tiles_deck[randomIdx] = temp_tile
            idx -= 1
    
    # Player draw function
    def draw(self, rack_tiles):
        for i in range(7):
            if not rack_tiles[i].hasTile() and self.size > 0:
                rack_tiles[i].assignTile(self.tiles_deck.pop())
                self.size -= 1
    
    # Bot draw function
    def botDraw(self, bot_tiles):
        for i in range(7):
            if bot_tiles[i] is None and self.size > 0:
                bot_tiles[i] = self.tiles_deck.pop()
                bot_tiles[i].square = None
                self.size -= 1
        
        for i in range(7):
            current_min = i
            if bot_tiles[i] is not None:
                for j in range(i + 1, 7):
                    if bot_tiles[j] is None:
                        current_min = j
                        break
                    if bot_tiles[current_min].letter > bot_tiles[j].letter:
                        current_min = j
                bot_tiles[current_min], bot_tiles[i] = bot_tiles[i], bot_tiles[current_min]
        
        # Logging: print the tiles in bot's rack
        str1 = ''
        for bt in bot_tiles:
            if bt is not None:
                str1 += (bt.letter + ' ')
        print('HAND:')
        print(str1)
        print('---------')

        # If the bot's rack is empty, game over
        if str1 == '':
            return True
        
        # Calculate if Swappable button can be clicked for the player
        self.calculateSwappable()
        return False
    
    # Swap function for player
    def swap(self, rack_tiles):
        moved_indexes = set()
        for i in range(7):
            if rack_tiles[i].hasTile():
                swap_index = random.randint(0, self.size - 1)
                while swap_index in moved_indexes:
                    swap_index = (swap_index + 1) % self.size
                moved_indexes.add(swap_index)
                temp_tile = rack_tiles[i].getTile()
                rack_tiles[i].assignTile(self.tiles_deck[swap_index])
                temp_tile.removeSquare()
                self.tiles_deck[swap_index] = temp_tile
    
    # Calculate if Swappable button can be clicked for the player
    def calculateSwappable(self):
        if self.size >= 7:
            self.swappable = True
        else:
            self.swappable = False
    
    # Check if player can swap
    def isSwappable(self):
        return self.swappable
    
    def playerPass(self):
        print('player passed')