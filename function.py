import csv
import math
import random
import pygame as pg

from feature import City, Player
from settings import Settings
import color as color

settings = Settings()
bg_color = settings.bg_color

def cities_setup(ct_map, ct_link, city_size):
    cities = {}
    cities_ls = []
    with open(ct_map) as city_map:
        content = csv.reader(city_map, delimiter=',')
        for row in content:
            if row[1] in ['r','b','k','y']:
                cities[row[0]] = City(row[0], row[1], int(row[2]), int(row[3]),
                                      city_size[0], city_size[1], int(row[4]))
                cities_ls.append(row[0])
                
    with open(ct_link) as city_link:
        content = csv.reader(city_link, delimiter=',')
        for row in content:
            if row[1] in cities_ls:
                cities[row[0]].add_link(row[1])
    return cities, cities_ls



def chara_setup(screen, chara_pool, pos, size, col = 2):
    # start from x = 360, y = 250
    # size = 1000, 400

    chara_box = [ SelectDicText(title = chara.key, 
                                body = chara.discribe,
                                color = chara.color) for chara in chara_pool]
    
    
    n_point = math.ceil(len(chara_box)/col)

    w = size[0] // col
    h = size[1] // n_point
    
    x = pos[0]
    for n_col in range(col):
        y = pos[1]
        for box in chara_box[ n_col * n_point : (n_col+1) * n_point]:
            box.update_rect(x,y,w,h)
        
            y += h
            y += 10
        x += w
        x += 10
    return chara_box

def player_setup(screen, input_box, chara_box, pos_input, setting_para, max_player):
    Q1_y, Q2_y = setting_para[:2]
    footer_y = setting_para[-1]
    
    Q1_text = SelectText(text = 'How many player?  ( 2 - ' + str(max_player) + ')',
                         x = (settings.screen_width // 2 - 100), y = Q1_y)
    Q1_text.update_text(color = color.BLACK, size = 48)

    Q2_text = SelectText(text = 'Please choose charactors, if not enougth, will fill up randonly',
                        x = (settings.screen_width // 2), y = Q2_y)
    Q2_text.update_text(color = color.BLACK, size = 36)
    
    Next_text = SelectText(text = 'Next',
                           x = (settings.screen_width // 2 + 300), y = footer_y)
    
    Next_text.update_select_method(False)
    Next_text.update_text(color = color.BLACK, size = 48)

    rtn_Next = False
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
        
        input_box.handle_event(event)
        
        for box in chara_box:
            box.handle_event(event)
            
        rtn_Next = Next_text.handle_event(event)

    input_box.update()
    
    chara_pick = []
    chara_rest = []
    for i, box in enumerate(chara_box):
        box.draw(screen, thick=10)
        if box.hit % 2:
            chara_pick.append(i)
        else:
            chara_rest.append(i)

    input_box.draw(screen)
    Q1_text.draw(screen)
    Q2_text.draw(screen)
    Next_text.draw(screen)
    
    try:
        player_number =  int(input_box.text)

        if player_number > max_player:
            play_setup_done = False
        else:
            if player_number < len(chara_pick) or len(chara_pick) <=1:
                play_setup_done = False
            elif player_number > len(chara_pick):
                random.shuffle(chara_rest)
                while len(chara_pick) < player_number:    
                    chara_pick.append(chara_rest.pop())
                play_setup_done = True
            else:
                play_setup_done = True
        
    except:
        play_setup_done = False
        
    play_setup_done = play_setup_done and rtn_Next  
    
    return  play_setup_done, chara_pick



# control fn
## display map, return key information to make sure user complete each step

# make sure if user draw infection card
def control_infection(screen, cities, Players, InfectionCard, WorldMap, grid, 
            special_rate = False, rtn_draw = '', rtn_discard = ''):
    
    if not special_rate:
        rate = InfectionCard.rate
    else:
        rate = special_rate
    # game display setting
    # =====================================================
    # fill color
    screen.fill(bg_color)

    ###
    # supervise keyboard and mouse item
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            grid.update(pos)
        
        # check who get pick
        # city
        for city in cities:
            cities[city].handle_event(event)
        # player
        for player in Players:
            player.handle_event(event)
            
        # infection card
        rtn_draw, rtn_discard = InfectionCard.handle_event(event)
        
        #  highlight this city
        if rtn_discard:
            cities[rtn_discard].active = True                
                
        if rtn_draw:
            cities[rtn_draw].active = True
            cities[rtn_draw].infect(cities[rtn_draw].color, rate)
    
    ## draw stuff
    # draw world map
    WorldMap.blitme()
    
    # draw city state
    for city in cities:
        cities[city].display_city_label(screen)
        cities[city].display_city_dis(screen)   
    
    
    # draw player state
    for player in Players:
        player.display_player_map(screen)

    # draw infection area
    InfectionCard.display(screen)

    #grid.draw()
    
    # visualiaze the window
    pg.display.flip()    

    return rtn_draw, rtn_discard

# make sure user finish the move for each round

# make sure user draw player card


pg.init()
FONT = pg.font.Font(None, 32)
FONT_p = pg.font.Font(None, 24)
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
        
    def draw(self, screen, thick = 2):
        # Blit the rect.
        rect = pg.Rect(self.x, self.y, self.w, self.h)
        pg.draw.rect(screen, self.color, rect, thick)


class SelectText(SelectBox):
    def __init__(self, x=10, y=10, w=10, h=10, keep_select = True, color = (0, 0, 0), 
                 text = '', is_draw_rect = False):
        super().__init__(x=x, y=y, w=w, h=h, keep_select = keep_select, color = color)
        
        self.content = text
        font = pg.font.SysFont('Arial',32, bold = True)
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = (x,y)
            
        self.text = text
        self.rect = textRect
        
        self.is_draw_rect = is_draw_rect
        
    def update_text(self, text = '', size = 32, color = (192, 192, 192)):
        
        font = pg.font.SysFont('Arial',size, bold = True)
        if text:
            text = font.render(text, True, color)
            self.content = text
        else:
            text = font.render(self.content, True, color) 
        textRect = text.get_rect()
        textRect.center = (self.x, self.y)
            
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
                 title = '', body = []):
        super().__init__(x=x, y=y, w=w, h=h, keep_select = keep_select, color = color)
        
        self.FONT_title = pg.font.Font(None, 32)
        self.FONT_body = pg.font.Font(None, 24)   
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
      
        
        

class SelectDicBox():

    def __init__(self, x=10, y=10, w=10, h=10, key='', val=[], color = (50,50,50)):
        self.rect = pg.Rect(x, y, w, h)
        self.color = (192, 192, 192)
        self.txt_color = (192, 192, 192)
        self.key = key
        self.val = val
        self.active = False
        self.hit = 0
        
        # color
        self.rect_select_color = color
        self.txt_select_color = (50,50,50)
        self.unselect_color = (192,192,192)
        
        self.txt_surface = FONT.render(key, True, (50,50,50))
        
    def update_rect(self,x,y,w,h):
        self.rect = pg.Rect(x,y,w,h)

    def handle_event(self, event, keep_select = True):
        if keep_select:
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.hit += 1
                    
                # Change the current color of the input box.
                self.txt_color = self.txt_select_color if self.hit % 2 else self.unselect_color
                self.color = self.rect_select_color if self.hit % 2 else self.unselect_color
        else:
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active

                else:
                    self.active = False
                # Change the current color of the input box.
                self.txt_color = self.txt_select_color if self.hit % 2 else self.unselect_color
                self.color = self.rect_select_color if self.hit % 2 else self.unselect_color
                            
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        n = len(self.val)
        for i, txt in enumerate(self.val):
            val_txt_surface = FONT_p.render(txt, True, self.txt_color)
            val_rect = pg.Rect( self.rect.x+ 50, self.rect.y + (i+1)*50,
                               self.rect.w//2, self.rect.h//n)
            screen.blit(val_txt_surface, val_rect)
            
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 10)


class GameControl():
    
    def __init__(self, screen, cities, Players, InfectionCard, WorldMap, grid):
        self.screen = screen
        self.cities = cities
        self.Players = Players
        self.InfectionCard = InfectionCard
        self.WorldMap = WorldMap
        self.grid = grid

    def display(self):
        # draw world map
        self.screen.fill(bg_color)
        self.WorldMap.blitme()
    
        # draw city state
        for city in self.cities:
            self.cities[city].display_city_label(self.screen)
            self.cities[city].display_city_dis(self.screen)   
    
        # draw player state
        for player in self.Players:
            player.display_player_map(self.screen)

        # draw infection area
        self.InfectionCard.display(self.screen)

        #self.grid.draw()
    
        # visualiaze the window
        pg.display.flip()    
    
    def even_control(self, event):
        # used in for loop
        # check who get pick
        
        # city
        for city in self.cities:
            self.cities[city].handle_event(event)
        # player
        for player in self.Players:
            player.handle_event(event)
            
        # infection card
        rtn_draw, rtn_discard = self.InfectionCard.handle_event(event)
        
        return rtn_draw, rtn_discard
    
    def after_event(self, rtn_draw, rtn_discard):
        
        # for infection part, highlight the city
            # either for new infection or user click on city name

        if rtn_discard:
            self.cities[rtn_discard].active = True                
                
        if rtn_draw:
            self.cities[rtn_draw].active = True
            self.cities[rtn_draw].infect(self.cities[rtn_draw].color, 1)        
            
    def after_event_initial(self, rtn_draw, rtn_discard, i):
        if rtn_discard:
            self.cities[rtn_discard].active = True                
                
        if rtn_draw:
            self.cities[rtn_draw].active = True
            self.cities[rtn_draw].infect(self.cities[rtn_draw].color, i)           
        