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

def text_setup(text, pos, size = 36, bg_color = settings.bg_color):
    font = pg.font.SysFont('Arial',size, bold = True)
    txt = font.render(text, True, (0, 0, 0), bg_color)
    textRect = txt.get_rect()
    textRect.center = pos
    return txt, textRect

def player_confirm(screen, footer_y, pos_input, play_setup_done):

    click_next = False

    if pos_input:
        
        if pos_input[1] <= footer_y+20 and pos_input[1] >= footer_y-20:
            if pos_input[0] >= (settings.screen_width // 2) + 300 - 40 and\
                pos_input[0] <= (settings.screen_width // 2) + 300 + 40:
                    click_next = True
    
    return click_next and play_setup_done

def player_setup(screen, input_box, chara_box, pos_input, setting_para, max_player):
    Q1_y, Q2_y = setting_para[:2]
    footer_y = setting_para[-1]
    
    Q1, Q1Rect = text_setup('How many player?  (Max = ' + str(max_player) + ')', 
                            (settings.screen_width // 2 - 100, Q1_y))
    Q2, Q2Rect = text_setup('Please choose charactors, if not enougth, will fill up randonly', 
                            (settings.screen_width // 2, Q2_y))
    next_text, next_Rect = text_setup(' next ', ((settings.screen_width // 2) + 300, footer_y), 
                              36, bg_color=color.WHITE)
    
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
        
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos_input = pg.mouse.get_pos()
    
        input_box.handle_event(event)
        for box in chara_box:
            box.handle_event(event)
        
    input_box.update()
    
    input_box.draw(screen)
    
    chara_pick = []
    chara_rest = []
    for i, box in enumerate(chara_box):
        box.draw(screen)
        if box.hit % 2:
            chara_pick.append(i)
        else:
            chara_rest.append(i)

    
    screen.blit(Q1, Q1Rect)
    screen.blit(Q2, Q2Rect)
    screen.blit(next_text, next_Rect)
    
    try:
        player_number =  int(input_box.text)

        if player_number > max_player:
            play_setup_done = False
        else:
            if player_number < len(chara_pick):
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
        
    play_setup_done = player_confirm(screen, footer_y, pos_input, play_setup_done)    
    
    return  play_setup_done, chara_pick

def chara_setup(screen, chara_pool, pos, size, col = 2):
    # start from x = 360, y = 250
    # size = 1000, 400
    chara_box = [SelectDicBox(key = chara.key, 
                              val = chara.discribe, 
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


def present(screen, cities, Players, InfectionCard, WorldMap, grid, 
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



pg.init()
FONT = pg.font.Font(None, 32)
FONT_p = pg.font.Font(None, 24)
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = pg.Color('lightskyblue3')
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
            self.color = pg.Color('dodgerblue2') if self.active else pg.Color('lightskyblue3')
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
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+20, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class SelectTextBox():

    def __init__(self, x=10, y=10, w=10, h=10, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
    
    def update_rect(self,x,y,w,h):
        self.rect = pg.Rect(x,y,w,h)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (192, 192, 192) if self.active else (255, 255, 255)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

class SelectDicBox():

    def __init__(self, x=10, y=10, w=10, h=10, key='', val=[], color = (50,50,50)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
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
        self.x = x
        self.y = y
        self.w = w
        self.h = h

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
            val_rect = pg.Rect( self.x+ 50, self.y + (i+1)*50,
                               self.w//2, self.h//n)
            screen.blit(val_txt_surface, val_rect)
            
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 10)

