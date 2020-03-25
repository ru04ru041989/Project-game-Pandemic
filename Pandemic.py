import sys
import os
import pygame as pg

from settings import Settings
import function as fn

from img import WorldMap, grid
from feature import City, Player, InfectionCard
from feature import Scientist, Researcher, Medic, Dispatcher, OperationsExpert
import color as color


pg.init()
settings = Settings()
    
screen = pg.display.set_mode((settings.screen_width,
                                      settings.screen_height))
pg.display.set_caption("Pandemic")

WorldMap = WorldMap(screen, os.getcwd() + '\\img\\world.png')
grid = grid(screen)


# set backgroud color
bg_color = settings.bg_color

# city list
city_size = (28,28)
cities, cities_ls = fn.cities_setup('city_map.csv','city_link.csv', city_size)

# initial game setting
infect_rate = 2
expose_time = 0
vaccine = {'r':False, 'b':False, 'k':False, 'y':False}
building = 6
dis_cube_r = 24
dis_cube_b = 24
dis_cube_k = 24
dis_cube_y = 24

# shuffle infection card,
InfectionCard = InfectionCard(cities_ls, infect_rate)
     
    
    # shuffle city card and special card
    #   distribute card to players, 4p, 2 cards; 3p, 3 cards; 2p, 4 cards
    #   depend on the level, seperate the rest of the card to different part,
    #       add epidemic card to each part
    #       shuffle each part and add together into a pile



max_player = 5

sci = Scientist()
res = Researcher()
med = Medic()
ope = OperationsExpert()
dip = Dispatcher()

chara_pool = [sci, res, med, ope, dip]


setting_para = (80,150,670)
input_box = fn.InputBox(settings.screen_width // 2 + 220, setting_para[0] - 10, 50, 32)

chara_para = [[50,200], [1200,400]]
chara_box = fn.chara_setup(screen, chara_pool, chara_para[0], chara_para[1])

''' debug mode, get to the main setting'''
Players = [ chara for chara in chara_pool]
'''

play_setup_done = False
pos_input = []
# initial setting loop
while not play_setup_done:
    screen.fill(bg_color)
    
    play_setup_done, chara_pick = \
        fn.player_setup(screen, input_box, chara_box, pos_input, setting_para, max_player)
    
    pg.display.update() 


# game initial setting (only run once)
# ======================================================
# setup player
Players = [ chara_pool[chara] for chara in chara_pick]

'''



# all player start form 'atlanta'
for i, player in enumerate(Players):
    player.playerNO_update(i+1)
    player.city_update(cities['atlanta'])


    





InfectionCard.active_draw()
  
for i in [3,2,1]:
    for j in range(3):
        rtn_draw = ''       
        while not rtn_draw:
            rtn_draw, rtn_discard = \
                fn.present(screen, cities, Players, InfectionCard, WorldMap, grid, 
                           special_rate = i, rtn_draw = rtn_draw)

InfectionCard.deactive_draw()




# game loop
game_on = True
while game_on:
    
    fn.present(screen, cities, Players, InfectionCard, WorldMap, grid)
  

pg.quit()
