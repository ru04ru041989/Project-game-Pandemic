import sys
import csv
import random

import pygame as pg
from paramater import *

# from basic_feature import*
# from feature import*
from gamecontrol_fn import *

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
disease_cube_summary, disease_cube_summary_title = initial_disease_summary()

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
player_card, player_card_img, player_card_discard_img = initial_player_card(cities)
player_card_active = []
player_card_discard = []
cur_player_card = ''

# tips
tips = initial_tip()

#-----------------------------------------------------------------  game control
# control bottom
OK_bottom = ControlBottom('OK', OK_bottom_pos, OK_bottom_size)
USE_bottom = ControlBottom('USE', USE_bottom_pos, USE_bottom_size)
#-----------------------------------------------------------------  interact board
# player board
player_board = PlayerBoard()
player_subboard1 = subboard(1)
player_subboard2 = subboard(2)
player_board_summary = PlayerBoardSummary()
player_board_key = ''

## special case control
# hand card over limit
is_hand_over_limit = False
hand_over_limit = SelectBoard()
hand_over_limit.add_title('Holding too many cards, discard one')

#####################
#####################

# set up game control

game_control = initial_game_control()

# first event = initial_infection1---------------------------debug mode, start at normal infection
assign_next_step(game_control, 'normal_infection',OK_bottom)
cur_player = players[1]
'''
for k, v in game_control.items():
    print(k)
    print(v.id)
    print(v.paramater)
    print(v.action)
    print('--------')
'''

###################################################################################  testing new item
test = SelectBoard()
test.add_title('testing selectboard sjeialjasidjfilasdjfleij')
test.add_ls(['a','b', 'c', 'd', 'e', 'f', 'g'], keep_active=True)


######################################################
######################################################
# game start

clock = pg.time.Clock()

game_on = True
while game_on:

    screen.fill(bg_color)
    WorldMap.display(screen)

    # infection card
    infection_card_img.update_select(game_control['normal_infection'].rtn_action_active()[0])
    infection_card_img.display(screen)
    infection_discard_img.display(screen)

    if infection_discard:
        infection_discard[-1].display(screen)

    if cur_infection_card:
        cur_infection_card.display(screen)

    # player card
    player_card_img.update_select(game_control['player_draw'].rtn_action_active()[0])
    player_card_img.display(screen)
    player_card_discard_img.display(screen)

    if player_card_discard:
        player_card_discard[-1].display(screen)

    if cur_player_card:
        cur_player_card.display(screen)

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
        cure.display(screen, is_fill=True)

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

    # player board
    player_round_display(screen, game_control['player_round'].rtn_action_active()[0],
                         player_board, player_board_summary,
                         player_subboard1, player_subboard2)

    # game control

    # bottoms
    for val in game_control['player_draw'].action.values():
        if val[0]:
            OK_bottom.set_select(True)
    for key in infection_disease_num:
        for val in game_control[key].action.values():
            if val[0]:
                OK_bottom.set_select(True)
    OK_bottom.display(screen)
    USE_bottom.display(screen)

    # special case
    if is_hand_over_limit:
        hand_over_limit.display(screen)

    # ---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------
    ####################################################################################
    ### event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            ###################################### print for debugging
            sys.exit()

        active_city = ''
        for city in cities:
            # re-set select
            cities[city].update_select(False)
            cities[city].handle_event(event)
            if cities[city].rtn_active():
                active_city = cities[city]

        active_player = ''
        for player in players:
            player.pawn.handle_event(event)
            player.area.handle_event(event)
            if player.rtn_active():
                active_player = player
                # let the city where this player on also active
                active_player.city.update_select(True)

        if infection_discard:
            infection_discard[-1].handle_event(event)

        if cur_infection_card:
            cur_infection_card.handle_event(event)

        active_player_card = ''
        for card in player_card_active:
            card.handle_event(event)
            if card.rtn_active():
                active_player_card = card

        # associated with board (which board display, which board collect event)
        player_round_handel_event(event, game_control['player_round'].rtn_action_active()[0],
                                  player_board, player_board_summary,
                                  player_subboard1, player_subboard2)

        # ----------------------------------- using ok bottom click as moving marker to next step
        OK_bottom.handle_event(event)
        # ------------------------------------ using use bottom click to see if want to use special card
        USE_bottom.set_select(False)
        if active_player_card:
            if active_player_card.type == 'special':
                # active USE_bottom
                USE_bottom.set_select(True)
                USE_bottom.display(screen)
                # keep track if USE click
                USE_bottom.handle_event(event)

        ### special case control

        # player has too many cards
        if is_hand_over_limit:
            hand_over_limit.handel_event(event)

    # ---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------

    ### after event

    ## player's action
    if game_control['player_round'].action['is_player_round_phase'][0]:
        # update player control board ---------------------------------------------------------debug
        player_board_key = player_subboard_update(player_board, player_subboard1, player_subboard2,
                                                  player_board_summary,
                                                  players, cur_player, player_board_key,
                                                  active_city, cities, labs)
        # player click on confirm
        if player_board_summary.rtn_active():
            action, target = player_action_confirm(players, cur_player, labs, cities,
                                                   player_board, player_subboard1, player_subboard2,
                                                   player_board_summary)
            if action == 'Move':
                move(cur_player, target[0], target[1], target[2],
                     player_card_active, player_card_discard)

            if action == 'Share':
                share(cur_player, target[0], target[1])

            if action == 'Cure':
                discover_cure(cur_player, target, is_cure, find_cure, player_card_active, player_card_discard)

            if action == 'Build':
                build(cur_player, target[0], target[1], labs, player_card_active, player_card_discard)

            if action == 'Treat':
                treat(cur_player, target, disease, is_cure, disease_cube_summary)

            player_subboard_update(player_board, player_subboard1, player_subboard2,
                                   player_board_summary,
                                   players, cur_player, player_board_key, active_city, cities, labs,
                                   force_update=True)

        # action phase is over, start player get card phase, setup the associated paramatar ---- after sweach player, reset action used
        if cur_player.action_used == cur_player.action:
            game_control['player_round'].action['is_player_round_phase'][0] = False
            assign_next_step(game_control, 'player_draw')


    ## player get card phase
    #----------------------------------------------------------
    # player get card
    cur_player_card_temp = player_get_card(OK_bottom,
                                           cur_player, player_card, player_card_active, cur_player_card, tips,
                                           game_control, cur_step='player_draw', next_step='player_round')
    if cur_player_card_temp:
        cur_player_card = cur_player_card_temp

    # ----------------------------------------------------------if this player card is an expose card...

    # ----------------------------------------------------------if this  player has too many card
    if len(cur_player.hand) <= cur_player.handlimit:
        is_hand_over_limit = False
        turn_OK_on(OK_bottom)

    else:
        turn_OK_off(OK_bottom)
        control_tip_update(tips, 'Discard one card to continue')
        # display another interaction board and select one card to discard
        is_hand_over_limit = True
        card_ls = [card.name for card in cur_player.hand]
        card_color = [card.color for card in cur_player.hand]
        if hand_over_limit.rtn_ls_content() != card_ls:
            hand_over_limit.add_ls(card_ls, card_color)

        if hand_over_limit.rtn_confirm():
            card_pick = [card for card in cur_player.hand if card.name == hand_over_limit.rtn_select()]
            if card_pick:
                card = card_pick[0]
                discard_card(cur_player, card, player_card_active, player_card_discard)




    ##------------------------------------------------------------------------------------------------------
    ## infection phase
    cur_infection_card_temp = infect_city(OK_bottom,
                                          cities, disease, infection_card, infection_discard,
                                          cur_infection_card,
                                          disease_cube_summary, tips,
                                          game_control)

    if cur_infection_card_temp:
        cur_infection_card = cur_infection_card_temp


    ##--------------------------------------------------------------------------------------------  start a new round

    #### info update

    # if click on infection card or play card
    rtn_infection_card = ''
    if infection_discard:
        rtn_infection_card = infection_discard[-1].rtn_target()

    cur_infection_city = cur_infection_card.rtn_target() if cur_infection_card else ''

    rtn_player_card = ''
    if active_player_card:
        if active_player_card.type == 'city':
            rtn_player_card = active_player_card.rtn_target()

    # activate the city
    hightlight_city(cities, rtn_infection_card, rtn_player_card, cur_infection_city)

    # update info
    # -----------------------------------------------------------------------------
    # tip update
    city_tip_update(tips, target=active_city, screen=screen)
    player_tip_update(tips, player_target=active_player,
                      player_card_target=active_player_card, screen=screen)

    clock.tick(FPS)
    pg.display.flip()

pg.quit()
