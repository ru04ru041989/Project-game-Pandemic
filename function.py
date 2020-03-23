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

def player_setup(screen, pos_input, player_number):
    # let user decise how many players
        # display option: form 2-4
        # display charactor for choose
            # if choose less then players, randomly fill up
    
    Q1, Q1Rect = text_setup('How many player?', (settings.screen_width // 2, 60))
    Q2, Q2Rect = text_setup('Please choose charactors, if not enougth, will fill up randonly', 
                            (settings.screen_width // 2, 250))
    
    A11, A11Rect = text_setup('  2  ', ((settings.screen_width // 2) - 100, 180), 
                              36, bg_color=settings.WHITE)
    A12, A12Rect = text_setup('  3  ', ((settings.screen_width // 2) , 180), 
                              36, bg_color=settings.WHITE)
    A13, A13Rect = text_setup('  4  ', ((settings.screen_width // 2) + 100, 180), 
                              36, bg_color=settings.WHITE)
    player_number = player_number
    if pos_input or player_number:
        if pos_input[1] <= 180+20 and pos_input[1] >= 180-20 or player_number:
            if (pos_input[0] >= (settings.screen_width // 2) -120 and \
                pos_input[0] <= (settings.screen_width // 2) -80) or player_number == 2:
                A11, A11Rect = text_setup('  2  ', ((settings.screen_width // 2) - 100, 180), 
                                                36, bg_color=settings.GREEN)
                player_number = 2
                
            elif (pos_input[0] >= (settings.screen_width // 2) -20 and \
                pos_input[0] <= (settings.screen_width // 2) +20) or player_number == 3:
                A12, A12Rect = text_setup('  3  ', ((settings.screen_width // 2) , 180), 
                                                36, bg_color=settings.GREEN)
                player_number = 3
                
            elif (pos_input[0] >= (settings.screen_width // 2) +80 and \
                pos_input[0] <= (settings.screen_width // 2) +120) or player_number == 4:
                A13, A13Rect = text_setup('  4  ', ((settings.screen_width // 2) + 100, 180), 
                                                36, bg_color=settings.GREEN)
                player_number = 4           
    
    screen.blit(Q1, Q1Rect)
    screen.blit(Q2, Q2Rect)
    screen.blit(A11, A11Rect)  
    screen.blit(A12, A12Rect)  
    screen.blit(A13, A13Rect)
    
    return player_number


def player_confirm(screen, pos_input):
    clear_text, clear_Rect = text_setup(' clear ', ((settings.screen_width // 2) - 300, 670), 
                              36, bg_color=settings.WHITE)
    next_text, next_Rect = text_setup(' next ', ((settings.screen_width // 2) + 300, 670), 
                              36, bg_color=settings.WHITE)
    
    play_setup_done = False
    play_setup_reset = False
    
    if pos_input:
        
        if pos_input[1] <= 670+20 and pos_input[1] >= 670-20:
            if pos_input[0] >= (settings.screen_width // 2) - 300 - 40 and\
                pos_input[0] <= (settings.screen_width // 2) - 300 + 40:
                    play_setup_reset = True        
        
        if pos_input[1] <= 670+20 and pos_input[1] >= 670-20:
            if pos_input[0] >= (settings.screen_width // 2) + 300 - 40 and\
                pos_input[0] <= (settings.screen_width // 2) + 300 + 40:
                    play_setup_done = True
    
    screen.blit(clear_text, clear_Rect)
    screen.blit(next_text, next_Rect)
    
    return play_setup_reset, play_setup_done