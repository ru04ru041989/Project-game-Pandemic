import sys
import csv
import random
import copy
import string

from basic_feature import *
from feature import *
from paramater import *


################################
#  initial
################################

def initial_map(map_size):
    WorldMap = ImgBox(x=0, y=0, w=map_size[0], h=map_size[1])
    WorldMap.add_img(filename='\\img\\world.jpg', size=map_size, as_rect=False)
    return WorldMap


def initial_city(city_size):
    cities, sudo_city = {}, {}
    cities_ls = []
    with open('city_map.csv') as city_map:
        content = csv.reader(city_map, delimiter=',')
        for row in content:
            if row[1] in ['r', 'b', 'k', 'y']:
                cities[row[0]] = City(cityname=row[0], citycolor=row[1], x=int(row[2]) + 10, y=int(row[3]) + 5,
                                      txt_up=int(row[4]))
                cities[row[0]].add_img(filename='\\img\\city_' + row[1] + '.png', size=city_size)
                cities_ls.append(row[0])
            if row[1] == 'w':
                sudo_city[row[0]] = [int(row[2]), int(row[3])]
    with open('city_link.csv') as city_link:
        content = csv.reader(city_link, delimiter=',')
        for row in content:
            if row[1] in cities or row[1] in sudo_city:
                if row[1] in cities:
                    cities[row[0]].add_link(cities[row[1]])
                else:
                    cities[row[0]].add_sudo_link(sudo_city[row[1]])

    # adding city link for those link with sudo_city
    cities['san francisco'].city_link.append(cities['tokyo'])
    cities['tokyo'].city_link.append(cities['san francisco'])
    cities['san francisco'].city_link.append(cities['manila'])
    cities['manila'].city_link.append(cities['san francisco'])
    cities['los angles'].city_link.append(cities['sydney'])
    cities['sydney'].city_link.append(cities['los angles'])

    return cities, cities_ls


def initial_lab():
    labs = []
    for i in range(lab_num):
        lab = Lab()
        labs.append(lab)

    return labs


def initial_disease(dis_cube_num, disease_size):
    disease = {}
    find_cure = {}
    for i, dis_color in enumerate(['r', 'b', 'k', 'y']):
        #
        dis_temp = [ImgBox() for j in range(dis_cube_num[dis_color])]
        for dis in dis_temp:
            dis.add_img(filename='\\img\\dis_' + dis_color + '.png', size=disease_size, to_center=False)
        disease[dis_color] = dis_temp

        #
        cure_temp = WordBox(w=disease_summary_size[0], h=disease_summary_size[1], as_rect=False)
        cure_temp.add_text(text='No Cure', size=12, color=WHITE)
        cure_temp.update_pos(x=disease_summary_pos[0] + i * disease_summary_size[0],
                             y=disease_summary_pos[1] + disease_summary_size[1])
        cure_temp.add_fill_color(BLACK)
        find_cure[dis_color] = cure_temp

    return disease, find_cure


def initial_disease_summary():
    disease_cube_summary = {}
    for i, dis_color in enumerate(['r', 'b', 'k', 'y']):
        dis_sum = DiseaseSummary()
        dis_sum.update_pos(x=disease_summary_pos[0] + i * disease_summary_size[0], y=disease_summary_pos[1])
        dis_sum.update_num(dis_cube_num[dis_color])
        dis_sum.add_fill_color(color_rbky[dis_color])
        disease_cube_summary[dis_color] = dis_sum

    disease_cube_summary_title = WordBox(w=disease_summary_size[0], h=disease_summary_size[1], as_rect=True)
    disease_cube_summary_title.add_text(text='Game Over if Disease = 0 !!!',
                                        size=16, color=WHITE, to_center=False)
    disease_cube_summary_title.update_pos(x=disease_summary_pos[0], y=disease_summary_pos[1] - disease_summary_size[1])
    disease_cube_summary_title.add_fill_color(BLACK)
    return disease_cube_summary, disease_cube_summary_title


def initial_infection_card(cities):
    infection_card = []
    for city in cities:
        card = InfectionCard(cities[city])
        infection_card.append(card)
    random.shuffle(infection_card)  # ------------------------------------------------ testing

    #
    infection_card_img = ImgBox(x=infection_card_img_pos[0], y=infection_card_img_pos[1],
                                w=infection_card_size[0], h=infection_card_size[1], thick=5, color=RED)
    infection_card_img.add_img(filename='\\img\\infectcard.png', size=infection_card_size, to_center=False)

    #
    infection_discard_img = SelectBox(x=infection_card_img_pos[0] + infection_card_size[0] + 10,
                                      y=infection_card_img_pos[1] - 5,
                                      w=infection_card_size[0] + 10, h=infection_card_size[1] + 10,
                                      keep_active=False, thick=0)
    infection_discard_img.update_color(SHADOW)

    return infection_card, infection_card_img, infection_discard_img


def initial_indicater(infect_rate, expose_time, labs):
    # lab
    lab_indicater = WordBox()
    lab_indicater.add_text(text='Rest of Lab number: ' + str(len(labs)), size=16, color=BLACK)
    lab_indicater.update_pos(x=lab_indicater_pos[0], y=lab_indicater_pos[1])

    # infection rate
    infection_rate_text = WordBox()
    infection_rate_text.add_text(text='Infection Rate: ' + str(infect_rate), size=18, color=BLACK)
    infection_rate_text.update_pos(x=infection_card_img_pos[0] + infection_card_size[0] * 0.5,
                                   y=infection_card_img_pos[1] - city_size[1])

    # expose_time
    expose_time_text = WordBox()
    expose_time_text.add_text(text='Expose Time: ' + str(expose_time) + ' /8', size=18, color=BLACK)
    expose_time_text.update_pos(x=infection_card_img_pos[0] + infection_card_size[0] * 0.5,
                                y=infection_card_img_pos[1] - city_size[1] * 2)
    return lab_indicater, infection_rate_text, expose_time_text


def initial_game_board():
    display_board = {}

    # infection discard board
    infection_discard_borad = DisplayBoard(x=player_control_board_pos[0] + 50, y=player_control_board_pos[1] - 100,
                                           w=player_control_board_size[0] - 100, h=player_control_board_size[1] + 100,
                                           to_drag=True, show_summary=False)
    infection_discard_borad.add_title('Infection Discard')
    display_board['infection_discard'] = infection_discard_borad

    # player board
    player_board = PlayerBoard()
    display_board['player'] = player_board

    # hand over limit
    hand_over_limit = SelectBoard(w=player_control_board_size[0] / 2, to_drag=True)
    hand_over_limit.add_title('Holding too many cards, discard one')
    display_board['hand_limit'] = hand_over_limit

    return display_board


def initial_player(cities):  # -----------------------------------------debug  start at taipei
    sci = Scientist()
    res = Researcher()
    med = Medic()
    dip = Dispatcher()
    ope = OperationsExpert()

    all_chara = [sci, res, med, dip, ope]

    # after user choose chara
    players = all_chara.copy()  # debug mode, display all for now

    for i, player in enumerate(players):
        player.playerNO_update(i + 1)
        player.pos_update(cities['taipei'])

    return players


# ---------------------------------------------- not adding sp card for debugging
def initial_player_card(cities):
    player_card = []

    # city card
    for city in cities:
        card = PlayerCard(cities[city])
        card.add_discribe(['1. Discard this card to move to this city',
                           '2. Discard this card to move to any city if you are in this city'])
        player_card.append(card)
    '''
    # special card
    for name, discribe in sp_player_card.items():
        card = SpPlayerCard(name)
        card.add_discribe(discribe)
        card.update_color(GREEN)
        player_card.append(card)
    '''

    player_card_img = ImgBox(x=player_card_img_pos[0], y=player_card_img_pos[1],
                             w=player_card_size[0], h=player_card_size[1], thick=5, color=RED)
    player_card_img.add_img(filename='\\img\\playercard.png', size=player_card_size, to_center=False)

    player_card_discard = SelectBox(x=player_card_img_pos[0] + player_card_size[0] + 10, y=player_card_img_pos[1] - 5,
                                    w=player_card_size[0] + 10, h=player_card_size[1] + 10,
                                    keep_active=False, thick=0)
    player_card_discard.update_color(SHADOW)

    return player_card, player_card_img, player_card_discard


def epidemic_card():
    card = SpPlayerCard('epidemic')
    card.add_discribe(['Infection Rate +1',
                       'draw infection card and infect the city',
                       'shuffle the discard infection pile and add back to infection pile'])
    card.update_color((0, 155, 0))
    card.epidemic()
    return card


def initial_tip():
    tips = {}
    for k, v in tip.items():
        t = Tip()
        t.update_rect(v[0], v[1], v[2], v[3])
        tips[k] = t

    tips['control'].update_text(title=' ', body=' ')
    return tips


# ----------------------------------------------####   add game control here
def initial_game_control():
    game_control = {}
    # infection control
    for key, val in infection_disease_num.items():
        control = GameControl()
        control.add_id(key)
        control.add_paramater('dis_num', copy.deepcopy(val[0]))
        control.add_paramater('rep', copy.deepcopy(val[1]))
        control.add_paramater('rep_reset', copy.deepcopy(val[1]))
        control.add_action(copy.deepcopy(infect_action))
        game_control[key] = control

    # player_draw
    control = GameControl()
    control.add_id('player_draw')
    control.add_paramater('rep', player_draw['rep'])
    control.add_paramater('rep_reset', player_card_per_round)
    control.add_action(player_draw['action'])
    game_control['player_draw'] = control

    # single action
    # player_round
    control = GameControl()
    control.add_id('player_round')
    control.add_action(False)
    game_control['player_round'] = control

    # check_player
    control = GameControl()
    control.add_id('check_player')
    control.add_action(False)
    game_control['check_player'] = control

    # hand_limit
    control = GameControl()
    control.add_id('hand_limit')
    control.add_action(False)
    game_control['hand_limit'] = control

    # infection_discard_view
    control = GameControl()
    control.add_id('infection_discard_view')
    control.add_action(False)
    game_control['infection_discard_view'] = control

    return game_control


################################
#  process
################################
def check_if_process(game_control, process):
    if isinstance(game_control[process].action, dict):
        for val in game_control[process].action.values():
            for v in val:
                if v:
                    return True
        return False
    else:
        return game_control[process].action


def assign_next_step(game_control, step_name, OK_bottom):
    # check if any phase is ongoing, if yes, need to return to mark as suspended
    suspended_task = ''
    for val in game_control.values():
        if not isinstance(val.action, bool):
            for v in val.action.values():
                if v[0]:
                    suspended_task = val.id
                    v[0] = False
        else:
            if val.action:
                val.action = False
                suspended_task = val.id

    if not isinstance(game_control[step_name].action, bool):
        key = list(game_control[step_name].action)[0]
        game_control[step_name].action[key][0] = True
    else:
        game_control[step_name].action = True

    if step_name == 'player_round':
        OK_bottom.turn_off()
    else:
        OK_bottom.turn_on()

    return suspended_task


def player_get_card(OK_bottom,
                    player, player_card, player_card_active, cur_player_card, tips,
                    game_control, cur_step, next_step, ):
    # check if the game_control handle is correct
    control = game_control[cur_step]

    # if ok, then next step
    if OK_bottom.rtn_click():
        if control.action['is_player_get_card_phase'][0]:
            control.action['is_player_get_card_phase'][0] = False
            control.action['is_player_get_card_phase'][1] = True
            return

        if control.action['is_player_draw_card'][0]:
            control.action['is_player_draw_card'][0] = False
            control.action['is_player_draw_card'][1] = True
            return

        if control.action['is_player_get_card'][0]:
            control.action['is_player_get_card'][0] = False
            control.action['is_player_get_card'][1] = True
            return

            # display tip

    if control.action['is_player_get_card_phase'][0]:
        control_tip_update(tips, 'Press OK to draw player card')
        OK_bottom.unclick()

    # draw player card
    if control.action['is_player_get_card_phase'][1]:
        control_tip_update(tips, 'Press OK to add this card to hand or continue next step')
        card = player_card.pop()
        if card.name != 'expose':
            player_card_active.append(card)

        control.action['is_player_get_card_phase'][1] = False
        control.action['is_player_draw_card'][0] = True
        OK_bottom.unclick()
        return card

    # add to player's hand
    if control.action['is_player_draw_card'][1]:
        control_tip_update(tips, 'Press OK to continue')
        if cur_player_card:
            if cur_player_card.name != 'expose':
                player.add_hand(cur_player_card)

        control.action['is_player_draw_card'][1] = False
        control.action['is_player_get_card'][0] = True
        OK_bottom.unclick()

    if control.action['is_player_get_card'][1]:
        control.action['is_player_get_card'][1] = False

        # check if need to repeat
        control.paramater['rep'] -= 1
        if control.paramater['rep'] != 0:
            # repeat the process
            control.action['is_player_get_card_phase'][0] = True
        else:
            # re-set the repeat, and move on the the next one
            control.paramater['rep'] = control.paramater['rep_reset']
            OK_bottom.turn_off()
            assign_next_step(game_control, next_step, OK_bottom)
        OK_bottom.unclick()
        control_tip_update(tips, ' ')


def helper_infect_city(OK_bottom,
                       cities, disease, infection_card, infection_discard, cur_infection_card,
                       disease_cube_summary, tips,
                       game_control, cur_step, next_step, tip_text):
    # check if the game_control handle is correct
    control = game_control[cur_step]

    # if ok, then next step
    if OK_bottom.rtn_click():
        if control.action['is_infection_phase'][0]:
            control.action['is_infection_phase'][0] = False
            control.action['is_infection_phase'][1] = True
            OK_bottom.unclick()
            return
        if control.action['is_infect_city'][0]:
            control.action['is_infect_city'][0] = False
            control.action['is_infect_city'][1] = True
            OK_bottom.unclick()
            return

    # update tip
    if control.action['is_infection_phase'][0]:
        control_tip_update(tips, tip_text)
        OK_bottom.unclick()
    # draw infection card
    if control.action['is_infection_phase'][1]:
        control_tip_update(tips, 'Press OK to infect the city')

        # in expose case, draw the first one
        if cur_step == 'expose_infection':
            card = infection_card.pop(0)
        else:
            card = infection_card.pop()

        control.action['is_infection_phase'][1] = False
        control.action['is_infect_city'][0] = True
        OK_bottom.unclick()
        return card

    # infection city
    if control.action['is_infect_city'][1] and cur_infection_card:
        OK_bottom.unclick()
        control_tip_update(tips, 'Press OK to continue')

        # update cur_infection_card's pos
        cur_infection_card.set_discard_pos()

        infection_discard.append(cur_infection_card)
        city_name = infection_discard[-1].name
        for i in range(control.paramater['dis_num']):
            cities[city_name].update_active(True)

            cur_dis_type = cities[city_name].ctcolor
            que = [cities[city_name]]
            memo = []

            while que:
                city = que.pop()
                if not city.is_explose(cur_dis_type):
                    city.infect(cur_dis_type, disease[cur_dis_type].pop())
                    # update dis_cube_num
                    disease_cube_summary[cur_dis_type].add_num(-1)
                else:
                    city.is_shake = True
                    memo.append(city)
                    for link_city in city.city_link:
                        if link_city not in memo or link_city not in que:
                            que.append(link_city)
            if memo:
                break

        control.action['is_infect_city'][1] = False

        # check if need to repeat
        control.paramater['rep'] -= 1
        if control.paramater['rep'] != 0:
            # repeat the process
            control.action['is_infection_phase'][0] = True
            OK_bottom.unclick()
            control_tip_update(tips, ' ')
        else:
            # re-set the repeat, and move on the the next one
            control.paramater['rep'] = control.paramater['rep_reset']
            OK_bottom.turn_off()
            assign_next_step(game_control, next_step, OK_bottom)
            OK_bottom.unclick()
            control_tip_update(tips, ' ')

            # if this is the expose_infection, shuffle the infection discard and add back
            if cur_step == 'expose_infection':
                random.shuffle(infection_discard)
                while infection_discard:
                    card = infection_discard.pop()
                    card.set_cur_pos()
                    infection_card.append(card)
                if memo:
                    return len(memo)
                else:
                    return 'done'

        if memo:
            return len(memo)
        else:
            return


def infect_city(OK_bottom,
                cities, disease, infection_card, infection_discard, cur_infection_card,
                disease_cube_summary, tips,
                game_control):
    # cur_next_ls is in paramater for better control

    for cur_step, next_step, tip_text in cur_next_ls:
        cur_infection_card_temp = helper_infect_city(OK_bottom,
                                                     cities, disease, infection_card, infection_discard,
                                                     cur_infection_card,
                                                     disease_cube_summary, tips,
                                                     game_control, cur_step, next_step, tip_text)
        if cur_infection_card_temp:
            return cur_infection_card_temp


# player action
def discard_card(player, card, player_card_active, player_card_discard):
    player.hand.remove(card)
    player_card_active.remove(card)
    player_card_discard.append(card)
    card.update_pos(x=player_card_img_pos[0] + player_card_size[0] + 15,
                    y=player_card_img_pos[1])


# player's action
def move(cur_player, player_to_move, city_move_to, card_to_use,
         player_card_active, player_card_discard):
    player_to_move.pos_update(city_move_to)
    if card_to_use:
        discard_card(cur_player, card_to_use, player_card_active, player_card_discard)
    cur_player.action_used += 1


def build(cur_player, card_to_use, rp_lab, labs, player_card_active, player_card_discard):
    if not cur_player.city.lab:
        if labs:
            cur_player.city.build_lab(labs.pop())
        else:
            cur_player.city.build_lab(rp_lab.lab)
            rp_lab.lab = ''

        if not cur_player.building_action:
            discard_card(cur_player, card_to_use, player_card_active, player_card_discard)
    cur_player.action_used += 1


def discover_cure(cur_player, cards, is_cure, find_cure, player_card_active, player_card_discard):
    for k, v in color_rbky.items():
        if v == cards[0].color:
            dis_type = k
    is_cure[dis_type] = True
    find_cure[dis_type].add_text(text='Found', size=12, color=WHITE)

    for card in cards:
        discard_card(cur_player, card, player_card_active, player_card_discard)
    cur_player.action_used += 1


def treat(cur_player, disease_color, disease, is_cure, disease_cube_summary):
    dis = cur_player.city.treat(disease_color)
    if dis:
        disease[disease_color].append(dis)
        disease_cube_summary[disease_color].add_num(1)

    if is_cure[disease_color] or cur_player.supertreat:
        for i in range(3):
            dis = cur_player.city.treat(disease_color)
            if dis:
                disease[disease_color].append(dis)
    cur_player.action_used += 1


def share(cur_player, target_player, card):
    cur_player.hand.remove(card)
    target_player.hand.append(card)
    cur_player.action_used += 1


### display board control
# choose one board to display, keep track if on hold of player board
def game_board_chosen(item, display_board):
    for board in display_board:
        if board == item:
            display_board[board].is_close = False
        else:
            display_board[board].is_close = True






################################
#  update
################################
# update tip

def city_tip_update(tips, screen, target=''):
    if target:
        title = target.txt
        title_color = color_rbky[target.ctcolor]
        body = []
        for k, v in target.disease.items():
            body.append(k + ' cube: ' + str(len(v)))
        tips['city'].update_text(title=title, title_color=title_color,
                                 body=body, body_size=15,
                                 line_space=15, indent=30, fit_size=35, n_col=2)
        tips['city'].display(screen)

    else:
        tips['city'].del_text()


def player_tip_update(tips, screen, player_target='', player_card_target=''):
    tips['player'].del_text()

    if player_card_target:
        title = player_card_target.name
        title_color = player_card_target.area.color
        body = []
        for a in player_card_target.discribe:
            body.append(a)
        tips['player'].update_text(title=title, title_size=24, title_color=title_color,
                                   body=body, body_size=16,
                                   line_space=15, indent=20, fit_size=45, n_col=1)
        tips['player'].display(screen)
        return

    if player_target:
        title = player_target.name
        body = []
        for a in player_target.discribe:
            body.append(a)
        tips['player'].update_text(title=title, title_size=24,
                                   body=body, body_size=16,
                                   line_space=15, indent=20, fit_size=45, n_col=1)
        tips['player'].display(screen)
        return


def control_tip_update(tips, body):
    tips['control'].update_text(body=body, body_size=16,
                                line_space=0, indent=10, fit_size=100, n_col=1)


# update indicater


# hightlight city
def hightlight_city(cities, hightlight_ls):
    for city in cities:
        if cities[city].txt in hightlight_ls:
            cities[city].update_active(True)


#########
# manage set of display / handel event
#########

###############################################################
# debug fn
def pnt_game_control(game_control, suspended_task):
    for v in game_control.values():
        print(v.id)
        print(v.paramater)
        print(v.action)
        print('--------')
    print(suspended_task)
