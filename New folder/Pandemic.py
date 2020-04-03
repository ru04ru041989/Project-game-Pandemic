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
disease, disease_summary, find_cure = initial_disease(dis_cube_num, disease_size)

# infection card
infection_card, infection_card_img, infection_discard_img = initial_infection_card(cities)
infection_discard = []

# infection indicater
infection_rate_text, expose_time_text = initial_infection_indicater()

# players
players = initial_player(cities)

# player card
player_card, player_card_img, player_card_discard = initial_player_card(cities)

# tips and control bottom
tips = initial_tip()
OK_bottom = ControlBottom()

#####################
#####################

# set up game control
game_control = {'is_infection_phase': True,
                'is_infect_city' : False, 
                
                'is_player_get_card' : False
                }

for v in game_control.values():
    if v:
        OK_bottom.set_select(True)

##########################
# test: let the first city get infection
#c_name = infection_card[0].name




######################################################
######################################################
# game start

clock = pg.time.Clock()

game_on = True
while game_on:
    
    screen.fill(bg_color)
    WorldMap.display(screen)
    
    # infection card
    infection_card_img.update_select(game_control['is_infection_phase'])
    infection_card_img.display(screen)
    infection_discard_img.display(screen)

    if infection_discard:
        infection_discard[-1].display(screen)
        
    # player card
    player_card_img.display(screen)
    player_card_discard.display(screen)
    player_card[1].display(screen)
            
    # infection indicater
    infection_rate_text.display(screen)
    expose_time_text.display(screen)
    
    # disease summary
    for dis in disease_summary.values():
        dis.display(screen, is_fill = True)
    for cure in find_cure.values():
        cure.display(screen, is_fill = True)

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

    # tips
    for tip in tips:
        tips[tip].display(screen)
    OK_bottom.display(screen)

### event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        
        active_city = ''
        for city in cities:
            cities[city].handle_event(event)
            if cities[city].rtn_active():
                active_city = cities[city]
        
        active_player=''
        for player in players:
            player.pawn.handle_event(event)
            player.area.handle_event(event)
            if player.rtn_active():
                active_player = player


        if infection_discard:
            infection_discard[-1].handle_event(event)
        
        active_player_card = ''
        for card in player_card:
            card.handle_event(event)
            if card.rtn_active():
                active_player_card = card
                
            
    #----------------------------------- using ok bottom click as moving marker to next step
        #check if OK got click
        OK_bottom.area.handle_event(event)
    #---------------------------------------------------------------------------------
        
        
### after event


    # if click on infection card or play card
    rtn_infection_card = ''
    if infection_discard:
        rtn_infection_card = infection_discard[-1].rtn_target()
    
    rtn_player_card = ''
    if active_player_card:
        rtn_player_card = active_player_card.rtn_target()

    # activate the city
    hightlight_city(cities, rtn_infection_card, rtn_player_card)
    
    # tip update
    city_tip_update(tips, target = active_city, screen=screen)
    player_tip_update(tips, player_target = active_player, 
                      player_card_target = active_player_card, screen=screen)
    

### game control > those function only executive once till next round
    # add player card to hands
    player_get_card(game_control, players[0], player_card[0])
    
    #-------------------------------------------------------------------------------- actually infect the city
    # infect city
    infect_city(game_control, OK_bottom, cities, disease, infection_card, infection_discard, repeat=3)
    #---------------------------------------------------------------------------------




    clock.tick(FPS)
    pg.display.flip() 
    
pg.quit()