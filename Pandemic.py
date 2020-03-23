import sys
import os
import pygame as pg

from settings import Settings
from feature import City, Player, InfectionCard
from img import WorldMap, grid

import function as fn


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
cities, cities_ls = fn.cities_setup('city_map.csv','city_link.csv')

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

initial_game_setting_done = False

play_setup_reset, play_setup_done = False, False
player_number = 0
pos_input = []

while not play_setup_done:
    screen.fill(bg_color)
    
    player_number = fn.player_setup(screen, pos_input, player_number)
    
    play_setup_reset, play_setup_done = fn.player_confirm(screen, pos_input)
    
    if play_setup_reset:
        player_number = 0
        pos_input = []
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos_input = pg.mouse.get_pos()
        
    pg.display.flip()

    
# game loop
while True:
    # game display setting
    # =====================================================
    # fill color
    screen.fill(bg_color)

    # draw world map
    WorldMap.blitme()
    
    # draw city state
    for city in cities:
        cities[city].draw_city_label(screen, city)
        cities[city].draw_city_dis(screen)   
    
    
    # draw player state
    
    # game initial setting (only run once)
    # ======================================================
    # initial infection: draw 3 card, 3 time
    #   1st city get 3 disease cubes, 2nd get 2 , 3th get 1
    if not initial_game_setting_done:
        for i in [3,2,1]:
            for j in range(3):
                city = InfectionCard.draw()
                cities[city].infect(cities[city].color,i)
                cities[city].draw_city_dis(screen)

        initial_game_setting_done = True
    
    # supervise keyboard and mouse item
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            
            grid.update(pos)

    grid.draw()
    
    # visualiaze the window
    pg.display.flip()


