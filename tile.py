import pygame
from pygame_constants import *
from trie import Trie
from scrabble_statics import letterValue

class Tile:
    SELECTED = None

    # Unselect the selected tile
    def unselectAll():
        if Tile.SELECTED is not None:
            Tile.SELECTED.square.unselectTile()
            Tile.SELECTED = None
    
    # Initiate a tile
    def __init__(self, letter):
        self.letter = letter
        self.locked = False
        self.unselect()
    
    # Move the tile to a position in the screen
    def move(self, x, y):
        self.letterPos = (x + 8, y + 3)
        self.scorePos = (x + 28, y + 22)
        self.backgroundPos = (x , y)
        self.unselect()
        Tile.SELECTED = None
    
    # Draw the tile onto the screen
    def blitTile(self, screen):
        screen.blit(self.backgroundTile, self.backgroundPos)
        screen.blit(self.letterTile, self.letterPos)
        screen.blit(self.scoreTile, self.scorePos)
    
    # Set the visual of the tile if this tile got selected
    def select(self):
        if Tile.SELECTED is not None:
            Tile.SELECTED.unselect()
        if not self.locked:
            Tile.SELECTED = self
            self.letterTile = pygame.transform.scale(FONT_COURIER.render(self.letter, True, BLACK, YELLOW), (20, 35))
            self.scoreTile = pygame.transform.scale(FONT_COURIER.render(str(letterValue(self.letter)), True, BLACK, YELLOW), (10, 15))
            self.backgroundTile = pygame.Surface((40, 40))
            self.backgroundTile.fill(YELLOW)
    
    # Set the visual of the tile if this tile got unselected
    def unselect(self):
        self.letterTile = pygame.transform.scale(FONT_COURIER.render(self.letter, True, BLACK, GREEN), (20, 35))
        self.scoreTile = pygame.transform.scale(FONT_COURIER.render(str(letterValue(self.letter)), True, BLACK, GREEN), (10, 15))
        self.backgroundTile = pygame.Surface((40, 40))
        self.backgroundTile.fill(GREEN)
    
    # Set the visual of locked tile & also lock it
    def lock(self):
        Tile.SELECTED = None
        self.locked = True
        self.letterTile = pygame.transform.scale(FONT_COURIER.render(self.letter, True, BLACK, EMERALD), (20, 35))
        self.scoreTile = pygame.transform.scale(FONT_COURIER.render(str(letterValue(self.letter)), True, BLACK, EMERALD), (10, 15))
        self.backgroundTile = pygame.Surface((40, 40))
        self.backgroundTile.fill(EMERALD)
    
    # Check if Tile is locked
    def isLocked(self):
        return self.locked
    
    # Get the letter of the Tile
    def getLetter(self):
        return self.letter
    
    # Return the value of the score modifier
    def getTileScoreModified(self):
        return self.square.squareFunction(letterValue(self.letter))
    
    # Unattach this Tile from its Square
    def removeSquare(self):
        del self.square