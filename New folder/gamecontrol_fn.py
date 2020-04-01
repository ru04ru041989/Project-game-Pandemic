import sys
import csv
import random

from basic_feature import*
from feature import*

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
    for i in ['r', 'b', 'k', 'y']:
        dis_temp = [ImgBox() for j in range(dis_cube_num)]
        for dis in dis_temp:
            dis.add_img(filename = '\\img\\dis_' + i +'.png', size = disease_size, to_center=False)
        disease[i] = dis_temp
    return disease

def initial_infection_card(cities_ls, infection_card_img_pos, infection_card_size):
    infection_card = []
    for city in cities_ls:
        card = InfectionCard(x=infection_card_img_pos[0] + infection_card_size[0]*1.2, y=infection_card_img_pos[1],
                            w=infection_card_size[0], h=infection_card_size[1])
        card.add_text(text=city, size=20, color=BLACK, as_rect=False)
        infection_card.append(card)
    random.shuffle(infection_card)

    infection_card_img = ImgBox(x=infection_card_img_pos[0], y=infection_card_img_pos[1],
                                w=infection_card_size[0], h=infection_card_size[1])
    infection_card_img.add_img(filename = '\\img\\infectcard.png', size = infection_card_size, to_center=False)
    return infection_card, infection_card_img

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

################################
#  process
################################

def infect_city(cities, disease, infection_card, repeat = 1):
    city_name = infection_card[0].name
    for i in range(repeat):
        cities[city_name].infect(cities[city_name].ctcolor, disease[cities[city_name].ctcolor].pop())

def treat_city(cities, disease, city_name, disease_color, cure):
    dis = cities[city_name].treat(disease_color)
    if dis:
        disease[disease_color].append(dis)
        
    if cure[disease_color]:
        for i in range(3):
            dis = cities[city_name].treat(disease_color)
            if dis:
                disease[disease_color].append(dis)
    

