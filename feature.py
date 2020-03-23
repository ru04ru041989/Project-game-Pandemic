import os
import string
import random
import pygame as pg

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
    def __init__(self, city, playerNO):
        # drawing para
        self.img_size = (16,20)
        self.angle = 45 + 40*int(playerNO)
        
        x,y = city.pos
        if int(playerNO) == 1:
            self.pos = [x -self.img_size[0] ,y -self.img_size[1]]
        elif int(playerNO) == 2:
            self.pos = [x -self.img_size[0] + self.img_size[0]*1.2 ,y -self.img_size[1]]
        elif int(playerNO) == 3:
            self.pos = [x -self.img_size[0] + self.img_size[0]*2.4 ,y -self.img_size[1]]
        elif int(playerNO) == 4:
            self.pos = [x + city.img_size[0], y ]
        elif int(playerNO) == 5:
            self.pos = [x + city.img_size[0] ,y + city.img_size[1]]    
        elif int(playerNO) == 6:
            self.pos = [x + city.img_size[0] - self.img_size[0]*1.2 ,y + city.img_size[1]]    

        # basic para
        self.city = city
        self.action = 4
        self.hand = []
        # might change base on character
        self.handlimit = 7
        self.vaccine_need = 5
        self.building_need = True
        self.supercure = False
        self.sharelock = True

    def move(self):
        pass
    
    def build(self):
        pass
    
    def research(self):
        pass
    
    def cure(self, cur_city, dis, is_vaccine):
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
        image = pg.image.load(os.getcwd() + '\\img\\player_' + self.color +'.png')
        image = pg.transform.scale(self.img_size)
        image = pg.transform.rotate(image, self.angle)
        screen.blit(image, self.pos)


class Scientist(Player):
    def __init__(self, city):
        super().__init__(city)
        self.color = 'grey'
        self.image = pg.image.load(os.getcwd() + '\\img\\player_' + self.color + '.png')
        
        # character ability
        self.vaccine_need = 4
        
class Researcher(Player):
    def __init__(self, city):
        super().__init__(city)
        self.color = 'yellow'
        self.image = pg.image.load(os.getcwd() + '\\img\\player_' + self.color + '.png')
        
        # character ability
        self.sharelock = False
        
