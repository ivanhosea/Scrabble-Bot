import pygame
from pygame_constants import *

class GameButton:

    # Initiate button: location, text, size, locked or not
    def __init__(self, location, title, lock=False):
        self.location = location
        self.size = (location.X_END - location.X, location.Y_END - location.Y)
        self.title = title
        self.title_center = ((location.X_END + location.X) // 2, (location.Y_END + location.Y) // 2)
        self.backgroundTile = pygame.Surface(self.size)
        if lock:
            self.locked = False
            self.lockButton()
        else:
            self.locked = True
            self.unlockButton()
    
    def lockButton(self):
        if not self.locked:
            self.title_view = FONT_COURIER_20.render(self.title, True, WHITE, GREY)
            self.title_rect = self.title_view.get_rect()
            self.title_rect.center = self.title_center
            self.backgroundTile.fill(GREY)
            self.locked = True
    
    def unlockButton(self):
        if self.locked:
            self.title_view = FONT_COURIER_20.render(self.title, True, BLACK, ORANGE)
            self.title_rect = self.title_view.get_rect()
            self.title_rect.center = self.title_center
            self.backgroundTile.fill(ORANGE)
            self.locked = False
    
    # Draw the button
    def blitButton(self, screen):
        screen.blit(self.backgroundTile, (self.location.X, self.location.Y))
        screen.blit(self.title_view, self.title_rect)
    
    def isLocked(self):
        return self.locked