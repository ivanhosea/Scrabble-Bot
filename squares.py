import pygame
from tile import Tile
from pygame_constants import *

class Squares:
    SQUARE_TYPES = [dict() for i in range(7)]

    # Init Square Visuals based on type
    def initBlank(x, y, self):
        self.square.fill(WHITE)
    
    def initEntrance(x, y, self):
        self.square.fill(PINK)
        self.square_name = pygame.transform.scale(FONT_COURIER.render('*', True, BLACK, PINK), (20, 30))
        self.square_name_pos = (x + 10, y + 5)
    
    def initDoubleLetter(x, y, self):
        self.square.fill(CYAN)
        self.square_name = pygame.transform.scale(FONT_COURIER.render('DL', True, BLACK, CYAN), (30, 30))
        self.square_name_pos = (x + 5, y + 5)
    
    def initTripleLetter(x, y, self):
        self.square.fill(BLUE)
        self.square_name = pygame.transform.scale(FONT_COURIER.render('TL', True, BLACK, BLUE), (30, 30))
        self.square_name_pos = (x + 5, y + 5)
    
    def initDoubleWord(x, y, self):
        self.square.fill(PINK)
        self.square_name = pygame.transform.scale(FONT_COURIER.render('DW', True, BLACK, PINK), (30, 30))
        self.square_name_pos = (x + 5, y + 5)
    
    def initTripleWord(x, y, self):
        self.square.fill(RED)
        self.square_name = pygame.transform.scale(FONT_COURIER.render('TW', True, BLACK, RED), (30, 30))
        self.square_name_pos = (x + 5, y + 5)
    
    def initRack(x, y, self):
        self.square.fill(BROWN)
    
    # Double letter modifier
    def squareDL(letter_score):
        return letter_score
    
    # Triple letter modifier
    def squareTL(letter_score):
        return letter_score * 2
    
    # Double word modifier
    def squareDW(letter_score):
        return 2
    
    # Triple word modifier
    def squareTW(letter_score):
        return 3
    
    # Initiate the init function given the square type
    def initSquares():
        Squares.SQUARE_TYPES[0]['name'] = 'BK'
        Squares.SQUARE_TYPES[0]['init'] = Squares.initBlank
        Squares.SQUARE_TYPES[1]['name'] = 'EW'
        Squares.SQUARE_TYPES[1]['init'] = Squares.initEntrance
        Squares.SQUARE_TYPES[1]['sf'] = Squares.squareDW
        Squares.SQUARE_TYPES[2]['name'] = 'DL'
        Squares.SQUARE_TYPES[2]['init'] = Squares.initDoubleLetter
        Squares.SQUARE_TYPES[2]['sf'] = Squares.squareDL
        Squares.SQUARE_TYPES[3]['name'] = 'TL'
        Squares.SQUARE_TYPES[3]['init'] = Squares.initTripleLetter
        Squares.SQUARE_TYPES[3]['sf'] = Squares.squareTL
        Squares.SQUARE_TYPES[4]['name'] = 'DW'
        Squares.SQUARE_TYPES[4]['init'] = Squares.initDoubleWord
        Squares.SQUARE_TYPES[4]['sf'] = Squares.squareDW
        Squares.SQUARE_TYPES[5]['name'] = 'TW'
        Squares.SQUARE_TYPES[5]['init'] = Squares.initTripleWord
        Squares.SQUARE_TYPES[5]['sf'] = Squares.squareTW
        Squares.SQUARE_TYPES[6]['name'] = 'RA'
        Squares.SQUARE_TYPES[6]['init'] = Squares.initRack

    # Initiate the square: position (in screen units), type, coordinate (0-14)
    def __init__(self, x, y, square_type_str, coordinate=None):
        self.letter_tile = None
        self.square = pygame.Surface((40, 40))
        self.square_pos = (x, y)
        self.square_type_id = int(square_type_str)
        Squares.SQUARE_TYPES[self.square_type_id]['init'](x, y, self)
        self.coordinate = coordinate
    
    # Assign Tile to a Square
    def assignTile(self, tile):
        tile.move(*self.square_pos)
        if hasattr(tile, 'square'):
            tile.square.removeTile()
        tile.square = self
        self.letter_tile = tile
    
    # Assign Tile to a Square, but for the bot
    def botAssignTile(self, tile):
        tile.square = self
        self.letter_tile = tile
    
    # Remove tile from a square, but for the bot
    def botRemovetile(self):
        self.letter_tile.square = None
        self.letter_tile = None
    
    # Check if Square has Tile
    def hasTile(self):
        return self.letter_tile is not None
    
    # Get the tile of the Square object
    def getTile(self):
        return self.letter_tile
    
    # Remove tile from a square
    def removeTile(self):
        self.letter_tile = None
    
    # Mark the Tile as selected
    def selectTile(self):
        if self.hasTile():
            self.letter_tile.select()
    
    # Unselect the selected tile
    def unselectTile(self):
        if self.hasTile():
            self.letter_tile.unselect()
    
    # Draw the Square or Tile onto the UI
    def drawSquare(self, screen):
        if self.letter_tile is None:
            screen.blit(self.square, self.square_pos)
            if hasattr(self, 'square_name'):
                screen.blit(self.square_name, self.square_name_pos)
        else:
            self.letter_tile.blitTile(screen)
    
    # Get the type of the Square
    def getSquareType(self):
        return Squares.SQUARE_TYPES[self.square_type_id]['name']
    
    # Get the Coordinate of the Square
    def getCoordinate(self):
        return self.coordinate
    
    # Get the modifier function of the square
    def squareFunction(self, letter_score):
        return Squares.SQUARE_TYPES[self.square_type_id]['sf'](letter_score)

Squares.initSquares()