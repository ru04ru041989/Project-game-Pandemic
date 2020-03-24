import os
import string
import random
import pygame as pg

import color as color

class City():
    def __init__(self, color, x, y, txt_up):
        # link: list of the city linked
        self.color = color
        self.pos = (x,y)
        self.link = []
        self.txt_up = txt_up
        self.img_size = (25,25)
        
        # how many disease cube in the city (Max = 3)
        self.dis = {'r':[], 'b':[], 'k':[], 'y':[]}
        self.dis_pos = [[0,0], [1,0], [2,0],
                        [0,1], [1,1], [2,1],
                        [0,2], [1,2], [2,2]]
        self.is_explose = False
    
    def add_link(self, city):
        self.link.append(city)
    
    def infect(self, dis, number):
        # adding the dis color and number to disease cube
        # check if num >3, if yes, then return true to explose
        if len(self.dis[dis]) + number >3:
            return True
        else:
            for i in range(number):
                self.dis[dis].append(self.dis_pos.pop(0))
            return False
    
    def cure_dis(self, dis, is_vaccine):
        if is_vaccine:
            if self.dis[dis]:
                self.dis_pos.append(self.dis[dis].pop())
        else:
            self.dis_pos.append(self.dis[dis].pop())
            
        
    def draw_city_label(self, screen, cityname):
        image = pg.image.load(os.getcwd() + '\\img\\city_' + self.color +'.png')
        image = pg.transform.scale(image,self.img_size)
        screen.blit(image, (self.pos[0]-5, self.pos[1]-4))
        
        font = pg.font.SysFont('Arial',12, bold = True)
        city_len = len(cityname)
        txt = font.render(string.capwords(cityname), True,
                        (0, 0, 0))
        if self.txt_up:
            screen.blit(txt, (self.pos[0]-(city_len*2/3), self.pos[1]-18))
        else:
            screen.blit(txt, (self.pos[0]-(city_len*2/3), self.pos[1]+18))

    def draw_city_dis(self,screen):
        for dis in self.dis:
            if self.dis[dis]:
                image = pg.image.load(os.getcwd() + '\\img\\dis_' + dis +'.png')
                image = pg.transform.scale(image,(8,8))
                
                for pos in self.dis[dis]:
                    screen.blit(image, (self.pos[0] + pos[0]*9 -3, 
                                        self.pos[1] + pos[1]*9 ))
                
        
    
class InfectionCard():
    def __init__(self,city_ls):
        self.cards = city_ls.copy()
        random.shuffle(self.cards)
        self.discards = []
    def draw(self):
        card = self.cards.pop()
        self.discards.append(card)
        return card
        
class PlayerCard():
    def __init__(self):
        pass

class Player():
    def __init__(self):
        # drawing para
        self.img_size = [16,20]
        self.angle = 0
        self.pos = [0,0]
        self.playerNO = 0
        
        # basic para
        self.city = ''
        self.hand = []
        
        # might change base on character
        self.action = 4
        self.handlimit = 7
        self.cure_need = 5
        self.building_action = True
        self.supertreat = False
        self.sharelock = True
        self.move_other = False

    def playerNO_update(self, playerNO):
        self.playerNO = playerNO
        self.angle = 45 - 40*(int(playerNO) -1)

    def city_update(self, city):
        self.city = city
        x,y = city.pos
        if int(self.playerNO) == 1:
            self.pos = [x -self.img_size[0] - self.img_size[0]*0.2,
                        y -self.img_size[1] - self.img_size[1]*0.1]
            
        elif int(self.playerNO) == 2:
            self.pos = [x -self.img_size[0] + self.img_size[0]*1.2 ,
                        y -self.img_size[1] - self.img_size[1]*0.2]
            
        elif int(self.playerNO) == 3:
            self.pos = [x -self.img_size[0] + self.img_size[0]*1.9 ,
                        y -self.img_size[1] - self.img_size[1]*0.1] 
            
        elif int(self.playerNO) == 4:
            self.pos = [x + city.img_size[0] - self.img_size[0]*0.6, 
                        y ]
            
        elif int(self.playerNO) == 5:
            self.pos = [x + city.img_size[0] - self.img_size[0], 
                        y + city.img_size[1] - self.img_size[1]*0.6]
                
        elif int(self.playerNO) == 6:
            self.pos = [x + city.img_size[0] - self.img_size[0]*1.2 ,
                        y + city.img_size[1]]    
        
    def move(self):
        pass
    
    def build(self):
        pass
    
    def research(self):
        pass
    
    def treat(self, cur_city, dis, is_vaccine):
        pass
    
    def share(self):
        pass

    def draw_hand(self, card):
        self.hand.append(card)
        if len(self.hand) > self.handlimit:
            self.discard()
    
    def discard(self):
        # display msg that hand over the limit, ask which card to discard
        # display clear and confirm option
        self.hand.remove(card)
        pass

    def draw_player_area(self, screen):
        # a region to show player's hand
        pass
    
    def draw_player_map(self, screen):
        # draw player on the map
        image = pg.image.load(os.getcwd() + '\\img\\player_' + self.color_lab +'.png')
        image = pg.transform.scale(image, self.img_size)
        image = pg.transform.rotate(image, self.angle)
        screen.blit(image, self.pos)


class Scientist(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'grey'
        self.image = pg.image.load(os.getcwd() + '\\img\\player_' + self.color_lab + '.png')
        self.color = color.Scientist
        self.key = 'Scientist'
        self.discribe = ['Need only four card for cure']        
        # character ability
        self.cure_need = 4
        
class Researcher(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'yellow'
        self.image = pg.image.load(os.getcwd() + '\\img\\player_' + self.color_lab + '.png')
        self.color = color.Researcher
        self.key = 'Researcher'
        self.discribe = ['Give a player card from your hand for one action', 
                            'Both of you need to be at the same city'] 
        # character ability
        self.sharelock = False
        
class Medic(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'orange'
        self.image = pg.image.load(os.getcwd() + '\\img\\player_' + self.color_lab + '.png')
        self.color = color.Medic
        self.key = 'Medic'
        self.discribe = ['Remove all the same disease in the city when you treat',
                       'If the cure is found, no need to cause for treat']        
        # character ability
        self.supertreat = False

class Dispatcher(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'purple'
        self.image = pg.image.load(os.getcwd() + '\\img\\player_' + self.color_lab + '.png')
        self.color = color.Dispatcher
        self.key = 'Dispatcher'
        self.discribe = ["Move other player in your turn ",
                        "Move any player to another player's city for one action"]         
        # character ability
        self.move_other = True
        
class OperationsExpert(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'lightgreen'
        self.image = pg.image.load(os.getcwd() + '\\img\\player_' + self.color_lab + '.png')
        self.color = color.OperationsExpert
        self.key = 'Operations Expert'
        self.discribe = ['Build a research station in your city with one action']         
        # character ability
        self.building_action = True



