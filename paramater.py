# basic setting
screen_width = 1360
screen_height = 800
bg_color = (230, 230, 230)

FPS = 30

# display object setting
# ------------------------------------
map_size = (1080, 640)
# -----------------------------------
city_size = (28, 28)
# -----------------------------------
lab_size = (60, 60)
lab_indicater_pos = (25, 460)
# -----------------------------------
disease_size = (8, 8)
disease_summary_pos = (700, 50)
disease_summary_size = (50, 20)
# ----------------------------------
infection_card_size = (120, 100)
infection_card_img_pos = (650, 500)
# ----------------------------------
player_pawn_size = (16, 20)
player_area_size = (250, 120)
# ----------------------------------
player_card_size = (60, 100)
player_card_img_pos = (30, 500)
# ----------------------------------
tip = {'city': (10, 10, 300, 65),
       'player': (990, 620, 360, 170),
       'control': (5, 630, 500, 50)}
# ----------------------------------
OK_bottom_size = (50, 50)
OK_bottom_pos = (510, 630)
USE_bottom_size = (80,50)
USE_bottom_pos = (900,630)

# color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
BLUE = (100, 100, 255)
PURPLE = (202, 50, 202)
SHADOW = (192, 192, 192)
ORANGE = (255, 165, 0)
GRAY = (230, 230, 230)
YELLOW = (200, 200, 0)

color_rbky = {'r': RED, 'b': BLUE, 'k': PURPLE, 'y': YELLOW}
# specific for character

color_OperationsExpert = (182, 255, 174)
color_Dispatcher = (182, 0, 180)
color_Medic = (255, 165, 0)
color_Researcher = (243, 243, 0)
color_Scientist = (128, 128, 128)

###########################
# game setting
infect_rate = 2
expose_time = 0
player_card_per_round = 2
cure = {'r': False, 'b': False, 'k': False, 'y': False}
lab_num = 6
dis_cube_num = {'r': 24, 'b': 24, 'k': 24, 'y': 24}

# key = player num, val = initial hand
initial_player_card = {'2': 4, '3': 3, '4': 2}

# key = level, val = expose card initial interval
difficult_level = {'1': 4, '2': 5, '3': 6}

# special player card
sp_player_card = {
    'lift': ['move a player to any city'],
    'peaceful night': ['skip the infection city phase'],
    'predict the future': ['see the top 6 infection cards',
                           'reorder the those 6 cards'],
    'funding': ['build a lab at any city without the city card'],
    'immune population': ['remove a infection card for the infection discard pile']
}

###########################
# game control

infection_disease_num = {
    # val[0] = num of disease, val[1] = rep time
    'initial_infection1': [3, 3],
    'initial_infection2': [2, 3],
    'initial_infection3': [1, 3],
    'normal_infection': [1, infect_rate],
    'expose_infection': [3, 1]
}

infect_action = {
    'is_infection_phase': [False, False],
    'is_infect_city': [False, False]
}

# ------------------------------------------------------------debug, start from player_draw
player_draw = {
    'rep': player_card_per_round,
    'action': {
        'is_player_get_card_phase': [False, False],
        'is_player_draw_card': [False, False],
        'is_player_get_card': [False, False]
    }
}

'''
some though of control the overall step
use list(game_control.keys()) to get all the main step
having another function / or in the each main step function
    at the end of the process, 
        > indicate the index of the next main step in the list
        > ......or the key name, an use list.index(key_name) to lociate the process

to do this, need a global main step indicater

'''
