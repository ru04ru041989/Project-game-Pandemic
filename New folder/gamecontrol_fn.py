import sys
import csv
import random
import time

from basic_feature import*
from feature import*
from paramater import*

################################
#  initial
################################

def initial_map(map_size):
    WorldMap = ImgBox(x=0,y=0,w=map_size[0],h=map_size[1])
    WorldMap.add_img(filename = '\\img\\world.jpg', size = map_size, as_rect=False)
    return WorldMap

def initial_city(city_size):
    cities, sudo_city = {}, {}
    cities_ls = []
    with open('city_map.csv') as city_map:
        content = csv.reader(city_map, delimiter=',')
        for row in content:
            if row[1] in ['r','b','k','y']:
                cities[row[0]] = City(cityname = row[0], citycolor = row[1], x=int(row[2])+10, y=int(row[3])+5, txt_up=int(row[4]))
                cities[row[0]].add_img(filename = '\\img\\city_' + row[1] +'.png', size = city_size)
                cities_ls.append(row[0])
            if row[1] == 'w':
                sudo_city[row[0]] = [int(row[2]), int(row[3])]
    with open('city_link.csv') as city_link:
        content = csv.reader(city_link, delimiter=',')
        for row in content:
            if row[1] in cities or  row[1] in sudo_city:
                if row[1] in cities:
                    cities[row[0]].add_link(cities[row[1]])
                else:
                    cities[row[0]].add_sudo_link(sudo_city[row[1]])
    return cities, cities_ls

def initial_disease(dis_cube_num, disease_size):
    disease = {}
    disease_summary = {}
    find_cure = {}
    for i, dis_color in enumerate(['r', 'b', 'k', 'y']):
        #
        dis_temp = [ImgBox() for j in range(dis_cube_num)]
        for dis in dis_temp:
            dis.add_img(filename = '\\img\\dis_' + dis_color +'.png', size = disease_size, to_center=False)
        disease[dis_color] = dis_temp
        
        #
        cure_temp = WordBox(w=disease_summary_size[0], h=disease_summary_size[1])
        cure_temp.add_text(text= 'No Cure', size=12, color=WHITE)
        cure_temp.update_pos(x=disease_summary_pos[0] + i*disease_summary_size[0] , y=disease_summary_pos[1]+disease_summary_size[1])
        cure_temp.add_fill_color(BLACK)
        find_cure[dis_color] = cure_temp
        
        #
        dis_sum = WordBox(w=disease_summary_size[0], h=disease_summary_size[1])
        dis_sum.add_text(text= dis_color + ': ' + str(dis_cube_num), size=18, color=BLACK)
        dis_sum.update_pos(x=disease_summary_pos[0] + i*disease_summary_size[0] , y=disease_summary_pos[1])
        dis_sum.add_fill_color(color_rbky[dis_color])
        disease_summary[dis_color] = dis_sum        
    
    dis_sum = WordBox(w=disease_summary_size[0], h=disease_summary_size[1])
    dis_sum.add_text(text= 'The rest of the disease, game over if = 0 !!!', size=18, color=WHITE)
    dis_sum.update_pos(x=disease_summary_pos[0], y=disease_summary_pos[1]-disease_summary_size[1])
    dis_sum.add_fill_color(BLACK)
    disease_summary['title'] = dis_sum
    
    return disease, disease_summary, find_cure

def initial_infection_card(cities):
    infection_card = []
    for city in cities:
        card = InfectionCard(cities[city])
        infection_card.append(card)
    random.shuffle(infection_card)

    #
    infection_card_img = ImgBox(x=infection_card_img_pos[0], y=infection_card_img_pos[1],
                                w=infection_card_size[0], h=infection_card_size[1], thick = 5, color=RED)
    infection_card_img.add_img(filename = '\\img\\infectcard.png', size = infection_card_size, to_center=False)
    
    #
    infection_discard_img = SelectBox(x= infection_card_img_pos[0] + infection_card_size[0]+10, y=infection_card_img_pos[1],
                                w=infection_card_size[0]+10, h=infection_card_size[1]+10, 
                             keep_active=False, thick=0)
    infection_discard_img.update_color(SHADOW) 

    return infection_card, infection_card_img, infection_discard_img

def initial_infection_indicater():
    #
    infection_rate_text = WordBox()
    infection_rate_text.add_text(text= 'Infection Rate: ' + str(infect_rate), size=18, color=BLACK)
    infection_rate_text.update_pos(x=infection_card_img_pos[0] + infection_card_size[0]*0.5 , 
                                   y=infection_card_img_pos[1] - city_size[1])

    #
    expose_time_text = WordBox()
    expose_time_text.add_text(text= 'Expose Time: ' + str(expose_time) + ' /8', size=18, color=BLACK)
    expose_time_text.update_pos(x=infection_card_img_pos[0] + infection_card_size[0]*0.5 , 
                                   y=infection_card_img_pos[1] - city_size[1]*2) 
    return  infection_rate_text, expose_time_text

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
        player.playerNO_update(i+1)
        player.pos_update(cities['atlanta'])
    
    return players

def initial_player_card(cities):
    player_card = []
    for city in cities:
        card = PlayerCard(cities[city])
        card.add_discribe(['1. Discard this card to move to this city', 
                           '2. Discard this card to move to any city if you are in this city'])
        player_card.append(card)

    player_card_img = ImgBox(x=player_card_img_pos[0], y=player_card_img_pos[1],
                                w=player_card_size[0], h=player_card_size[1], thick = 5, color=RED)
    player_card_img.add_img(filename = '\\img\\playercard.png', size = player_card_size, to_center=False)

    player_card_discard = SelectBox(x= player_card_img_pos[0] + player_card_size[0]+10, y=player_card_img_pos[1],
                                w=player_card_size[0]+10, h=player_card_size[1]+10, 
                             keep_active=False, thick=0)
    player_card_discard.update_color(SHADOW)        

    return player_card, player_card_img, player_card_discard

def initial_tip():
    tips = {}
    for k,v in tip.items():
        t = Tip()
        t.update_rect(v[0], v[1], v[2], v[3])
        tips[k] = t
    return tips
    

################################
#  process
################################


    
def player_get_card(game_control, OK_bottom, player, player_card, player_card_active):
    # if ok, then next step
    if OK_bottom.rtn_click():
        if game_control['is_player_get_card_phase']:
            game_control['is_player_get_card_phase'] = False
            game_control['is_player_get_card'] = True      
    
    # draw player card
    if game_control['is_player_get_card']:
        card = player_card.pop()
        player_card_active.append(card)
        
    # add to player's hand
    if game_control['is_player_get_card']:
        player.add_hand(card)
        game_control['is_player_get_card'] = False
        # disable OK
        OK_bottom.set_select(False)
#--------------------------------------------------------------debug, let infect city after play draw  
        OK_bottom.unclick()
        game_control['is_infection_phase'] = True


def infect_city(game_control, OK_bottom, cities, disease, infection_card, infection_discard, repeat = 1):
    # if ok, then next step
    if OK_bottom.rtn_click():
        if game_control['is_infection_phase']:
            game_control['is_infection_phase'] = False
            game_control['is_infect_city'] = True    
    
    # draw infection card
    if game_control['is_infect_city']:
        infection_discard.append(infection_card.pop())      
    
    # infection city
    if game_control['is_infect_city'] and infection_discard:
        city_name = infection_discard[-1].name
        for i in range(repeat):
            cities[city_name].infect(cities[city_name].ctcolor, disease[cities[city_name].ctcolor].pop())
        
        game_control['is_infect_city'] = False
        # disable OK bottom
        OK_bottom.set_select(False)
#--------------------------------------------------------------debug, let play draw after infect city
        OK_bottom.unclick()
        game_control['is_player_get_card_phase'] = True        

        
        
        

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

def city_tip_update(tips, screen, target = '' ):

    if target:
        title = target.txt
        body = []
        for k,v in target.disease.items():
            body.append( k + ' cube: ' + str(len(v)) )
        tips['city'].update_text(title = title, body=body, body_size = 15, 
                              line_space = 15, indent = 30, fit_size = 35, n_col=2)
        tips['city'].display(screen)
    
    else:
        tips['city'].del_text()  

def player_tip_update(tips, screen, player_target = '', player_card_target='' ):
    tips['player'].del_text()  
    
    if player_card_target:
        title = player_card_target.name
        body = []
        for a in player_card_target.discribe:
            body.append(a)
        tips['player'].update_text(title = title, title_size = 24, body=body, body_size=16,
                              line_space = 15, indent = 50, fit_size = 35, n_col=1)
        tips['player'].display(screen)
        return
    
    if player_target:
        title = player_target.name
        body = []
        for a in player_target.discribe:
            body.append(a)
        tips['player'].update_text(title = title, title_size = 24, body=body, body_size=16,
                              line_space = 15, indent = 50, fit_size = 35, n_col=1)
        tips['player'].display(screen)
        return    

        


# hightlight city
def hightlight_city(cities, rtn_infection_card, rtn_player_card):
    for city in cities:
        if cities[city].txt == rtn_infection_card or cities[city].txt == rtn_player_card:
            cities[city].update_active(True)
            


