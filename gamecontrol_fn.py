import sys
import csv
import random
import copy

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
    return cities, cities_ls


def initial_lab():
    lab = Lab()
    labs = [lab for i in range(lab_num)]

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
        cure_temp = WordBox(w=disease_summary_size[0], h=disease_summary_size[1])
        cure_temp.add_text(text='No Cure', size=12, color=WHITE, as_rect=False)
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

    disease_cube_summary_title = WordBox(w=disease_summary_size[0], h=disease_summary_size[1])
    disease_cube_summary_title.add_text(text='The rest of the disease, game over if = 0 !!!', size=18, color=WHITE)
    disease_cube_summary_title.update_pos(x=disease_summary_pos[0], y=disease_summary_pos[1] - disease_summary_size[1])
    disease_cube_summary_title.add_fill_color(BLACK)
    return disease_cube_summary, disease_cube_summary_title


def initial_infection_card(cities):
    infection_card = []
    for city in cities:
        card = InfectionCard(cities[city])
        infection_card.append(card)
    random.shuffle(infection_card)

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


def initial_player(cities):
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
        player.pos_update(cities['atlanta'])

    return players


def initial_player_card(cities):
    player_card = []

    # city card
    for city in cities:
        card = PlayerCard(cities[city])
        card.add_discribe(['1. Discard this card to move to this city',
                           '2. Discard this card to move to any city if you are in this city'])
        player_card.append(card)

    # special card
    for name, discribe in sp_player_card.items():
        card = SpPlayerCard(name)
        card.add_discribe(discribe)
        card.update_color(GREEN)
        player_card.append(card)

    player_card_img = ImgBox(x=player_card_img_pos[0], y=player_card_img_pos[1],
                             w=player_card_size[0], h=player_card_size[1], thick=5, color=RED)
    player_card_img.add_img(filename='\\img\\playercard.png', size=player_card_size, to_center=False)

    player_card_discard = SelectBox(x=player_card_img_pos[0] + player_card_size[0] + 10, y=player_card_img_pos[1] - 5,
                                    w=player_card_size[0] + 10, h=player_card_size[1] + 10,
                                    keep_active=False, thick=0)
    player_card_discard.update_color(SHADOW)

    return player_card, player_card_img, player_card_discard


def initial_tip():
    tips = {}
    for k, v in tip.items():
        t = Tip()
        t.update_rect(v[0], v[1], v[2], v[3])
        tips[k] = t

    tips['control'].update_text(title=' ', body=' ')
    return tips


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

    return game_control


################################
#  process
################################

def assign_next_step(game_control, step_name):
    key = list(game_control[step_name].action)[0]
    game_control[step_name].action[key][0] = True


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

    # draw player card
    if control.action['is_player_get_card_phase'][1]:
        control_tip_update(tips, 'Press OK to add this card to hand or continue next step')
        card = player_card.pop()
        player_card_active.append(card)

        control.action['is_player_get_card_phase'][1] = False
        control.action['is_player_draw_card'][0] = True
        return card

    # add to player's hand
    if control.action['is_player_draw_card'][1]:
        control_tip_update(tips, 'Press OK to continue')
        if cur_player_card:
            player.add_hand(cur_player_card)

        control.action['is_player_draw_card'][1] = False
        control.action['is_player_get_card'][0] = True

    # after adding, disable ok and start the next phase
    if control.action['is_player_get_card'][1]:
        # disable OK
        OK_bottom.set_select(False)
        control.action['is_player_get_card'][1] = False

        # check if need to repeat
        control.paramater['rep'] -= 1
        if control.paramater['rep'] != 0:
            # repeat the process
            control.action['is_player_get_card_phase'][0] = True
        else:
            # re-set the repeat, and move on the the next one
            control.paramater['rep'] = control.paramater['rep_reset']
            assign_next_step(game_control, next_step)
        OK_bottom.unclick()


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
            return
        if control.action['is_infect_city'][0]:
            control.action['is_infect_city'][0] = False
            control.action['is_infect_city'][1] = True
            return

    # update tip
    if control.action['is_infection_phase'][0]:
        control_tip_update(tips, tip_text)

    # draw infection card
    if control.action['is_infection_phase'][1]:
        control_tip_update(tips, 'Press OK to infect the city')

        card = infection_card.pop()

        control.action['is_infection_phase'][1] = False
        control.action['is_infect_city'][0] = True
        return card

    # infection city
    if control.action['is_infect_city'][1] and cur_infection_card:
        control_tip_update(tips, 'Press OK to continue')

        # update cur_infection_card's pos
        cur_infection_card.update_pos(x=infection_card_img_pos[0] + infection_card_size[0] + 15,
                                      y=infection_card_img_pos[1])

        infection_discard.append(cur_infection_card)
        city_name = infection_discard[-1].name
        for i in range(control.paramater['dis_num']):
            cities[city_name].infect(cities[city_name].ctcolor, disease[cities[city_name].ctcolor].pop())
            cities[city_name].update_active(True)

        # update dis_cube_num
        cur_num = disease_cube_summary[cities[city_name].ctcolor].num
        disease_cube_summary[cities[city_name].ctcolor].update_num(cur_num - control.paramater['dis_num'])

        # disable OK bottom
        OK_bottom.set_select(False)
        control.action['is_infect_city'][1] = False

        # check if need to repeat
        control.paramater['rep'] -= 1
        if control.paramater['rep'] != 0:
            # repeat the process
            control.action['is_infection_phase'][0] = True
        else:
            # re-set the repeat, and move on the the next one
            control.paramater['rep'] = control.paramater['rep_reset']
            assign_next_step(game_control, next_step)
        OK_bottom.unclick()


def infect_city(OK_bottom,
                cities, disease, infection_card, infection_discard, cur_infection_card,
                disease_cube_summary, tips,
                game_control):
    cur_next_ls = [['initial_infection1', 'initial_infection2', 'Press OK to set up 1st initial infection'],
                   ['initial_infection2', 'initial_infection3', 'Press OK to set up 2nd initial infection'],
                   ['initial_infection3', 'player_draw', 'Press OK to set up 3rd initial infection'],
                   ['normal_infection', 'player_draw', 'Press OK to draw infection card']]

    for cur_step, next_step, tip_text in cur_next_ls:
        cur_infection_card_temp = helper_infect_city(OK_bottom,
                                                     cities, disease, infection_card, infection_discard,
                                                     cur_infection_card,
                                                     disease_cube_summary, tips,
                                                     game_control, cur_step, next_step, tip_text)
        if cur_infection_card_temp:
            return cur_infection_card_temp


# player move
def treat_city(cities, disease, city_name, disease_color, cure):
    dis = cities[city_name].treat(disease_color)
    if dis:
        disease[disease_color].append(dis)

    if cure[disease_color]:
        for i in range(3):
            dis = cities[city_name].treat(disease_color)
            if dis:
                disease[disease_color].append(dis)


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
                                   line_space=15, indent=30, fit_size=45, n_col=1)
        tips['player'].display(screen)
        return

    if player_target:
        title = player_target.name
        body = []
        for a in player_target.discribe:
            body.append(a)
        tips['player'].update_text(title=title, title_size=24,
                                   body=body, body_size=16,
                                   line_space=15, indent=30, fit_size=45, n_col=1)
        tips['player'].display(screen)
        return


def control_tip_update(tips, body):
    tips['control'].update_text(body=body, body_size=16,
                                line_space=0, indent=10, fit_size=100, n_col=1)


# update indicater


# hightlight city
def hightlight_city(cities, rtn_infection_card, rtn_player_card, cur_infection_city):
    for city in cities:
        if cities[city].txt == rtn_infection_card or cities[city].txt == rtn_player_card or \
                cities[city].txt == cur_infection_city:
            cities[city].update_active(True)
