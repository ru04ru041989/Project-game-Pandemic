import os
import string
import random
import time
import pygame as pg

import color as color

pg.init()
FONT_pick = pg.font.Font(None, 32)
FONT_notpick = pg.font.Font(None, 24)
FONT = pg.font.Font(None, 32)



class City():
    def __init__(self, cityname, ctcolor, x, y, w, h, txt_up):
        # link: list of the city linked
        self.rect = pg.Rect(x-5, y-4, w, h)
        self.txt = cityname
        self.color = ctcolor
        self.pos = (x,y)
        self.link = []
        self.txt_up = txt_up
        self.img_size = (w,h)
        
        # click control
        self.active = False
        self.hit = 0
        self.font_notpick = pg.font.SysFont('Arial',12, bold = True)
        self.font_pick = pg.font.SysFont('Arial',16, bold = True)
        self.pick_color = color.SHADOW        
        
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
            
    def handle_event(self, event, keep_select = False):
        if keep_select:
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.hit += 1
                    
                # Change the current color of the input box.
                #self.txt_color = self.txt_select_color if self.hit % 2 else self.unselect_color
                #self.color = self.rect_select_color if self.hit % 2 else self.unselect_color
        else:
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active

                else:
                    self.active = False
                # Change the current color of the input box.
                #self.txt_color = self.txt_select_color if self.hit % 2 else self.unselect_color
                #self.color = self.rect_select_color if self.hit % 2 else self.unselect_color                
        
    def display_city_label(self, screen):
        image = pg.image.load(os.getcwd() + '\\img\\city_' + self.color +'.png')
        image = pg.transform.scale(image,self.img_size)
        screen.blit(image, (self.pos[0]-5, self.pos[1]-4))
        
        font = self.font_pick if self.active else self.font_notpick
        city_len = len(self.txt)
        txt = font.render(string.capwords(self.txt), True, (0, 0, 0))
        
        if self.txt_up:
            screen.blit(txt, (self.pos[0]-(city_len*2/3), self.pos[1]-18))
        else:
            screen.blit(txt, (self.pos[0]-(city_len*2/3), self.pos[1]+21))
            
        # draw rect if activate
        if self.active:
            pg.draw.rect(screen, self.pick_color, self.rect, 2)

    def display_city_dis(self,screen):
        for dis in self.dis:
            if self.dis[dis]:
                image = pg.image.load(os.getcwd() + '\\img\\dis_' + dis +'.png')
                image = pg.transform.scale(image,(8,8))
                
                for pos in self.dis[dis]:
                    screen.blit(image, (self.pos[0] + pos[0]*9 -3, 
                                        self.pos[1] + pos[1]*9 ))

    
class InfectionCard():
    def __init__(self,city_ls, rate):
        self.cards = city_ls.copy()
        random.shuffle(self.cards)
        self.discards = []
        
        self.w = 100
        self.h = 90
        
        self.rate = int(rate)
        
        # select contol
        self.color = color.RED
        
        # area for draw
        self.draw_pos = [630,510]
        self.draw_rect = pg.Rect(630, 510, 100, 90)
        image = pg.image.load(os.getcwd() + '\\img\\infectcard.png')
        self.image = pg.transform.scale(image, (self.w,self.h))
        
        self.draw_active = False
        
        # area for discard
        self.discard_pos = [790,530]
        self.discard_rect = pg.Rect(770, 510, 100, 90)
        self.discard_txt = ''
        
        self.discard_active = False

    def active_draw(self):
        self.draw_active = True
        self.draw_discard = False
    def active_discard(self):
        self.draw_active = False
        self.draw_discard = True    
    def deactive_draw(self):
        self.draw_active = False
    def deactive_disdraw(self):
        self.draw_discard = False

    def handle_event(self, event):
        rtn_draw, rtn_discard = '',''
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the discard pile.
            if self.discard_rect.collidepoint(event.pos) and not self.discard_active :
                # highlight the city
                rtn_discard = self.discard_txt
                
            if self.discard_rect.collidepoint(event.pos) and self.discard_active :
                # shuffle the discard pile and add to the end of the whole pile
                random.shuffle(self.discards)
                self.cards = self.cards + self.discards
                self.discards = []
                rtn_discard = ''

            if self.draw_rect.collidepoint(event.pos) and self.draw_active :
                rtn_draw =  self.draw()

        return rtn_draw, rtn_discard

            
  
    def display(self, screen):
        # need to know when the play's round end > to draw card
        # need to know when to re-shuffle discard pile > when pick up a epdimac card
        # when those two event occurd, start checking MOUSEDOWN event, to respond accordingly
        
        # display infection rate
        rate_text = 'Infection rate: ' + str(self.rate)
        rate_txt_surface = FONT.render(rate_text, True, self.color)
        screen.blit(rate_txt_surface, (self.draw_pos[0] +30, self.draw_pos[1]-30))
        
        # display draw part
        screen.blit(self.image, self.draw_pos)
        if self.draw_active:
            pg.draw.rect(screen, self.color, self.draw_rect, 5)
        
        # display discard part
        city_name = string.capwords(self.discard_txt).split()
        for i, txt in enumerate(city_name):
            txt_surface = FONT_notpick.render(txt, True, color.BLACK)
            screen.blit(txt_surface, (self.discard_pos[0], 
                                      self.discard_pos[1] + i*20))
        if self.discard_active:
            pg.draw.rect(screen, self.color, self.discard_rect, 5)
            
    def draw(self):
        card = self.cards.pop()
        self.discard_txt = card
        self.discards.append(card)
        return card



class PlayerCard():
    def __init__(self):
        pass

class Player():
    def __init__(self):
        # drawing para
        self.img_size = [16,20]
        self.init_angle = 0
        self.pos = [0,0]
        self.playerNO = 0
        
        # select para
        self.pawn_rect = pg.Rect(0, 0, 16, 20)
        self.active = False
        self.hit = 0

        self.pick_color = color.SHADOW
                
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

    def handle_event(self, event, keep_select = True):
        if keep_select:
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.pawn_rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.hit += 1
                else:
                    self.hit = 0
        else:
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.pawn_rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
        
    def playerNO_update(self, playerNO):
        self.playerNO = playerNO
        self.init_angle = 45 - 40*(int(playerNO) -1)

    def city_update(self, city):
        self.city = city
        x,y = city.pos
        if int(self.playerNO) == 1:
            self.pos = [x -self.img_size[0] - self.img_size[0]*0.7,
                        y -self.img_size[1] - self.img_size[1]*0.6]
            
        elif int(self.playerNO) == 2:
            self.pos = [x -self.img_size[0] + self.img_size[0]*0.7 ,
                        y -self.img_size[1] - self.img_size[1]*0.7]
            
        elif int(self.playerNO) == 3:
            self.pos = [x -self.img_size[0] + self.img_size[0]*1.4 ,
                        y -self.img_size[1] - self.img_size[1]*0.6] 
            
        elif int(self.playerNO) == 4:
            self.pos = [x + city.img_size[0] - self.img_size[0]*1.1, 
                        y - self.img_size[1]*0.5]
            
        elif int(self.playerNO) == 5:
            self.pos = [x + city.img_size[0] - self.img_size[0]*1.5, 
                        y + city.img_size[1] - self.img_size[1]*1.1]
                
        elif int(self.playerNO) == 6:
            self.pos = [x + city.img_size[0] - self.img_size[0]*1.7 ,
                        y + city.img_size[1] * 0.5]   
        
        # finaly update self.Rect
        self.pos[0] += self.img_size[0]*0.5
        self.pos[1] += self.img_size[1]*0.5
        self.pawn_rect = pg.Rect(self.pos[0], self.pos[1], 16, 20)

    def display_player_area(self, screen):
        # a region to show player's hand
        pass
    
    def display_player_map(self, screen):
        # draw player on the map
        image = pg.image.load(os.getcwd() + '\\img\\player_' + self.color_lab +'.png')
        image = pg.transform.scale(image, self.img_size)
        
        if self.hit % 2:
            image = pg.transform.rotate(image, self.init_angle + 8*(round(time.time() % 360)))
        else:
            image = pg.transform.rotate(image, self.init_angle)
        
        #pawn_cent = self.pawn_rect.center
        #screen.blit(image, pawn_cent)
        screen.blit(image, self.pos)



      
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



