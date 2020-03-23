import csv
import pygame as pg

from feature import City, Player
from settings import Settings

settings = Settings()

def cities_setup(ct_map, ct_link):
    cities = {}
    cities_ls = []
    with open(ct_map) as city_map:
        content = csv.reader(city_map, delimiter=',')
        for row in content:
            if row[1] in ['r','b','k','y']:
                cities[row[0]] = City(row[1], int(row[2]), int(row[3]), int(row[4]))
                cities_ls.append(row[0])
                
    with open(ct_link) as city_link:
        content = csv.reader(city_link, delimiter=',')
        for row in content:
            if row[1] in cities_ls:
                cities[row[0]].add_link(row[1])
    return cities, cities_ls

def text_setup(text, pos, size = 48, bg_color = settings.bg_color):
    font = pg.font.SysFont('Arial',size, bold = True)
    txt = font.render(text, True, (0, 0, 0), bg_color)
    textRect = txt.get_rect()
    textRect.center = pos
    return txt, textRect

def player_confirm(screen, footer_y, pos_input):

    play_setup_done = False
    play_setup_reset = False
    
    if pos_input:
        
        if pos_input[1] <= footer_y + 20 and pos_input[1] >=  footer_y - 20:
            if pos_input[0] >= (settings.screen_width // 2) - 300 - 40 and\
                pos_input[0] <= (settings.screen_width // 2) - 300 + 40:
                    play_setup_reset = True        
        
        if pos_input[1] <= footer_y+20 and pos_input[1] >= footer_y-20:
            if pos_input[0] >= (settings.screen_width // 2) + 300 - 40 and\
                pos_input[0] <= (settings.screen_width // 2) + 300 + 40:
                    play_setup_done = True
    
    return play_setup_reset, play_setup_done

def player_setup(screen, input_box, pos_input, setting_para, max_player):
    Q1_y, Q2_y = setting_para[:2]
    footer_y = setting_para[-1]
    
    Q1, Q1Rect = text_setup('How many player?  (Max = ' + str(max_player) + ')', 
                            (settings.screen_width // 2 - 100, Q1_y))
    Q2, Q2Rect = text_setup('Please choose charactors, if not enougth, will fill up randonly', 
                            (settings.screen_width // 2, Q2_y))
    clear_text, clear_Rect = text_setup(' clear ', ((settings.screen_width // 2) - 300, footer_y), 
                              36, bg_color=settings.WHITE)
    next_text, next_Rect = text_setup(' next ', ((settings.screen_width // 2) + 300, footer_y), 
                              36, bg_color=settings.WHITE)
    
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
        
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos_input = pg.mouse.get_pos()
    
        input_box.handle_event(event)
        
    input_box.update()
    
    input_box.draw(screen)
    screen.blit(Q1, Q1Rect)
    screen.blit(Q2, Q2Rect)
    screen.blit(clear_text, clear_Rect)
    screen.blit(next_text, next_Rect)
    
    play_setup_reset, play_setup_done = player_confirm(screen, footer_y, pos_input)
        
    try:
        player_number =  int(input_box.text)
        if player_number > max_player:
            play_setup_done = False
    except:
        player_number = 0
        play_setup_done = False
    
    return  play_setup_reset, play_setup_done, player_number


pg.init()
FONT = pg.font.Font(None, 32)  
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
        



