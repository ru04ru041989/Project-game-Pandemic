import pygame as pg
from settings import Settings
import color as color

settings = Settings()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


pg.init()
FONT = pg.font.Font(None, 32)
FONT_p = pg.font.Font(None, 24)


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
                    
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = (192, 192, 192)
        self.text_color = (0,0,0)
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (255, 255, 255) if self.active else (192, 192, 192)
            
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.text_color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+20, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class SelectBox():

    def __init__(self, x=10, y=10, w=10, h=10, keep_select = True, color = (0, 0, 0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.color = (192, 192, 192)
        
        # select control
        self.keep_select = keep_select
        self.active = False
        self.hit = 0
        
        self.unselect_color = (192, 192, 192)
        self.select_color = color

    def update_select_color(self,color):
        self.select_color = color
        
    def update_unselect_color(self,color):
        self.unselect_color = color
        self.color = color

    def update_rect(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
    
    def update_pos(self,x,y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)        
    
    def update_select_method(self, keep_select):
        self.keep_select = keep_select
        
    def handle_event(self, event):
        rtn = False
        clickon = False
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # record hit time
                self.hit += 1
                clickon = True
            else:
                clickon = False
            
            if self.keep_select:
                self.color = self.select_color if self.hit % 2 else self.unselect_color
                rtn = True if self.hit % 2 else False
            else:
                self.color = self.select_color if clickon else self.unselect_color
                rtn = True if clickon else False
        return rtn            
        
    def draw(self, screen, thick = 2, is_select = False):
        # Blit the rect.
        rect = pg.Rect(self.x, self.y, self.w, self.h)
        pg.draw.rect(screen, self.color, rect, thick)
        
        if is_select:
            pg.draw.rect(screen, self.select_color, rect, thick)


class SelectText(SelectBox):
    def __init__(self, x=10, y=10, w=10, h=10, keep_select = True, color = (0, 0, 0), 
                 text = '', is_draw_rect = False, size = 32):
        super().__init__(x=x, y=y, w=w, h=h, keep_select = keep_select, color = color)
        
        self.content = text
        self.font = pg.font.SysFont('Arial',size, bold = True)
        text = self.font.render(text, True, color)
        self.textRect = text.get_rect()
        self.textRect.center = (x,y)
            
        self.text = text
        self.rect = self.textRect
        self.size = size
        
        self.is_draw_rect = is_draw_rect
    
    def update_text_pos(self, x,y):
        self.textRect.topleft = (x,y)
    
    def update_text(self, text):

        text = self.font.render(text, True, self.color)
        self.content = text

        textRect = text.get_rect()

        self.text = text
        self.rect = textRect        
        
    def set_draw_rect(self, is_draw_rect):
        self.is_draw_rect = is_draw_rect
    
    def return_textrect(self):
        return self.rect
    
    def draw(self, screen, thick = 2):
        # Blit the text.
        #text_surface = self.FONT.render(self.text, True, self.color)
        #screen.blit(self.text_surface, (self.x+10, self.y+5))
        screen.blit(self.text, self.rect)
        
        if self.is_draw_rect:
            pg.draw.rect(screen, self.color, self.rect, thick)            

    
class SelectDicText(SelectBox):
    def __init__(self, x=10, y=10, w=10, h=10, keep_select = True, color = (0, 0, 0), 
                 title = '', body = [], title_size = 32, body_size = 23):
        super().__init__(x=x, y=y, w=w, h=h, keep_select = keep_select, color = color)
        
        self.FONT_title = pg.font.Font(None, title_size)
        self.FONT_body = pg.font.Font(None, body_size)   
        self.title = title
        self.body = body
        self.indent = 50
        self.line_space = 50
        self.title_color = (0, 0, 0)
        
    def update_title(self, title, size = 32, color = (0, 0, 0)):
        self.title = title
        self.FONT_title = pg.font.Font(None, size)
        self.title_color = color
    
    def update_body(self, body, size = 24, line_space = 50, indent = 50):
        self.body = body if isinstance(body, list) else [body]
        self.FONT_body = pg.font.Font(None, size)
        self.line_space = line_space
        self.indent = indent

    def draw(self, screen, thick = 2):
        
        # Blit the title
        title_surface = self.FONT_title.render(self.title, True, self.title_color)
        screen.blit(title_surface, (self.x+10, self.y+5))
        
        # Blit the body
        n = len(self.body)
        for i, txt in enumerate(self.body):
            body_surface = self.FONT_body.render(txt, True, self.unselect_color)
            body_rect = pg.Rect( self.x+ self.indent, self.y + (i+1) * self.line_space,
                               self.w//2, self.h//n)
            screen.blit(body_surface, body_rect)
        
        # Blit the rect.
        rect = pg.Rect(self.x, self.y, self.w, self.h)
        pg.draw.rect(screen, self.color, rect, thick)
      
        