import pygame
pygame.init()

import sys
import time
import configparser
from pygame_constants import *
from tile import Tile
from squares import Squares
from location import Location
from tiles_deck import TilesDeck
from game import Game
from trie import Trie
from game_button import GameButton
from score import drawScore

# Dictionary file init
config = configparser.ConfigParser()
config.read('game.ini')
FILENAME = config.get('GAME', 'dictionary')
del config

# Constants
WIDTH, HEIGHT = 1000, 700
BOARD_LOCATION = Location(10, 2, 2 + 15 * 42, 10 + 15 * 42)
RACK_LOCATION = Location(4 * 42 + 10, 648, 4 * 42 + 10 + 7 * 42, 648 + 42)
ENTER_LOCATION = Location(12 * 42 - 7, 648, 12 * 42 + 2 * 42 - 9, 648 + 42)
SWAP_LOCATION = Location(90, 648, 90 + 60, 648 + 42)
PASS_LOCATION = Location(10, 648, 10 + 60, 648 + 42)

# Initiate Tiles Deck
DECK = TilesDeck()

# Initiate Suffix Tree
WORD_DICTIONARY = Trie()
with open(FILENAME) as file_handler:
    for line in file_handler:
        if line != '':
            WORD_DICTIONARY.addWord(line.rstrip().upper())

# Create a game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SCRABBLE")

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False

# Initiate Scrabble Board
SCRABBLE_BOARD = []
with open('scrabble_board.txt', 'r') as file_handler:
    for i, line in enumerate(file_handler):
        new_row = []
        for j, ch in enumerate(line.rstrip()):
            new_row.append(Squares(BOARD_LOCATION.X + j * 42, BOARD_LOCATION.Y + i * 42, ch, (i, j)))
        SCRABBLE_BOARD.append(new_row)

# Initiate a new game
BOT_TILES = [None for i in range(7)]
GAME = Game(SCRABBLE_BOARD, WORD_DICTIONARY, BOT_TILES)

# Initiate the player's rack
RACK_HOLDER = pygame.Rect(RACK_LOCATION.X - 4, RACK_LOCATION.Y - 4, 7 * 42 + 6, 42 + 6)
RACK_TILES = []
for i in range(7):
    RACK_TILES.append(Squares(RACK_LOCATION.X + i * 42, RACK_LOCATION.Y, 6))

# Both players Draw Tiles
DECK.draw(RACK_TILES)
DECK.botDraw(BOT_TILES)

# Initiate Buttons
ENTER_BUTTON = GameButton(ENTER_LOCATION, 'ENTER', lock=True)
SWAP_BUTTON = GameButton(SWAP_LOCATION, 'SWAP')
PASS_BUTTON = GameButton(PASS_LOCATION, 'PASS')

bot_move = False

while running:

    # Delay 1 second to make player be able so clearly see what the bot played
    if bot_move:
        time.sleep(1)
        GAME.lockTiles()
        bot_move = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            
            # Clicking rack
            if RACK_LOCATION.isClicked(mx, my):
                rack_id = (mx - RACK_LOCATION.X) // 42
                
                # Either select or unselect the tile
                if Tile.SELECTED == RACK_TILES[rack_id].getTile():
                    Tile.unselectAll()
                else:
                    RACK_TILES[rack_id].selectTile()
            
            # Clicking board
            elif BOARD_LOCATION.isClicked(mx, my):
                board_col = (mx - BOARD_LOCATION.X) // 42
                board_row = (my - BOARD_LOCATION.Y) // 42

                # If a tile is selected
                if Tile.SELECTED is not None:

                    # If clicking the selected tile: return to rack
                    if Tile.SELECTED == SCRABBLE_BOARD[board_row][board_col].getTile():
                        for i in range(7):
                            if RACK_TILES[i].getTile() is None:
                                GAME.delTempTile(Tile.SELECTED)
                                RACK_TILES[i].assignTile(Tile.SELECTED)
                                Tile.SELECTED = None
                                if GAME.checkMove():
                                    ENTER_BUTTON.unlockButton()
                                else:
                                    GAME.resetCurrentWordScore()
                                    ENTER_BUTTON.lockButton()
                                if GAME.getTempTilesLength() == 0 and DECK.isSwappable():
                                    SWAP_BUTTON.unlockButton()
                                break
                    
                    # If the clicked square already has a tile: select the square's tile instead
                    elif SCRABBLE_BOARD[board_row][board_col].hasTile():
                        SCRABBLE_BOARD[board_row][board_col].selectTile()
                    
                    # If the clicked square is empty: move selected tile to the clicked square
                    else:
                        GAME.addTempTile(Tile.SELECTED)
                        SCRABBLE_BOARD[board_row][board_col].assignTile(Tile.SELECTED)
                        if GAME.checkMove():
                            ENTER_BUTTON.unlockButton()
                        else:
                            GAME.resetCurrentWordScore()
                            ENTER_BUTTON.lockButton()
                        SWAP_BUTTON.lockButton()

                # If no tile selected
                else:
                    SCRABBLE_BOARD[board_row][board_col].selectTile()
            
            # Clicking enter button
            elif ENTER_LOCATION.isClicked(mx, my) and not ENTER_BUTTON.isLocked():
                GAME.lockTiles()
                ENTER_BUTTON.lockButton()
                GAME.addCurrentScore()
                DECK.draw(RACK_TILES)

                # Bot plays a move
                bot_move = GAME.botFind()
                game_over = DECK.botDraw(BOT_TILES)

                if DECK.isSwappable():
                    SWAP_BUTTON.unlockButton()
                else:
                    SWAP_BUTTON.lockButton()
            
            # Clicking swap button
            elif SWAP_LOCATION.isClicked(mx, my) and not SWAP_BUTTON.isLocked():
                DECK.swap(RACK_TILES)
                GAME.resetCurrentWordScore()

                # Bot plays a move
                bot_move = GAME.botFind()
                game_over = DECK.botDraw(BOT_TILES)
                
                if DECK.isSwappable():
                    SWAP_BUTTON.unlockButton()
                else:
                    SWAP_BUTTON.lockButton()
            
            elif PASS_LOCATION.isClicked(mx, my) and not PASS_BUTTON.isLocked():
                Tile.unselectAll()
                GAME.resetCurrentWordScore()

                # Bot plays a move
                bot_move = GAME.botFind()
                game_over = DECK.botDraw(BOT_TILES)

                if DECK.isSwappable():
                    SWAP_BUTTON.unlockButton()
                else:
                    SWAP_BUTTON.lockButton()

            # Clicking others
            else:
                Tile.unselectAll()
        
        # Cheat: press enter key to force enter any tile, for testing purposes only, doesn't trigger a bot move nor adding score
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            GAME.lockTiles()
            DECK.draw(RACK_TILES)
            ENTER_BUTTON.lockButton()

    # Clear the screen
    screen.fill(BLACK)

    # Game over
    if game_over:
        screen.blit(FONT_COURIER.render('GAME OVER', True, RED, BLACK), (700, 150))

    # Draw rack holder
    pygame.draw.rect(screen, BROWN, RACK_HOLDER)

    # Draw the scores
    drawScore(screen, GAME.current_score, GAME.current_word_score, GAME.current_score_bot, GAME.current_word_score_bot)

    # Draw buttons
    ENTER_BUTTON.blitButton(screen)
    SWAP_BUTTON.blitButton(screen)
    PASS_BUTTON.blitButton(screen)
    
    # Draw the board
    for i in range(15):
        for j in range(15):
            SCRABBLE_BOARD[i][j].drawSquare(screen)
    
    # Draw the rack
    for i in range(7):
        RACK_TILES[i].drawSquare(screen)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()