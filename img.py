import pygame as pg
from settings import Settings

settings = Settings()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class WorldMap():
    def __init__(self, screen, filename):
        self.screen = screen
        
        image = pg.image.load(filename)
        self.image = pg.transform.scale(image, (1080,640))
        self.rect = self.image.get_rect()
        
    def resize(self,x,y):
        self.image = pg.transform.scale(self.image,(x,y))
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)

        
        
class grid():
    def __init__(self, screen):
        self.screen = screen
        
        self.width, self.height = 10, 10
        self.margin = 2
         
        self.grid = [[0 for x in range(settings.screen_width//self.width)] 
                     for y in range(settings.screen_height//self.height)]
    
    def update(self, pos):
        column = pos[0] // (self.width + self.margin)
        row = pos[1] // (self.height + self.margin)
        self.grid[row][column] = 1
        print('Click {}, Grid coordinates: ({},{})'.format(pos, row, column))
        
    def draw(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                color = BLACK
                if self.grid[row][col] ==1:
                    color = GREEN
                
                    pg.draw.rect(self.screen, color,
                             [(self.margin + self.width) * col + self.margin,
                              (self.margin + self.height) * row + self.margin,
                              self.width, self.height])