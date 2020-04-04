import os
import string
import time
import pygame as pg

from paramater import*

from basic_feature import*

pg.init()



class City(ImgBox):
    def __init__(self, x=0, y=0, w=10, h=10, color = BLACK, keep_active = False, to_drag = False,
                 cityname = '', citycolor = '', txt_up = True):
        super().__init__(x=x, y=y, w=w, h=h, color = color, keep_active = keep_active, to_drag = to_drag)   
        self.link = []
        self.txt = cityname
        self.ctcolor = citycolor
        self.txt_up = txt_up
        self.txt_no_select_size = 12
        self.txt_select_size = 16
        
        self.lab = ''
        
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

    def build_lab(self, lab):
        lab.update_pos(self.x-lab_size[0]*0.5, self.y-lab_size[1]*0.5)
        self.lab = lab

    def rm_lab(self):
        lab = self.lab
        self.lab = ''
        return lab

    def display_before(self, screen):
        if self.lab:
            self.lab.display(screen)  
                  
        # draw link
        for link in self.link:
            link.display(screen)  


    def display_after(self, screen):
        # draw city name
        txt_size = self.txt_select_size if self.active else self.txt_no_select_size
        font = pg.font.SysFont('Calibri', txt_size, True, False)
        text = font.render(string.capwords(self.txt), True, self.color)
        text_rect = text.get_rect(midtop = self.rect.midbottom)
        if self.txt_up:
            text_rect = text.get_rect(midbottom = self.rect.midtop)
        
        screen.blit(text, text_rect)

        #
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


class Lab():
    def __init__(self):
        area = ImgBox(x=0,y=0,w=lab_size[0],h=lab_size[1])
        area.add_img(filename = '\\img\\lab.png', size = lab_size)
        self.area = area
    
    def update_pos(self, x,y):
        self.area.update_pos(x,y) 
    
    def display(self, screen):
        self.area.display(screen)
        
        
class InfectionCard():
    def __init__(self, city):
        area = SelectBox(x= infection_card_img_pos[0] + infection_card_size[0]*0.2, 
                        y=infection_card_img_pos[1]+ infection_card_size[0]*0.2,
                        w=infection_card_size[0], 
                        h=infection_card_size[1], 
                        keep_active=False, thick=0)
        area.update_color((0, 175, 0))
        self.area = area
        
        x,y = area.rect.topleft
        area_text = WordBox(x= x , y=y,
                       w=infection_card_size[0], h=infection_card_size[1])
        
        area_text.add_text(text=city.txt, size = 16, color = BLACK, as_rect=False)


        self.name = city.txt
        
        self.area_text = area_text

    def update_pos(self,x,y):
        self.area.update_pos(x,y)
        text_x,text_y = self.area.rect.topleft
        self.area_text.update_pos(text_x,text_y)

    def handle_event(self,event):
        self.area.handle_event(event)

    def rtn_target(self):
        if self.area.active:
            return self.name
        else:
            return 

    def display(self,screen):
        self.area.display(screen, is_rect=True, active_off=True)
        self.area_text.display(screen)
        

class PlayerCard():
    def __init__(self, city):

        area = SelectBox(x= player_card_img_pos[0] + player_card_size[0]*0.2, 
                        y=player_card_img_pos[1] + player_card_size[1]*0.2,
                        w=player_card_size[0], 
                        h=player_card_size[1], 
                        keep_active=False, thick=0)
        area.update_color(color_rbky[city.ctcolor])
        self.area = area
        
        #
        area_text = WordBox(w=player_card_size[0], h=player_card_size[1])
        area_text.add_text(text=string.capwords(city.txt), size = 12, color = BLACK, is_cap=True)
        area_text.rotate_text(-90)
        
        area_text.rect.midright = area.rect.midright

        self.name = city.txt
        self.area_text = area_text
        self.discribe = ''

    def update_pos(self, x, y):
        self.area.update_pos(x,y)
        text_x, text_y = self.area.rect.midright
        self.area_text.rect.midright = (text_x,text_y)

    def add_discribe(self, discribe):
        self.discribe = discribe

    def rtn_active(self):
        return self.area.active

    def handle_event(self,event):
        self.area.handle_event(event)  

    def rtn_target(self):
        if self.area.active:
            return self.name
        else:
            return 

    def display(self,screen):
        self.area.display(screen, is_rect=True, active_off=True)
        self.area_text.display(screen)


class DiseaseSummary():
    def __init__(self):
        area_text = WordBox(w=disease_summary_size[0], h=disease_summary_size[1])
               
        self.area_text = area_text
        self.num = 0

    def update_pos(self,x,y):
        self.area_text.update_pos(x,y)
    
    def add_fill_color(self, color):
        self.area_text.add_fill_color(color)
        
    def update_num(self, num):
        self.num = num
        self.area_text.add_text(text= str(self.num), size=18, color=BLACK, as_rect=False)
        
    def display(self, screen):
        self.area_text.display(screen, is_fill = True)
        

class Tip():
    def __init__(self):
        area = SelectBox(thick=0)
        area.update_color(WHITE)
        self.area = area
        
        area_text = InfoBox()
        self.area_text = area_text
    
    def update_rect(self,x,y,w,h):
        # set rect in area and area_text
        self.area.update_pos(x,y)
        self.area.update_wh(w,h)
        
        x,y = self.area.rect.center
        self.area_text.update_pos(x-w*0.5,y-h*0.5)
        self.area_text.update_wh(w,h)       
    
    def update_text(self, title='', title_size = 14, title_color = BLACK,
                    body='', body_size = 10, body_color = BLACK,
                    line_space = 15, indent = 50, fit_size = 35, n_col=1):
        if title:
            self.area_text.add_title(title=title, size = title_size, color=title_color)
        if body:
            self.area_text.add_body(body=body, size = body_size, color=body_color, 
                                    line_space = line_space, indent = indent, fit_size = fit_size, n_col=n_col)

    def del_text(self):
        self.area_text.add_title(title='')
        self.area_text.add_body(body='')
        
    def display(self, screen):
        self.area.display(screen)
        if self.area_text.is_content:
            self.area_text.display(screen)


class ControlBottom():
    def __init__(self):
        area = SelectBox(thick=0, keep_active=False)
        area.update_color(WHITE)
        area.update_pos(x = control_bottom_pos[0], y = control_bottom_pos[1])
        area.update_wh(w=control_bottom_size[0], h=control_bottom_size[1])
        self.area = area
        
        area_text = WordBox(x = control_bottom_pos[0] + control_bottom_size[0]*0.5, 
                            y = control_bottom_pos[1] + control_bottom_size[1]*0.5,
                            w=control_bottom_size[0], 
                            h=control_bottom_size[1])
        area_text.add_text(text = 'OK', color = BLACK, size = 36, is_cap=False)
        self.area_text = area_text

        # if select by other object
        self.select = False
    
    def update_pos(self,x,y):
        # set rect in area and area_text
        self.area.update_pos(x,y)
    
    def set_select(self, select):
        self.select = select

    def unclick(self):
        self.area.click = False
    
    def rtn_click(self):
        return self.area.rtn_click()
    
    def display(self, screen):
        if self.select:
            self.area.update_color(ORANGE)
        else:
            self.area.update_color(WHITE)
        
        self.area.display_no_active(screen)
        self.area_text.display(screen)
    

        
class Player():
    def __init__(self):
        self.pawn = ImgBox(w=player_pawn_size[0],h=player_pawn_size[1], keep_active=False)
        self.area = SelectBox(w=player_area_size[0], h=player_area_size[1], thick=0, keep_active=False)
        self.area_text = WordBox(w=player_area_size[0], h=player_area_size[1])

        self.pawn_size = player_pawn_size
        self.init_angle = 0
        self.playerNO = 0

        self.select = False
        self.active = False

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

    def rtn_active(self):
        return self.active

    def add_hand(self, card):
        self.hand.append(card)
    
    def discard_hand(self,card):
        # update the card's pos to discard pile
        card.update_pos(infection_card_img_pos[0] + infection_card_size[0]+10, infection_card_img_pos[1])
        # rm from hand
        self.hand.remove(card)

    def display(self,screen):

        # draw pawn, player area
        self.active = True if self.pawn.rtn_active() != self.area.rtn_active() else False
        if self.active:
            self.pawn.rotate_img(self.init_angle + 8*(round(time.time() % 360)))
            self.area.display_active(screen)
        else:
            self.pawn.rotate_img(self.init_angle)
            self.area.display_no_active(screen)
        self.pawn.display(screen, is_rect=False)
        self.area_text.display(screen)

        # draw player card
        # get the rect to calculate pos for each card
        x = self.area.rect.x + self.area.rect.w - player_card_size[0]*0.5
        y = [self.area.rect.y + player_card_size[1]*0.2, 
             self.area.rect.y ]
        for i in range(self.handlimit):
            # calculate
            cur_x = x - (i+1)*player_card_size[0]*0.5
            cur_y = y[1] if i%2 else y[0]
            
            if i < len(self.hand):
                # update the card to that pos
                self.hand[i].update_pos(x=cur_x, y=cur_y)
                self.hand[i].display(screen)
            #else:
            #    # just print the rect 
            #    rect = pg.Rect(cur_x,cur_y,player_card_size[0],player_card_size[1])
            #    pg.draw.rect(screen, WHITE, rect, 2)
                
        

class Scientist(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'grey'
        self.pawn.add_img(filename = '\\img\\player_' + self.color_lab +'.png', size = self.pawn_size)
        self.color = color_Scientist
        self.name = 'Scientist'
        self.discribe = ['> Need only four cards for cure']
        
        self.area_text.add_text(text=self.name, color=BLACK,size=15, to_center=False)
        self.area_text.rotate_text(30)
        self.area.update_color(color_Scientist)
              
        # character ability
        self.cure_need = 4
        
class Researcher(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'yellow'
        self.pawn.add_img(filename = '\\img\\player_' + self.color_lab +'.png', size = self.pawn_size)
        self.color = color_Researcher
        self.name = 'Researcher'
        self.discribe = ['> Give a player card from your hand for one action', 
                            '> Both of you need to be at the same city'] 
        
        self.area_text.add_text(text=self.name, color=BLACK,size=15, to_center=False)
        self.area_text.rotate_text(30)
        self.area.update_color(color_Researcher)
        
        # character ability
        self.sharelock = False
        
class Medic(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'orange'
        self.pawn.add_img(filename = '\\img\\player_' + self.color_lab +'.png', size = self.pawn_size)
        self.color = color_Medic
        self.name = 'Medic'
        self.discribe = [' > Remove all the same disease in the city when you treat',
                       ' > If the cure is found, no need to cost action for treat']        
        
        self.area_text.add_text(text=self.name, color=BLACK,size=15, to_center=False)
        self.area_text.rotate_text(30)
        self.area.update_color(color_Medic)
        
        # character ability
        self.supertreat = False

class Dispatcher(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'purple'
        self.pawn.add_img(filename = '\\img\\player_' + self.color_lab +'.png', size = self.pawn_size)
        self.color = color_Dispatcher
        self.name = 'Dispatcher'
        self.discribe = ["> Move other player in your turn ",
                        "> Move any player to another player's city for one action"]         
        
        self.area_text.add_text(text=self.name, color=BLACK,size=15, to_center=False)
        self.area_text.rotate_text(30)
        self.area.update_color(color_Dispatcher)
        
        # character ability
        self.move_other = True
        
class OperationsExpert(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'lightgreen'
        self.pawn.add_img(filename = '\\img\\player_' + self.color_lab +'.png', size = self.pawn_size)
        self.color = color_OperationsExpert
        self.name = 'Operations Expert'
        self.discribe = [' > Build a research station in your city with one action']         
        
        self.area_text.add_text(text=self.name, color=BLACK,size=15, to_center=False)
        self.area_text.rotate_text(30)
        self.area.update_color(color_OperationsExpert)
        
        # character ability
        self.building_action = True

