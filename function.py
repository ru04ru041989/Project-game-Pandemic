import csv
import math
import random
import string
import pygame as pg

from feature import City, Player
from settings import Settings
import color as color

from img import InputBox, SelectBox, SelectText, SelectDicText

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
            if player_number < len(chara_pick) or player_number <= 1:
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
    

class GameControl():
    
    def __init__(self, screen, cities, Players, InfectionCard, WorldMap, Tips, grid):
        self.screen = screen
        self.cities = cities
        self.Players = Players
        self.InfectionCard = InfectionCard
        self.WorldMap = WorldMap
        self.grid = grid
        self.Tips = Tips
        
        # event control
        self.rsp_player = ''
        self.rsp_city = ''

    def display(self):
        
        def update_Tip():
            # for player
            if self.rsp_player:
                content = self.rsp_player.discribe
                self.Tips['player'].update_content(content)
            else:
                self.Tips['player'].update_content('')
                
            # for city
            if self.rsp_city:
                dis_summary = self.cities[self.rsp_city].dis
                content = [string.capwords(self.rsp_city)]
                for k,v in dis_summary.items():
                    number = len(v)
                    if k == 'r' and number:
                        content.append( '   ' + str(number) + ' red disease')
                    if k == 'y' and number:
                        content.append( '   ' + str(number) + ' yellow disease')
                    if k == 'b' and number:
                        content.append( '   ' + str(number) + ' blue disease')                                        
                    if k == 'k' and number:
                        content.append( '   ' + str(number) + ' black disease')                    

                self.Tips['city'].update_content(content, is_title=True, y_border=5)
            else:
                self.Tips['city'].update_content('')
            
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
            player.display_player_area(self.screen)

        # draw infection area
        self.InfectionCard.display(self.screen)

        # draw tips
        # player tips

        update_Tip()
                    
        for Tip in self.Tips.values():
            Tip.display(self.screen)
        
        #self.grid.draw()
    
        # visualiaze the window
        pg.display.flip()    

    def even_control_infection(self,event):
        rtn_draw, rtn_discard = self.InfectionCard.handle_event(event)
        
        return rtn_draw, rtn_discard
    
    def even_control_player(self, event):
        self.rsp_player = ''
        for player in self.Players:
            r = player.handle_event(event)
            if r: 
                self.rsp_player = player        
    
    def even_control_city(self, event):
        self.rsp_city = ''
        for city in self.cities:
            r = self.cities[city].handle_event(event)
            if r:
                self.rsp_city = city     
    
    
    def event_respond_infection(self, rtn_draw, rtn_discard):
        
        # for infection part, highlight the city
            # either for new infection or user click on city name

        if rtn_discard:
            self.cities[rtn_discard].active = True                
                
        if rtn_draw:
            self.cities[rtn_draw].active = True
            self.cities[rtn_draw].infect(self.cities[rtn_draw].color, 1)        
            
    def event_respond_infection_initial(self, rtn_draw, rtn_discard, i):
        if rtn_discard:
            self.cities[rtn_discard].active = True                
                
        if rtn_draw:
            self.cities[rtn_draw].active = True
            self.cities[rtn_draw].infect(self.cities[rtn_draw].color, i)           
        