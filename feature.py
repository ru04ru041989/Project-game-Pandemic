import os
import string
import time
from typing import Dict, Any

import pygame as pg

from paramater import *

from basic_feature import *

pg.init()


class City(ImgBox):
    def __init__(self, x=0, y=0, w=10, h=10, color=BLACK, keep_active=False, to_drag=False,
                 cityname='', citycolor='', txt_up=True):
        super().__init__(x=x, y=y, w=w, h=h, color=color, keep_active=keep_active, to_drag=to_drag)
        self.city_link = []
        self.link = []
        self.txt = cityname
        self.ctcolor = citycolor
        self.txt_up = txt_up
        self.txt_no_select_size = 12
        self.txt_select_size = 16

        self.lab = ''

        self.disease = {'r': [], 'b': [], 'k': [], 'y': []}

    def add_link(self, city):
        self.link.append(Link((self.x, self.y), (city.x, city.y)))
        self.city_link.append(city)

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
        lab.update_pos(self.x - lab_size[0] * 0.5, self.y - lab_size[1] * 0.5)
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
        text_rect = text.get_rect(midtop=self.rect.midbottom)
        if self.txt_up:
            text_rect = text.get_rect(midbottom=self.rect.midtop)

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
            for disease in diseases[n_col * 3: (n_col + 1) * 3]:
                disease.update_pos(x, y)
                disease.display(screen)
                y += h
            x += w


class Lab():
    def __init__(self):
        area = ImgBox(x=0, y=0, w=lab_size[0], h=lab_size[1])
        area.add_img(filename='\\img\\lab.png', size=lab_size)
        self.area = area

    def update_pos(self, x, y):
        self.area.update_pos(x, y)

    def display(self, screen):
        self.area.display(screen)


class InfectionCard():
    def __init__(self, city):
        area = SelectBox(x=infection_card_img_pos[0] + infection_card_size[0] * 0.2,
                         y=infection_card_img_pos[1] + infection_card_size[0] * 0.2,
                         w=infection_card_size[0],
                         h=infection_card_size[1],
                         keep_active=False, thick=0)
        area.update_color((0, 175, 0))
        self.area = area

        x, y = area.rect.topleft
        area_text = WordBox(x=x, y=y,
                            w=infection_card_size[0], h=infection_card_size[1])

        area_text.add_text(text=city.txt, size=16, color=BLACK, as_rect=False)

        self.name = city.txt

        self.area_text = area_text

    def update_pos(self, x, y):
        self.area.update_pos(x, y)
        text_x, text_y = self.area.rect.topleft
        self.area_text.update_pos(text_x, text_y)

    def handle_event(self, event):
        self.area.handle_event(event)

    def rtn_target(self):
        if self.area.active:
            return self.name
        else:
            return

    def display(self, screen):
        self.area.display(screen, is_rect=True, active_off=True)
        self.area_text.display(screen)


# -------------------------------------------------------------------   Player card
class PlayerCard():
    def __init__(self, city):
        area = SelectBox(x=player_card_img_pos[0] + player_card_size[0] * 0.2,
                         y=player_card_img_pos[1] + player_card_size[1] * 0.2,
                         w=player_card_size[0],
                         h=player_card_size[1],
                         keep_active=False, thick=0)
        area.update_color(color_rbky[city.ctcolor])
        self.color = color_rbky[city.ctcolor]
        self.area = area

        #
        area_text = WordBox(w=player_card_size[0], h=player_card_size[1])
        area_text.add_text(text=string.capwords(city.txt), size=12, color=BLACK, is_cap=True)
        area_text.rotate_text(-90)

        area_text.rect.midright = area.rect.midright

        self.name = city.txt
        self.area_text = area_text
        self.discribe = ''
        self.type = 'city'


    def update_pos(self, x, y):
        self.area.update_pos(x, y)
        text_x, text_y = self.area.rect.midright
        self.area_text.rect.midright = (text_x, text_y)

    def add_discribe(self, discribe):
        self.discribe = discribe

    def rtn_active(self):
        return self.area.active

    def handle_event(self, event):
        self.area.handle_event(event)

    def rtn_target(self):
        if self.area.active:
            return self.name
        else:
            return

    def display(self, screen):
        self.area.display(screen, is_rect=True, active_off=True)
        self.area_text.display(screen)


class SpPlayerCard(PlayerCard):
    def __init__(self, name):
        area = SelectBox(x=player_card_img_pos[0] + player_card_size[0] * 0.2,
                         y=player_card_img_pos[1] + player_card_size[1] * 0.2,
                         w=player_card_size[0],
                         h=player_card_size[1],
                         keep_active=False, thick=0)
        self.area = area
        self.color = ''
        #
        area_text = WordBox(w=player_card_size[0], h=player_card_size[1])
        area_text.add_text(text=string.capwords(name), size=12, color=BLACK, is_cap=True)
        area_text.rotate_text(-90)

        area_text.rect.midright = area.rect.midright

        self.area_text = area_text
        self.name = name
        self.discribe = ''
        self.type = 'special'

    def update_color(self, color):
        self.color = color
        self.area.update_color(color)


# ----------------------------------------------------------------------------------
class DiseaseSummary():
    def __init__(self):
        area_text = WordBox(w=disease_summary_size[0], h=disease_summary_size[1])

        self.area_text = area_text
        self.num = 0

    def update_pos(self, x, y):
        self.area_text.update_pos(x, y)

    def add_fill_color(self, color):
        self.area_text.add_fill_color(color)

    def add_num(self, num):
        self.num += num
        self.area_text.add_text(text=str(self.num), size=18, color=BLACK, as_rect=False)

    def update_num(self, num):
        self.num = num
        self.area_text.add_text(text=str(self.num), size=18, color=BLACK, as_rect=False)

    def display(self, screen):
        self.area_text.display(screen, is_fill=True)


class Tip():
    def __init__(self):
        area = SelectBox(thick=0)
        area.update_color(WHITE)
        self.area = area

        area_text = InfoBox()
        self.area_text = area_text

    def update_rect(self, x, y, w, h):
        # set rect in area and area_text
        self.area.update_pos(x, y)
        self.area.update_wh(w, h)

        x, y = self.area.rect.center
        self.area_text.update_pos(x - w * 0.5, y - h * 0.5)
        self.area_text.update_wh(w, h)

    def update_text(self, title='', title_size=14, title_color=BLACK,
                    body='', body_size=10, body_color=BLACK,
                    line_space=10, indent=50, fit_size=35, n_col=1):
        if title:
            self.area_text.add_title(title=title, size=title_size, color=title_color)
        if body:
            self.area_text.add_body(body=body, size=body_size, color=body_color,
                                    line_space=line_space, indent=indent, fit_size=fit_size, n_col=n_col)

    def del_text(self):
        self.area_text.add_title(title='')
        self.area_text.add_body(body='')

    def display(self, screen):
        self.area.display(screen)
        if self.area_text.is_content:
            self.area_text.display(screen)


# --------------------------------------------------------------------- game control
class ControlBottom():
    def __init__(self, text, pos, size):
        area = SelectBox(thick=0, keep_active=False)
        area.update_color(WHITE)
        area.update_pos(x=pos[0], y=pos[1])
        area.update_wh(w=size[0], h=size[1])
        self.area = area

        area_text = WordBox(x=pos[0] + size[0] * 0.5,
                            y=pos[1] + size[1] * 0.5,
                            w=size[0],
                            h=size[1])
        area_text.add_text(text=text, color=BLACK, size=24, is_cap=False)
        self.area_text = area_text

        # if select by other object
        self.select = False

    def update_pos(self, x, y):
        # set rect in area and area_text
        self.area.update_pos(x, y)

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


# game control
class GameControl():
    def __init__(self):
        self.id = ''
        self.paramater = {'rep': 1, 'rep_reset': 1}
        self.action = {}

    def add_id(self, id):
        self.id = id

    def add_paramater(self, key, val):
        self.paramater[key] = val

    def add_action(self, val):
        self.action = val

    def update_rep(self, num):
        self.paramater['rep'] = num

    def rtn_action_active(self):
        action_active = []
        if self.action:
            for key, val in self.action.items():
                action_active.append(val[0])
        return action_active


# ----------------------------------------------------------------------- player
class subboard():
    def __init__(self, lv):
        # size and pos
        self.x = player_control_board_pos[0] + 10 + (player_control_subtext_size[0] + 20) * lv
        self.y = player_control_board_pos[1] + 5
        self.w = player_control_subtext_size[0] + 10
        self.h = player_control_subtext_size[1] - 5

        subboard = [[], []]
        self.subboard = subboard

        self.subboard_title = WordBox(x=self.x, y=self.y, w=self.w, h=self.h)
        self.subboard_title.add_text(' ', size=16, color=BLACK, as_rect=False)

        self.title = ''

        # maybe need to tracking system
        self.cur_mult_subboard = set()
        self.cur_uni_subboard = -1
        self.cur_is_mult = False
        self.has_active = False

    def add_subtext(self, key, infos):
        self.subboard = [[], []]
        self.cur_mult_subboard = set()
        self.cur_uni_subboard = -1
        self.cur_is_mult = False
        self.has_active = False

        if key in infos:
            self.subboard_title.add_text(text=infos[key][0], size=16, color=BLACK, as_rect=False)
            self.title = infos[key][0]

            color, text, keep_active = infos[key][1], infos[key][2], infos[key][3]

            for i in range(len(color)):
                if i < 5:
                    box = SelectBox(x=self.x, y=self.y + self.h * (i + 1),
                                    w=self.w, h=self.h, keep_active=False)
                    box_text = WordBox(x=self.x, y=self.y + self.h * (i + 1),
                                       w=self.w, h=self.h, keep_active=False)
                else:
                    box = SelectBox(x=self.x + self.w, y=self.y + self.h * (i + 1 - 5),
                                    w=self.w, h=self.h, keep_active=False)
                    box_text = WordBox(x=self.x + self.w, y=self.y + self.h * (i + 1 - 5),
                                       w=self.w, h=self.h, keep_active=False)

                box.update_color(color[i])
                box.update_method(keep_active)
                box_text.add_text(text[i], size=16, color=BLACK, as_rect=False)

                self.subboard[0].append(box)
                self.subboard[1].append(box_text)

    def handel_event(self, event):
        cur_active = []
        for i, box in enumerate(self.subboard[0]):
            box.handle_event(event)
            if box.active:
                cur_active.append(i)
                self.has_active = True

        # check how many active
        if cur_active:
            if len(cur_active) == 1:
                self.cur_is_mult = False
                self.cur_uni_subboard = cur_active[0]
            else:
                self.cur_is_mult = True
                self.cur_mult_subboard = set()
                for act in cur_active:
                    self.cur_mult_subboard.add(act)

    def rtn_select(self):
        if self.cur_is_mult:
            rtn = []
            if self.cur_mult_subboard:
                for i in self.cur_mult_subboard:
                    rtn.append(self.subboard[1][i].org_text)
                return rtn
        else:
            # check if get activate
            if self.has_active:
                return self.subboard[1][self.cur_uni_subboard].org_text

    def display(self, screen):
        if self.title:
            self.subboard_title.display(screen)

        for i, box in enumerate(self.subboard[0]):
            box.update_thick()
            if self.cur_is_mult:
                if box.active:
                    box.update_thick(0)
            else:
                if box.active or i == self.cur_uni_subboard:
                    box.update_thick(0)
            box.display_no_active(screen)

        for box in self.subboard[1]:
            box.display(screen)


# player control board
class PlayerBoard():
    def __init__(self):
        # whole board
        area = SelectBox(thick=0, keep_active=False)
        area.update_color(WHITE)
        area.update_pos(x=player_control_board_pos[0], y=player_control_board_pos[1])
        area.update_wh(w=player_control_board_size[0], h=player_control_board_size[1])
        self.area = area

        # subtext
        x = player_control_board_pos[0] + 10
        y = player_control_board_pos[1] + 5
        w, h = player_control_subtext_size
        subtext = ['Move', 'Build Lab', 'Find Cure', 'Treat disease', 'Share info']
        subtext_area = []
        for i, text in enumerate(subtext):
            box = WordBox(x=x, y=y + h * i, w=w, h=h, keep_active=False)
            box.add_text(text=text, size=16, color=BLACK, as_rect=False)
            subtext_area.append(box)
        self.subtext_area = subtext_area

        # subboard info
        # key = sub text
        # val:[title, 1st ls = color, to update select box; 2nd ls = text, update word box]
        self.subboard1_info = {}
        self.subboard2_info = {}

        self.cur_subtext_area = ''

        self.city_pick = ''

    def update_city_pick(self, city):
        self.city_pick = city

    def update_subboard_info(self, players, cur_player, active_city):
        # info for update
        city = cur_player.city
        hand = cur_player.hand
        hand_ls = [card.name for card in hand if card.type == 'city']
        hand_color = [card.color for card in hand if card.type == 'city']

        # compute the possible action
        # move
        if cur_player.move_other:
            move_ls = [player.name for player in players]
            move_color = [player.color for player in players]
        else:
            move_ls = [cur_player.name]
            move_color = [cur_player.color]

        card_to_use, card_to_use_color = [], []
        if cur_player.city.txt in hand_ls:
            card_to_use.append(cur_player.city.txt)
            card_to_use_color.append(color_rbky[cur_player.city.ctcolor])

        if active_city:
            self.city_pick = active_city
            if active_city.txt in hand_ls and active_city.txt not in card_to_use:
                card_to_use.append(active_city.txt)
                card_to_use_color.append(color_rbky[active_city.ctcolor])
        elif self.city_pick:
            if self.city_pick.txt in hand_ls and self.city_pick.txt not in card_to_use:
                card_to_use.append(self.city_pick.txt)
                card_to_use_color.append(color_rbky[self.city_pick.ctcolor])

        self.subboard1_info['Move'] = ['Whom', move_color, move_ls, False]
        self.subboard2_info['Move'] = ['Using Card', card_to_use_color, card_to_use, False]

        # build lab
        if cur_player.building_action:
            build_ls = ['Yes']
        else:
            build_ls = ['Yes'] if city.txt in hand_ls else ['Need city card']

        self.subboard1_info['Build Lab'] = ['Build', [WHITE], build_ls, False]

        # find cure
        if city.lab:
            cure_color = [val for val in color_rbky.values() if hand_color.count(val) >= cur_player.cure_need]
            cure_ls = ['cure'] * len(cure_color)

            cure_card = [card.name for card in hand if card.color in cure_color]
            cure_card_color = [card.color for card in hand if card.color in cure_color]
        else:
            cure_ls = ['City has no lab']
            cure_color = [WHITE]
            cure_card, cure_card_color = [], []

        self.subboard1_info['Find Cure'] = ['Which cure', cure_color, cure_ls, False]
        self.subboard2_info['Find Cure'] = ['Card to use', cure_card_color, cure_card, True]

        # treat
        treat_ls = [k for k, v in city.disease.items() if len(v) != 0]
        treat_color = [color_rbky[k] for k, v in city.disease.items() if len(v) != 0]

        self.subboard1_info['Treat disease'] = ['Which disease', treat_color, treat_ls, False]

        # share
        share_ppl = [player.name for player in players if player.city == city]
        share_ppl_color = [player.color for player in players if player.city == city]

        share_ppl.remove(cur_player.name)
        share_ppl_color.remove(cur_player.color)

        if not cur_player.sharelock:
            share_card = hand_ls
            share_card_color = hand_color
        else:
            share_card = [city.txt] if city.txt in hand_ls else []
            share_card_color = [color_rbky[city.ctcolor]] if city.txt in hand_ls else []

        self.subboard1_info['Share info'] = ['Whom', share_ppl_color, share_ppl, False]
        self.subboard2_info['Share info'] = ['Which Card', share_card_color, share_card, False]

    def rtn_subboard_info(self):
        return self.subboard1_info, self.subboard2_info

    def rtn_board_active(self):
        return self.area.active

    def rtn_select(self):
        if self.cur_subtext_area:
            return self.cur_subtext_area.org_text

    def add_player_color(self, color):
        self.area.update_active_color(color)
        for box in self.subtext_area:
            box.add_fill_color(color)

    def handle_event(self, event):
        self.area.handle_event(event)
#        if not self.area.active:
#            self.cur_subtext_area = ''

        for i, box in enumerate(self.subtext_area):
            box.handle_event(event)

            if box.active:
                self.cur_subtext_area = box

    def display(self, screen):
        self.area.display_active(screen, thick=3)
        for i, box in enumerate(self.subtext_area):
            if not box == self.cur_subtext_area:
                box.display(screen, draw_rect=True)
            else:
                box.display(screen, draw_rect=True, is_fill=True)


# player board summary
class PlayerBoardSummary():
    def __init__(self):
        # summary action
        area_text = InfoBox(x=player_board_summary_pos[0],
                            y=player_board_summary_pos[1])
        self.area_text = area_text

        # confirm bottom
        bottom = SelectBox(thick=0, keep_active=False)
        bottom.update_color(WHITE)
        bottom.update_pos(x=CONFIRM_bottom_pos[0], y=CONFIRM_bottom_pos[1])
        bottom.update_wh(w=CONFIRM_bottom_size[0], h=CONFIRM_bottom_size[1])
        self.bottom = bottom

        bottom_text = WordBox(x=CONFIRM_bottom_pos[0] + CONFIRM_bottom_size[0] * 0.5,
                              y=CONFIRM_bottom_pos[1] + CONFIRM_bottom_size[1] * 0.6,
                              w=CONFIRM_bottom_size[0], h=CONFIRM_bottom_size[1])
        bottom_text.add_text(text='Confirm', color=BLACK, size=20, is_cap=False)
        self.bottom_text = bottom_text

        self.select = False

        # player action left
        action_used = WordBox(x=player_board_summary_pos[0] + player_control_subtext_size[0] * 0.8,
                              y=CONFIRM_bottom_pos[1] + CONFIRM_bottom_size[1]*0.5)
        action_used.add_text(text=' ', size=18, color=BLACK, as_rect=False, to_center=False)
        self.action_used = action_used

    def add_summary(self, text):
        self.area_text.add_title(' ', size=2, color=BLACK)
        self.area_text.add_body(text, size=20, color=BLACK,
                                line_space=20, indent=10, fit_size=50, n_col=1)

    def update_player_action(self, player):
        text = 'Player action used: ' + str(player.action_used) + ' / ' + str(player.action)
        self.action_used.add_text(text=text, size=18, color=BLACK, as_rect=False)

    def handel_event(self, event):
        self.bottom.handle_event(event)

    def rtn_active(self):
        return self.bottom.active

    def set_active(self, active):
        self.bottom.active = active

    def display(self, screen):
        if self.select:
            self.bottom.update_color(ORANGE)
        else:
            self.bottom.update_color(WHITE)

        self.area_text.display(screen, draw_rect=False)
        self.bottom.display(screen)
        self.bottom_text.display(screen)
        self.action_used.display(screen)


# player
class Player():
    def __init__(self):
        self.pawn = ImgBox(w=player_pawn_size[0], h=player_pawn_size[1], keep_active=False)
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
        self.action_used = 0

        # might change base on character
        self.action = 4
        self.handlimit = 7
        self.cure_need = 5
        self.building_action = False
        self.supertreat = False
        self.sharelock = True
        self.move_other = False

    def playerNO_update(self, playerNO):
        self.playerNO = playerNO
        self.init_angle = 45 - 40 * (int(playerNO) - 1)
        self.pawn.rotate_img(self.init_angle)

        x = map_size[0] + 10
        y = 10 + (int(playerNO) - 1) * player_area_size[1]
        self.area.update_pos(x, y)
        self.area_text.update_pos(x, y)

    def pos_update(self, city):

        self.city = city
        x, y, w, h = city.rect
        # according to player#, adjust the pos
        # (city's w, play's w, city's h, play's h)
        pos_adjs = [(0, 0, 0, 0), (0, 1, 0, -0.3), (0, 2, 0, 0),
                    (1, 0.4, 0.5, 0), (1, 0.3, 1, 0.1), (0.5, 0.1, 1, 0.3)]
        pos_adj = pos_adjs[int(self.playerNO) - 1]
        update_x = x + city_size[0] * pos_adj[0] + player_pawn_size[0] * pos_adj[1]
        update_y = y + city_size[1] * pos_adj[2] + player_pawn_size[1] * pos_adj[3]

        self.pawn.update_pos(update_x, update_y)

        # self.city = city
        # self.pawn.update_pos(city.rect.x, city.rect.y)

    def rtn_active(self):
        return self.active

    def add_hand(self, card):
        self.hand.append(card)

    def discard_hand(self, card):
        # update the card's pos to discard pile
        card.update_pos(infection_card_img_pos[0] + infection_card_size[0] + 10, infection_card_img_pos[1])
        # rm from hand
        self.hand.remove(card)

    def display(self, screen):

        # draw pawn, player area
        self.active = True if self.pawn.rtn_active() != self.area.rtn_active() else False
        if self.active:
            self.pawn.rotate_img(self.init_angle + 8 * (round(time.time() % 360)))
            self.area.display_active(screen)
        else:
            self.pawn.rotate_img(self.init_angle)
            self.area.display_no_active(screen)
        self.pawn.display(screen, is_rect=False)
        self.area_text.display(screen)

        # draw player card
        # get the rect to calculate pos for each card
        x = self.area.rect.x + self.area.rect.w - player_card_size[0] * 0.5
        y = [self.area.rect.y + player_card_size[1] * 0.2,
             self.area.rect.y]
        for i in range(self.handlimit):
            # calculate
            cur_x = x - (i + 1) * player_card_size[0] * 0.5
            cur_y = y[1] if i % 2 else y[0]

            if i < len(self.hand):
                # update the card to that pos
                self.hand[i].update_pos(x=cur_x, y=cur_y)
                self.hand[i].display(screen)



class Scientist(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'grey'
        self.pawn.add_img(filename='\\img\\player_' + self.color_lab + '.png', size=self.pawn_size)
        self.color = color_Scientist
        self.name = 'Scientist'
        self.discribe = ['> Need only four cards for cure']

        self.area_text.add_text(text=self.name, color=BLACK, size=15, to_center=False)
        self.area_text.rotate_text(30)
        self.area.update_color(color_Scientist)

        # character ability
        self.cure_need = 4


class Researcher(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'yellow'
        self.pawn.add_img(filename='\\img\\player_' + self.color_lab + '.png', size=self.pawn_size)
        self.color = color_Researcher
        self.name = 'Researcher'
        self.discribe = ['> Give a player card from your hand for one action',
                         '> Both of you need to be at the same city']

        self.area_text.add_text(text=self.name, color=BLACK, size=15, to_center=False)
        self.area_text.rotate_text(30)
        self.area.update_color(color_Researcher)

        # character ability
        self.sharelock = False


class Medic(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'orange'
        self.pawn.add_img(filename='\\img\\player_' + self.color_lab + '.png', size=self.pawn_size)
        self.color = color_Medic
        self.name = 'Medic'
        self.discribe = [' > Remove all the same disease in the city when you treat',
                         ' > If the cure is found, no need to cost action for treat']

        self.area_text.add_text(text=self.name, color=BLACK, size=15, to_center=False)
        self.area_text.rotate_text(30)
        self.area.update_color(color_Medic)

        # character ability
        self.supertreat = False


class Dispatcher(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'purple'
        self.pawn.add_img(filename='\\img\\player_' + self.color_lab + '.png', size=self.pawn_size)
        self.color = color_Dispatcher
        self.name = 'Dispatcher'
        self.discribe = ["> Move other player in your turn ",
                         "> Move any player to another player's city for one action"]

        self.area_text.add_text(text=self.name, color=BLACK, size=15, to_center=False)
        self.area_text.rotate_text(30)
        self.area.update_color(color_Dispatcher)

        # character ability
        self.move_other = True


class OperationsExpert(Player):
    def __init__(self):
        super().__init__()
        self.color_lab = 'lightgreen'
        self.pawn.add_img(filename='\\img\\player_' + self.color_lab + '.png', size=self.pawn_size)
        self.color = color_OperationsExpert
        self.name = 'Operations Expert'
        self.discribe = [' > Build a research station in your city with one action']

        self.area_text.add_text(text=self.name, color=BLACK, size=15, to_center=False)
        self.area_text.rotate_text(30)
        self.area.update_color(color_OperationsExpert)

        # character ability
        self.building_action = True
