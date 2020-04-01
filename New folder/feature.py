import os
import string
import time
import pygame as pg

from paramater import*

from basic_feature import*

pg.init()



class City(ImgBox):
    def __init__(self, x=0, y=0, w=10, h=10, color = BLACK, keep_select = False, to_drag = False,
                 cityname = '', citycolor = '', txt_up = True):
        super().__init__(x=x, y=y, w=w, h=h, color = color, keep_select = keep_select, to_drag = to_drag)   
        self.link = []
        self.txt = cityname
        self.ctcolor = citycolor
        self.txt_up = txt_up
        self.txt_no_select_size = 12
        self.txt_select_size = 16
        
        self.disease = {'r':[], 'b':[], 'k':[], 'y':[]}
        
    def add_link(self, city):
        self.link.append(Link((self.x, self.y), (city.x, city.y)))
    
    def add_sudo_link(self, pos):
        self.link.append(Link((self.x, self.y), (pos[0], pos[1])))
        
    def infect(self, dis_color, dis):
        self.disease[dis_color].append(dis)
    
    def treat(self, dis_color):
        if self.disease[dis_color]:
            return self.disease[dis_color].pop()
        else:
            return ''
    
    def display_link(self, screen):
        # draw link
        for link in self.link:
            link.display(screen)  
              
    def display_cityname(self, screen):
        # draw city name
        txt_size = self.txt_select_size if self.active else self.txt_no_select_size
        font = pg.font.SysFont('Calibri', txt_size, True, False)
        text = font.render(string.capwords(self.txt), True, self.color)
        text_rect = text.get_rect(midtop = self.rect.midbottom)
        if self.txt_up:
            text_rect = text.get_rect(midbottom = self.rect.midtop)
        
        screen.blit(text, text_rect)

    def display_disease(self, screen):
        diseases = []
        for vs in self.disease.values():
            for v in vs:
                diseases.append(v)
        
        # update starting pos for dis in self.rect, 3 columns in a row
        w = self.rect.w // 3
        h = self.rect.h // 3
        
        x = self.rect.x
        for n_col in range(3):
            y = self.rect.y
            for disease in diseases[ n_col * 3 : (n_col+1) * 3]:
                disease.update_pos(x,y)
                disease.display(screen)
                y += h
            x += w
        

class InfectionCard(WordBox):
    def __init__(self, x=0, y=0, w=10, h=10, color = BLACK, keep_select = False, to_drag = False):
        super().__init__(x=x, y=y, w=w, h=h, color = color, keep_select = keep_select, to_drag = to_drag)  
        self.no_rect_color = BLACK
        self.rect_color = RED
              
    def display(self, screen):
        # draw card
        pg.draw.rect(screen, (0, 175, 0), self.rect, 0)
        if self.active:
            pg.draw.rect(screen, self.rect_color, self.rect, self.thick)
        else:
            pg.draw.rect(screen, self.no_rect_color, self.rect, self.thick)     
            
        # draw text       
        if self.as_rect:
            screen.blit(self.text, self.rect)
        else:
            content = content_fit(content=self.org_text, size = 35)
            for txt in content:
                text = self.font.render(string.capwords(txt), True, self.color)
                text_rect = text.get_rect(center = self.rect.center)
                screen.blit(text, text_rect)
        

class Player():
    def __init__(self):
        self.pawn = ImgBox(w=player_pawn_size[0],h=player_pawn_size[1])
        self.area = SelectBox(w=player_area_size[0], h=player_area_size[1], thick=0, keep_select=False)
        self.area_text = WordBox(w=player_area_size[0], h=player_area_size[1])

        
        self.pawn_size = player_pawn_size
        self.init_angle = 0
        self.playerNO = 0

        self.select = False

        # basic para
        self.key = ''
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
        self.init_angle = 45 - 40*(int(playerNO) -1)
        self.pawn.rotate_img(self.init_angle)
        
        x = map_size[0] + 10
        y = 10 + (int(playerNO)-1) * player_area_size[1]
        self.area.update_pos(x,y)
        self.area_text.update_pos(x,y)

    def pos_update(self, city):
        
        self.city = city
        x,y,w,h = city.rect
        # according to player#, adjust the pos
        # (city's w, play's w, city's h, play's h)
        pos_adjs = [(0,0, 0, 0), (0, 1, 0, -0.3), (0, 2, 0, 0),
                   (1,0.4, 0.5, 0), (1, 0.3, 1, 0.1), (0.5, 0.1, 1, 0.3)]
        pos_adj = pos_adjs[int(self.playerNO)-1]
        update_x = x + city_size[0]*pos_adj[0] + player_pawn_size[0]*pos_adj[1]
        update_y =y + city_size[1]*pos_adj[2] + player_pawn_size[1]*pos_adj[3]        
        
        self.pawn.update_pos(update_x, update_y)        
        
        
        #self.city = city
        #self.pawn.update_pos(city.rect.x, city.rect.y)

    def display(self,screen):

        active = True if self.pawn.rtn_active() != self.area.rtn_active() else False
        
        if active:
            self.pawn.rotate_img(self.init_angle + 8*(round(time.time() % 360)))
            self.area.display_select(screen)
        else:
            self.pawn.rotate_img(self.init_angle)
            self.area.display_no_select(screen)

        self.pawn.display_no_rect(screen)
        self.area_text.display(screen)


class Scientist(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'grey'
        self.pawn.add_img(filename = '\\img\\player_' + self.color_lab +'.png', size = self.pawn_size)
        self.color = color_Scientist
        self.key = 'Scientist'
        self.discribe = ['> Need only four cards for cure']
        
        self.area_text.add_text(text=self.key, color=BLACK, rotate=30, size=15, to_center=False)
        self.area.update_color(color_Scientist)
              
        # character ability
        self.cure_need = 4
        
class Researcher(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'yellow'
        self.pawn.add_img(filename = '\\img\\player_' + self.color_lab +'.png', size = self.pawn_size)
        self.color = color_Researcher
        self.key = 'Researcher'
        self.discribe = ['> Give a player card from your hand for one action', 
                            '> Both of you need to be at the same city'] 
        
        self.area_text.add_text(text=self.key, color=BLACK, rotate=30, size=15, to_center=False)
        self.area.update_color(color_Researcher)
        
        # character ability
        self.sharelock = False
        
class Medic(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'orange'
        self.pawn.add_img(filename = '\\img\\player_' + self.color_lab +'.png', size = self.pawn_size)
        self.color = color_Medic
        self.key = 'Medic'
        self.discribe = [' > Remove all the same disease in the city when you treat',
                       ' > If the cure is found, no need to cost action for treat']        
        
        self.area_text.add_text(text=self.key, color=BLACK, rotate=30, size=15, to_center=False)
        self.area.update_color(color_Medic)
        
        # character ability
        self.supertreat = False

class Dispatcher(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'purple'
        self.pawn.add_img(filename = '\\img\\player_' + self.color_lab +'.png', size = self.pawn_size)
        self.color = color_Dispatcher
        self.key = 'Dispatcher'
        self.discribe = [" > Move other player in your turn ",
                        " > Move any player to another player's city for one action"]         
        
        self.area_text.add_text(text=self.key, color=BLACK, rotate=30, size=15, to_center=False)
        self.area.update_color(color_Dispatcher)
        
        # character ability
        self.move_other = True
        
class OperationsExpert(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'lightgreen'
        self.pawn.add_img(filename = '\\img\\player_' + self.color_lab +'.png', size = self.pawn_size)
        self.color = color_OperationsExpert
        self.key = 'Operations Expert'
        self.discribe = [' > Build a research station in your city with one action']         
        
        self.area_text.add_text(text=self.key, color=BLACK, rotate=30, size=15, to_center=False)
        self.area.update_color(color_OperationsExpert)
        
        # character ability
        self.building_action = True

