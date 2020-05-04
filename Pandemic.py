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

##############################################################################
##############################################################################
# pre_game setting [selecting how many player and the characher


##############################################################################
##############################################################################
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

'''infection_discard_borad = DisplayBoard(x=player_control_board_pos[0]+50, y=player_control_board_pos[1]-100,
                                        w=player_control_board_size[0]-100, h=player_control_board_size[1]+100,
                                        to_drag=True, show_summary=False)
infection_discard_borad.add_title('Infection Discard')'''

# infection indicater
lab_indicater, infection_rate_text, expose_time_text = initial_indicater(infect_rate, expose_time, labs)
cur_infect_rate, cur_expose_time = infect_rate, expose_time
cur_lab_num = len(labs)

# players
players = initial_player(cities)

# player card
player_card, player_card_img, player_card_discard_img = initial_player_card(cities)
# distribute player's hand card

# adding epidemic_card


player_card_active = []
player_card_discard = []
cur_player_card = ''

# tips
tips = initial_tip()

# -----------------------------------------------------------------  game control
# control bottom
OK_bottom = ControlBottom('OK', OK_bottom_pos, OK_bottom_size)
USE_bottom = ControlBottom('USE', USE_bottom_pos, USE_bottom_size)
# -----------------------------------------------------------------  interact board
display_board = initial_game_board()

# player board
'''player_board = PlayerBoard()'''
display_board['player'].add_player_color(players[3 % 5].color)

## special case control
# hand card over limit
'''is_hand_over_limit = False
hand_over_limit = SelectBoard(w=player_control_board_size[0] / 2, to_drag=True)
hand_over_limit.add_title('Holding too many cards, discard one')'''

#####################
#####################

# set up game control

game_control = initial_game_control()

# first event = initial_infection1---------------------------debug mode, start at normal infection
suspended_task = assign_next_step(game_control, 'player_round', OK_bottom)
display_board['player'].is_close = False

total_player = 5  # -----------------------------------------------------------------this should be set in advance
cur_playNO = 3

pnt_game_control(game_control, suspended_task)
# ------------------------------------------------------------------------  testing new item


######################################################
######################################################
# game start

clock = pg.time.Clock()

game_on = True
while game_on:

    cur_player = players[cur_playNO % 5]

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
    if game_control['player_round'].rtn_action_active():
        display_board['player'].add_player_color(cur_player.color)

    display_board['player'].display(screen, players, cur_player, cities)

    # game control

    # bottoms

    OK_bottom.display(screen)
    USE_bottom.display(screen)

    # special case
    display_board['hand_limit'].display(screen)

    display_board['infection_discard'].display(screen)

    # ---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------
    ####################################################################################
    ### event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            ###################################### print for debugging
            sys.exit()

        active_city = ''
        for city in cities.values():
            # re-set select
            city.update_select(False)
            city.handle_event(event)
            if city.rtn_active():
                active_city = city

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

        infection_discard_img.handle_event(event)

        if cur_infection_card:
            cur_infection_card.handle_event(event)

        active_player_card = ''
        for card in player_card_active:
            card.handle_event(event)
            if card.rtn_active():
                active_player_card = card

        # player_board
        if game_control['player_round'].rtn_action_active():
            display_board['player'].update_city_pick(players, cur_player, active_city, cities)

        display_board['player'].handle_event(event, players, cur_player, cities)

        # ----------------------------------- using ok bottom click as moving marker to next step
        OK_bottom.handle_event(event)
        if OK_bottom.rtn_click():
            for city in cities.values():
                city.is_shake = False
        # ------------------------------------ using use bottom click to see if want to use special card
        USE_bottom.set_select(False)
        if active_player_card:
            if active_player_card.type == 'special' and \
                    not check_if_process('expose_infection') and not check_if_process('normal_infection'):
                # active USE_bottom
                USE_bottom.set_select(True)
                # keep track if USE click
                USE_bottom.handle_event(event)

        ### special case control

        # player has too many cards
        display_board['hand_limit'].handle_event(event)

        # if click on infection discard
        display_board['infection_discard'].handle_event(event)
    # ---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------

    ####################################################################################
    ### after event

    #############################################     ## player's action
    if check_if_process(game_control, 'player_round'):
        game_board_chosen('player', display_board)
        tip_text = 'Player ' + str((cur_playNO % total_player) + 1) + ': ' + cur_player.name + "'s round"
        control_tip_update(tips, tip_text)

        # if no need to cost card, double-click to move to near city
        if [city for city in cities.values() if city.double_click]:
            db_click_city = [city for city in cities.values() if city.double_click][0]
            db_click_city.double_click = False

            action, subboard = display_board['player'].rtn_status()
            # if the action is 'Move', and the ppl who move don't cost, then move it
            if action == 'Move':
                ppl = cur_player
                if cur_player.move_other:
                    if subboard:
                        player_move = subboard.pop(0)
                        if player_move:
                            ppl = [player for player in players if player.name == player_move][0]

                # figure if need card, and which player choose if there is multi card can be used
                if (db_click_city in ppl.city.city_link) or (db_click_city.lab and ppl.city.lab) or \
                        (cur_player.move_other and db_click_city in [player.city for player in players]):
                    if db_click_city != ppl.city:
                        move(cur_player, ppl, db_click_city, '',
                             player_card_active, player_card_discard)

        # player click on confirm
        elif display_board['player'].rtn_active():
            action, subboard = display_board['player'].rtn_status()
            display_board['player'].bottom.unclick()

            if action == 'Move':
                target_city = display_board['player'].city_pick
                if target_city:
                    # figure which player to move
                    ppl = cur_player
                    if cur_player.move_other:
                        if subboard:
                            player_move = subboard.pop(0)
                            if player_move:
                                ppl = [player for player in players if player.name == player_move][0]

                    # figure if need card, and which player choose if there is multi card can be used
                    if target_city in ppl.city.city_link:
                        move(cur_player, ppl, target_city, '',
                             player_card_active, player_card_discard)
                    elif target_city.lab and ppl.city.lab:
                        move(cur_player, ppl, target_city, '',
                             player_card_active, player_card_discard)
                    elif cur_player.move_other and target_city in [player.city for player in players]:
                        if target_city != ppl.city:
                            move(cur_player, ppl, target_city, '',
                                 player_card_active, player_card_discard)
                    else:
                        if subboard:
                            card_need = subboard.pop(0)
                            for card in cur_player.hand:
                                if card.name == card_need:
                                    move(cur_player, ppl, target_city, card,
                                         player_card_active, player_card_discard)
                else:
                    summary_text = ['Please choose city to move']

            if action == 'Build Lab':
                if cur_player.city.lab:
                    summary_text = ['City has lab already']
                else:
                    if labs:
                        if cur_player.building_action:
                            build(cur_player, '', '', labs, player_card_active, player_card_discard)
                        else:
                            for card in cur_player.hand:
                                if card.name == cur_player.city.txt:
                                    build(cur_player, card, '', labs, player_card_active, player_card_discard)
                    else:
                        if subboard:
                            for city in cities:
                                if city.txt == subboard.pop():
                                    rp_lab = city
                            if cur_player.building_action:
                                build(cur_player, '', rp_lab, labs, player_card_active, player_card_discard)
                            else:
                                for card in cur_player.hand:
                                    if card.name == cur_player.city.txt:
                                        build(cur_player, card, rp_lab, labs, player_card_active, player_card_discard)

            if action == 'Find Cure':
                summary_text = ['Not enough city card',
                                'Need ' + str(cur_player.cure_need) + ' same color cards']
                if not cur_player.city.lab:
                    summary_text = ['This City has no lab']
                else:
                    if subboard:
                        board = subboard.pop(0)
                        board = board if isinstance(board, list) else [board]
                        if len(board) >= cur_player.cure_need:
                            card_to_use = []
                            for card in cur_player.hand:
                                if card.name in board:
                                    card_to_use.append(card)
                            discover_cure(cur_player, card_to_use, is_cure, find_cure, player_card_active,
                                          player_card_discard)

            if action == 'Treat disease':
                treat_ls = [k for k, v in cur_player.city.disease.items() if len(v) != 0]
                if not len(treat_ls):
                    summary_text = ['City has no disease',
                                    'Please choose another action']
                else:
                    if len(treat_ls) == 1:
                        treat(cur_player, treat_ls[0], disease, is_cure, disease_cube_summary)
                    elif subboard:
                        treat(cur_player, subboard.pop(0), disease_cube_summary)
                    else:
                        summary_text = ['City has more than one disease',
                                        'Please choose which one to treat']

            if action == 'Share info':
                board1 = subboard.pop(0) if subboard else None
                board2 = subboard.pop(0) if subboard else None
                if board1 and board2:
                    for player in players:
                        if player.name == board1:
                            player_trade = player
                    for card in cur_player.hand:
                        if card.name == board2:
                            card_trade = card
                    share(cur_player, player_trade, card_trade)
                else:
                    summary_text = ['Make sure you finish choosing', 'before click confirm']

            display_board['player'].get_subboard(action, players, cur_player, display_board['player'].city_pick, cities)

        # player use up all the action: action phase is over, start player get card phase
        if cur_player.action_used == cur_player.action or display_board['player'].rtn_done():
            game_control['player_round'].action = False
            assign_next_step(game_control, 'player_draw', OK_bottom)
            display_board['player'].cur_move_ppl = ''
            display_board['player'].city_pick = ''
            display_board['player'].done_bottom.unclick()
            display_board['player'].is_close = True

    ############################################      ## player get card phase
    cur_player_card_temp = player_get_card(OK_bottom,
                                           cur_player, player_card, player_card_active, cur_player_card, tips,
                                           game_control, cur_step='player_draw', next_step='check_player')
    if cur_player_card_temp:
        cur_player_card = cur_player_card_temp

    # ------------------------------------------------if this player card is an epidemic card...
    if cur_player_card:
        if cur_player_card.name == 'epidemic':
            # put the card to discard
            cur_player_card.update_pos(x=player_card_img_pos[0] + player_card_size[0] + 15,
                                       y=player_card_img_pos[1])
            player_card_discard.append(cur_player_card)
            cur_player_card = ''

            # add the cur task to suspended, and assign to expose_infection
            suspended_task = assign_next_step(game_control, 'expose_infection', OK_bottom)

    ############################################      ## expose_infection phase
    # check if expose_infection phase
    if check_if_process(game_control, 'expose_infection'):
        cur_infection_card_temp = helper_infect_city(OK_bottom,
                                                     cities, disease, infection_card, infection_discard,
                                                     cur_infection_card,
                                                     disease_cube_summary, tips,
                                                     game_control, 'expose_infection', suspended_task,
                                                     'Press OK to start epidemic!')
        if cur_infection_card_temp:
            if isinstance(cur_infection_card_temp, int) or cur_infection_card_temp == 'done':
                cur_infection_card = ''
                infect_rate += 1
                game_control['normal_infection'].paramater['rep'] += 1
                game_control['normal_infection'].paramater['rep_reset'] += 1
                # add the expose time
                if isinstance(cur_infection_card_temp, int):
                    expose_time += cur_infection_card_temp
            else:
                cur_infection_card = cur_infection_card_temp

    # ------------------------------------------------if any  player has too many card
    over_hand_limit = False
    for player in players:
        if len(player.hand) > player.handlimit:
            over_hand_limit = True

    if over_hand_limit:
        if not check_if_process(game_control, 'hand_limit'):
            suspended_task = assign_next_step(game_control, 'hand_limit', OK_bottom)

    ############################################      ## hand_limit phase
    if check_if_process(game_control, 'hand_limit'):
        OK_bottom.turn_off()
        control_tip_update(tips, 'Discard one card to continue')

        # display another interaction board and select one card to discard
        game_board_chosen('hand_limit', display_board)

        # check which player's hand over limit
        player_hand_over = ''
        for player in players:
            if len(player.hand) > player.handlimit:
                player_hand_over = player

        card_ls = [card.name for card in player_hand_over.hand]
        card_color = [card.color for card in player_hand_over.hand]
        if display_board['hand_limit'].rtn_ls_content() != card_ls:
            display_board['hand_limit'].add_ls(card_ls, card_color)

        # player confirm which card to discard
        if display_board['hand_limit'].rtn_confirm():
            card_pick = [card for card in player_hand_over.hand if
                         card.name == display_board['hand_limit'].rtn_select()]
            if card_pick:
                card = card_pick[0]
                discard_card(player_hand_over, card, player_card_active, player_card_discard)
                game_control['hand_limit'].action = False
                # assign next game step
                assign_next_step(game_control, suspended_task, OK_bottom)

    #############################################      ## check cur player round
    if game_control['check_player'].rtn_action_active():
        cur_player.action_used = 0
        cur_playNO += 1
        assign_next_step(game_control, 'normal_infection', OK_bottom)
        game_control['check_player'].action = False

    ##------------------------------------------------------------------------------------------------------
    ## infection phase
    cur_infection_card_temp = infect_city(OK_bottom,
                                          cities, disease, infection_card, infection_discard,
                                          cur_infection_card,
                                          disease_cube_summary, tips,
                                          game_control)

    if isinstance(cur_infection_card_temp, int):
        expose_time += cur_infection_card_temp
    else:
        if cur_infection_card_temp:
            cur_infection_card = cur_infection_card_temp

    ##--------------------------------------------------------------------------------------------  start a new round

    #### info update

    # ------------------------------------------------if click on infection discard pile
    if infection_discard_img.rtn_click():
        if not check_if_process(game_control, 'infection_discard_view'):
            suspended_task = assign_next_step(game_control, 'infection_discard_view', OK_bottom)

    ############################################      ## infection_discard_view phase
    if check_if_process(game_control, 'infection_discard_view'):
        game_board_chosen('infection_discard', display_board)

        card = [x.name for x in infection_discard]
        card_color = [x.area.active_color for x in infection_discard]

        # update board if content list change
        if display_board['infection_discard'].list_content != card:
            display_board['infection_discard'].add_ls(card, card_color, row_limit=6, is_seq=True)

    # if player close the infection_discard:
    if display_board['infection_discard'].close.click:
        display_board['infection_discard'].close.unclick()
        game_control['infection_discard_view'].action = False
        display_board['infection_discard'].reset()
        assign_next_step(game_control, suspended_task, OK_bottom)

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
    hightlight_city(cities,
                    [rtn_infection_card, rtn_player_card, cur_infection_city,
                     display_board['infection_discard'].rtn_select()])

    # update info
    # -----------------------------------------------------------------------------
    # tip update
    city_tip_update(tips, target=active_city, screen=screen)
    player_tip_update(tips, player_target=active_player,
                      player_card_target=active_player_card, screen=screen)

    clock.tick(FPS)
    pg.display.flip()

pg.quit()
