import sys
import os
import pygame as pg

from settings import Settings
import function as fn
from function import GameControl

from img import WorldMap, grid
from feature import City, Player, InfectionCard, Tip, PlayerCard
from feature import Scientist, Researcher, Medic, Dispatcher, OperationsExpert
import color as color

FPS = 30

pg.init()
settings = Settings()
 
screen = pg.display.set_mode((settings.screen_width,
                                      settings.screen_height))
pg.display.set_caption("Pandemic")

WorldMap = WorldMap(screen, os.getcwd() + '\\img\\world.jpg')
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

city_tip = Tip(10,10,300,60, color.WHITE, interval = 20, textsize=10)
chara_tip = Tip(1090, 620, 260 , 170, color.WHITE, interval = 35)
Tips = {'player': chara_tip, 'city': city_tip}


setting_para = (80,150,670)
input_box = fn.InputBox(settings.screen_width // 2 + 250, setting_para[0]-10 , 50, 32)

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
    
    play_setup_done, chara_pick= \
        fn.player_setup(screen, input_box, chara_box, pos_input, setting_para, max_player)
    
    pg.display.update() 


# game initial setting (only run once)
# ======================================================
# setup player
Players = [ chara_pool[chara] for chara in chara_pick]

'''
test = PlayerCard(x = 50, y=50, name = 'text', color = 'b')

# all player start form 'atlanta'
for i, player in enumerate(Players):
    player.playerNO_update(i+1)
    player.city_update(cities['atlanta'])


GameControl = GameControl(screen, cities, Players, InfectionCard, WorldMap, Tips, grid)


InfectionCard.active_draw()


clock = pg.time.Clock()
  
for i in [1, 1, 1, 2, 2, 2, 3, 3, 3]:

    rtn_draw, rtn_discard = '',''
    while not rtn_draw:

#### debug testing        
        GameControl.display(test)
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        
            # event control
            rtn_draw, rtn_discard = GameControl.even_control_infection(event)
            GameControl.even_control_player(event)
            GameControl.even_control_city(event)

#### debug testing            
            GameControl.event_control_debut(event, test)
        
        # even respond
        GameControl.event_respond_infection_initial(rtn_draw, rtn_discard,i)

    clock.tick(FPS)
    
InfectionCard.deactive_draw()
if len(InfectionCard.discards) >9:
    for city in InfectionCard.discards:
        print(city)
        print(cities[city].dis)
        




# game loop
game_on = True
while game_on:
    
    #fn.control_infection(screen, cities, Players, InfectionCard, WorldMap, grid)
    GameControl.display()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            grid.update(pos)
        
        # even control
        rtn_draw, rtn_discard = GameControl.even_control_infection(event)
        GameControl.even_control_player(event)
        GameControl.even_control_city(event)
    
    # even respond
    GameControl.event_respond_infection(rtn_draw, rtn_discard)
    
    clock.tick(FPS)

    
pg.quit()
