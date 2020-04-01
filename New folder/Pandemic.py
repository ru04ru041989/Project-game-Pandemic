import sys
import csv
import random

import pygame as pg
from paramater import*

#from basic_feature import*
#from feature import*
from gamecontrol_fn import*


FPS = 30

pg.init()

# prepare screen 
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Pandemic")

# prepare world
WorldMap = initial_map(map_size)

# prepare city
cities, cities_ls = initial_city(city_size)

# prepare disease
disease = initial_disease(dis_cube_num, disease_size)

# infection card
infection_card, infection_card_img = initial_infection_card(cities_ls, infection_card_img_pos, infection_card_size)

# players
players = initial_player(cities)

#####################
#####################

# test: let the first city get infection
#c_name = infection_card[0].name
infect_city(cities, disease, infection_card, repeat=3)





######################################################
######################################################
# game start

clock = pg.time.Clock()

game_on = True
while game_on:
    
    screen.fill(bg_color)
    WorldMap.display(screen)
    
    # infection card
    infection_card_img.display(screen)
    infection_card[0].display(screen)

    # city
    for city in cities:
        cities[city].display_link(screen)
    for city in cities:
        cities[city].display(screen)
        cities[city].display_cityname(screen)
        cities[city].display_disease(screen)   
    
    # player
    for player in players:
        player.display(screen)

    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        
        
        for city in cities:
            cities[city].handle_event(event)
        
        
        for player in players:
            player.pawn.handle_event(event)
            player.area.handle_event(event)

    
    clock.tick(FPS)
    pg.display.flip() 
    
pg.quit()