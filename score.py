import pygame
from pygame_constants import *

# Draw player's and bot's score
def drawScore(screen, player_score, player_score_recent, bot_score, bot_score_recent):
    screen.blit(FONT_COURIER_20.render('PLAYER: ' + str(player_score) + ' (+' + str(player_score_recent) + ')', True, WHITE, BLACK), (700, 50))
    screen.blit(FONT_COURIER_20.render('BOT   : ' + str(bot_score) + ' (+' + str(bot_score_recent) + ')', True, WHITE, BLACK), (700, 80))