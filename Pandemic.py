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
InfectionCard = InfectionCard(cities_ls)
     
    
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

# all player start form 'atlanta'
for i, player in enumerate(Players):
    player.playerNO_update(i+1)
    player.city_update(cities['atlanta'])

# initial infection: draw 3 card, 3 time
#   1st city get 3 disease cubes, 2nd get 2 , 3th get 1
for i in [3,2,1]:
    for j in range(3):
        city = InfectionCard.draw()
        cities[city].infect(cities[city].color,i)
        cities[city].draw_city_dis(screen)



# game loop
game_on = True
while game_on:
    
    # game display setting
    # =====================================================
    # fill color
    screen.fill(bg_color)

    # supervise keyboard and mouse item
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_on = False
            break
        
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            grid.update(pos)
        
        # check who get pick
        # city
        for city in cities:
            cities[city].handle_event(event)
        # player
        for player in Players:
            player.handle_event(event)

    # draw world map
    WorldMap.blitme()
    
    # draw city state
    for city in cities:
        cities[city].draw_city_label(screen)
        cities[city].draw_city_dis(screen)   
    
    
    # draw player state
    for player in Players:
        player.draw_player_map(screen)


    #grid.draw()
    
    # visualiaze the window
    pg.display.flip()

for play in Players:
    print(player.key)
    print(player.hit)
    print(player.active)

pg.quit()
