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

# prepare labs
labs = initial_lab()
cities['atlanta'].build_lab(labs.pop())
# prepare disease
disease, find_cure = initial_disease(dis_cube_num, disease_size)
disease_cube_summary, disease_cube_summary_title  = initial_disease_summary()

# infection card
infection_card, infection_card_img, infection_discard_img = initial_infection_card(cities)
infection_discard = []
cur_infection_card = ''

# infection indicater
lab_indicater, infection_rate_text, expose_time_text = initial_indicater(infect_rate, expose_time, labs)
cur_infect_rate, cur_expose_time = infect_rate, expose_time
cur_lab_num = len(labs)

# players
players = initial_player(cities)

# player card
player_card, player_card_img, player_card_discard = initial_player_card(cities)
player_card_active = []
player_discard = []
cur_player_card = ''
# tips and control bottom
tips = initial_tip()
OK_bottom = ControlBottom()

#####################
#####################

# set up game control
#game_control = {'infection_phase_rep': infect_rate,
#                'is_infection_phase': [False, False],
#                'is_infect_city' : [False, False], 
                
#                'player_get_card_phase_rep': player_card_per_round,
#                'is_player_get_card_phase' : [True, False],
#                'is_player_draw_card' : [False, False],
#                'is_player_get_card' : [False, False]
#                }

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
    infection_card_img.update_select(game_control['is_infection_phase'][0])
    infection_card_img.display(screen)
    infection_discard_img.display(screen)

    if infection_discard:
        infection_discard[-1].display(screen)
        
    # player card
    player_card_img.update_select(game_control['is_player_get_card_phase'][0])
    player_card_img.display(screen)
    player_card_discard.display(screen)
    
            
    # indicater
    # update indicater
    if cur_infect_rate != infect_rate or cur_expose_time != expose_time or cur_lab_num != len(labs):
        lab_indicater, infection_rate_text, expose_time_text = initial_indicater(infect_rate, expose_time, labs)
        cur_infect_rate, cur_expose_time = infect_rate, expose_time
        cur_lab_num = len(labs)
    
    lab_indicater.display(screen)
    infection_rate_text.display(screen)
    expose_time_text.display(screen)
    
    # disease summary
    disease_cube_summary_title.display(screen, is_fill=True)
    for summary in disease_cube_summary.values():
        summary.display(screen)
    
    for cure in find_cure.values():
        cure.display(screen, is_fill = True)

    # city
    for city in cities:
        cities[city].display_before(screen)
    for city in cities:
        cities[city].display(screen)
        cities[city].display_after(screen)
    
    # player
    for player in players:
        player.display(screen)

    # tips
    for tip in tips:
        tips[tip].display(screen)

    # game control
    for v in game_control.values():
        if v:
            OK_bottom.set_select(True)
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
        
        if cur_infection_card:
            cur_infection_card.handle_event(event)
        
        active_player_card = ''
        for card in player_card_active:
            card.handle_event(event)
            if card.rtn_active():
                active_player_card = card
    
    #----------------------------------- using ok bottom click as moving marker to next step
        #check if OK got click
        OK_bottom.area.handle_event(event)
    #---------------------------------------------------------------------------------
    

        
### after event


### game control > those function only executive once till next round
    # draw player phase, show the card, add player card to hands
    
    cur_player_card_temp = player_get_card(game_control['player_draw'], OK_bottom, 
                                           players[0], player_card, player_card_active, cur_player_card,tips)
    if cur_player_card_temp:
        cur_player_card = cur_player_card_temp
    if cur_player_card:
        cur_player_card.display(screen)

    #-------------------------------------------------------------------------------- actually infect the city
    # infect city
    cur_infection_card_temp = infect_city(game_control['normal_infection'], OK_bottom, cities, disease, 
                                          infection_card, infection_discard, cur_infection_card,
                                        disease_cube_summary,tips,cur_infect_rate, 
                                        repeat=infection_disease_num['normal_infection'])
    if cur_infection_card_temp:
        cur_infection_card = cur_infection_card_temp
    if cur_infection_card:
        cur_infection_card.display(screen)    
    
    #---------------------------------------------------------------------------------



    # if click on infection card or play card
    rtn_infection_card = ''
    if infection_discard:
        rtn_infection_card = infection_discard[-1].rtn_target()
    
    cur_infection_city = cur_infection_card.rtn_target() if cur_infection_card else ''
    
    rtn_player_card = ''
    if active_player_card:
        rtn_player_card = active_player_card.rtn_target()

    # activate the city
    hightlight_city(cities, rtn_infection_card, rtn_player_card, cur_infection_city)
    
    
    # update info
    #-----------------------------------------------------------------------------
    # tip update
    city_tip_update(tips, target = active_city, screen=screen)
    player_tip_update(tips, player_target = active_player, 
                      player_card_target = active_player_card, screen=screen)
    
    

        



    clock.tick(FPS)
    pg.display.flip() 
    
pg.quit()