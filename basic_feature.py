import os
import string
import pygame as pg

from paramater import *

pg.init()


def content_fit(content, size=1000):
    if not isinstance(content, list):
        content = [content]
    # let content fit
    fit = []
    for con in content:
        if len(con) > size:
            c = con.split()
            while len(' '.join(c)) > (size - 5):
                con_temp = []
                while len(' '.join(con_temp)) < (size - 5) and c:
                    con_temp.append(c.pop(0))
                if con_temp:
                    fit.append(' '.join(con_temp))
            if c:
                fit.append(' '.join(c))

        else:
            fit.append(con)
    return fit


class SelectBox():
    def __init__(self, x=0, y=0, w=10, h=10, color=BLACK, thick=2, keep_active=True, to_drag=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.thick = thick
        self.rect = pg.Rect(x, y, w, h)

        # for selecting (for game control)
        self.select = False

        self.click = False

        # for active (if mouse click on the object)
        self.fill_color = WHITE
        self.active_color = RED
        self.keep_active = keep_active
        self.active = False
        self.hit = 0

        # for dragging
        self.to_drag = to_drag
        self.drag = False
        self.offset_x = 0
        self.offset_y = 0

    def update_method(self, method):
        self.keep_active = method

    def update_wh(self, w, h):
        self.w = w
        self.h = h
        self.rect.w = w
        self.rect.h = h

    def update_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def add_fill_color(self, color):
        self.fill_color = color

    def update_color(self, color):
        self.color = color

    def update_active_color(self, color):
        self.active_color = color

    def update_thick(self, thick=2):
        self.thick = thick

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # for dragging
            if event.button == 1 and self.to_drag:
                if self.rect.collidepoint(event.pos):
                    self.drag = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y

            # for selecting
            if self.rect.collidepoint(event.pos):
                self.hit += 1
                self.active = True if not self.keep_active else False
                self.click = True
            else:
                self.active = False

            if self.keep_active:
                self.active = True if self.hit % 2 else False


        elif event.type == pg.MOUSEBUTTONUP:
            # for dragging
            if event.button == 1 and self.to_drag:
                self.drag = False
            self.click = False

        elif event.type == pg.MOUSEMOTION:
            # for dragging
            if self.drag:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

    def update_active(self, active):
        self.active = active

    def rtn_active(self):
        return self.active

    def rtn_click(self):
        return self.click

    def update_select(self, select):
        self.select = select

    def rtn_select(self):
        return self.select

    def display(self, screen, select=False, is_rect=False, active_off=False, is_fill=False):
        pg.draw.rect(screen, self.color, self.rect, self.thick)

        if is_rect:
            pg.draw.rect(screen, BLACK, self.rect, 2)

        if (self.active or select) and not active_off:
            pg.draw.rect(screen, self.active_color, self.rect, 2)

    def display_active(self, screen, thick=2):
        pg.draw.rect(screen, self.color, self.rect, self.thick)
        pg.draw.rect(screen, self.active_color, self.rect, thick)

    def display_no_active(self, screen):
        pg.draw.rect(screen, self.color, self.rect, self.thick)


class ImgBox(SelectBox):
    def __init__(self, x=0, y=0, w=10, h=10, color=BLACK, thick=2, keep_active=True, to_drag=False):
        super().__init__(x=x, y=y, w=w, h=h, color=color, thick=thick, keep_active=keep_active, to_drag=to_drag)

    def add_img(self, filename, size, as_rect=True, to_center=True):
        # image
        image = pg.image.load(os.getcwd() + filename)
        self.raw_image = image
        self.size = size
        self.image = pg.transform.scale(image, size)

        if as_rect:
            if to_center:
                self.rect = self.image.get_rect(center=(self.x, self.y))
            else:
                self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.as_rect = as_rect
        self.to_center = to_center

    def rotate_img(self, rotate=0):
        image = pg.transform.scale(self.raw_image, self.size)
        self.image = pg.transform.rotate(image, rotate)

        if self.as_rect:
            if self.to_center:
                self.rect = self.image.get_rect(center=(self.x, self.y))
            else:
                self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def display(self, screen, select=False, is_rect=True):
        if self.as_rect:
            screen.blit(self.image, self.rect)
        else:
            image_rect = self.image.get_rect(center=self.rect.center)
            screen.blit(self.image, image_rect)

        if self.active or self.select:
            if is_rect:
                pg.draw.rect(screen, self.color, self.rect, self.thick)


class WordBox(SelectBox):
    def __init__(self, x=0, y=0, w=10, h=10, color=BLACK, thick=2, keep_active=True, to_drag=False):
        super().__init__(x=x, y=y, w=w, h=h, color=color, thick=thick, keep_active=keep_active, to_drag=to_drag)
        self.as_rect = True
        self.text = ''

    def add_text(self, text, size, color, as_rect=True, to_center=True, is_cap=True):
        text = str(text)
        self.name = text
        self.org_text = text
        self.text_size = size
        self.text_color = color

        self.font = pg.font.SysFont('Calibri', size, True, False)
        if is_cap:
            self.text = self.font.render(string.capwords(self.org_text), True, color)
        else:
            self.text = self.font.render(self.org_text, True, color)

        if as_rect:
            if to_center:
                self.rect = self.text.get_rect(center=(self.x, self.y))
            else:
                self.rect = self.text.get_rect(topleft=(self.x, self.y))
        self.as_rect = as_rect
        self.to_center = to_center
        self.is_cap = is_cap

    def rotate_text(self, rotate):
        text = self.font.render(self.org_text, True, self.text_color)
        self.text = pg.transform.rotate(text, rotate)

        if self.as_rect:
            if self.to_center:
                self.rect = self.text.get_rect(center=(self.x, self.y))
            else:
                self.rect = self.text.get_rect(topleft=(self.x, self.y))

    def display(self, screen, select=False, is_fill=False, is_rect=False, draw_rect=False):
        if is_fill:
            pg.draw.rect(screen, self.fill_color, self.rect, 0)

        if draw_rect:
            pg.draw.rect(screen, self.color, self.rect, self.thick)

        if self.as_rect:
            screen.blit(self.text, self.rect)
        else:
            content = content_fit(content=self.org_text, size=35)
            for txt in content:
                if self.is_cap:
                    text = self.font.render(string.capwords(txt), True, self.text_color)
                else:
                    text = self.font.render(txt, True, self.text_color)
                if self.to_center:
                    text_rect = text.get_rect(center=self.rect.center)
                else:
                    text_rect = text.get_rect(topleft=self.rect.topleft)

                screen.blit(text, text_rect)

        if self.active or select:
            if not is_rect:
                pg.draw.rect(screen, self.color, self.rect, self.thick)


class InfoBox(SelectBox):
    def __init__(self, x=0, y=0, w=10, h=10, color=BLACK, keep_active=True, to_drag=False):
        super().__init__(x=x, y=y, w=w, h=h, color=color, keep_active=keep_active, to_drag=to_drag)
        self.is_content = False
        self.title = ''
        self.body = ''

    def add_title(self, title, size=32, color=BLACK):
        font = pg.font.SysFont('Calibri', size, True, False)
        self.title = font.render(string.capwords(title), True, color)
        self.is_content = True if title else False
        self.title_size = size

    def add_body(self, body, size=24, color=BLACK, line_space=15, indent=50, fit_size=35, n_col=1):
        self.body = body if isinstance(body, list) else [body]
        self.FONT_body = pg.font.SysFont('Calibri', size, True, False)
        self.line_space = line_space
        self.indent = indent
        self.body_color = color

        self.is_content = True if body else False
        self.fit_size = fit_size
        self.n_col = n_col

    def display(self, screen, thick=2, select=False):

        # Blit the title
        if self.title:
            screen.blit(self.title, (self.x + 10, self.y + 5))

        # Blit the body

        full_txt = []
        for i, txt in enumerate(self.body):
            content = content_fit(txt, self.fit_size)
            for text in content:
                full_txt.append(text)

        n_col = self.n_col
        n_row = int(len(full_txt) / n_col)

        w = self.w // n_col
        h = self.h // n_row

        x = self.x
        for col in range(n_col):
            i = 0
            y = self.y + self.title_size
            for txt in full_txt[col * n_row: (col + 1) * n_row]:
                body_surface = self.FONT_body.render(txt, True, self.body_color)
                body_rect = pg.Rect(x + self.indent, y + (i + 1) * self.line_space,
                                    w, h)
                screen.blit(body_surface, body_rect)
                i += 1
                # y += h*0.8
                # y += 2
            x += w
            x += 2

            # Blit the rect.
        rect = pg.Rect(self.x, self.y, self.w, self.h)
        pg.draw.rect(screen, self.color, rect, thick)


class Link():
    def __init__(self, pos1, pos2, color=BLACK, thick=3):
        self.pos1 = pos1
        self.pos2 = pos2
        self.color = (100, 100, 100)
        self.thick = thick

        self.active_color = color

        # for selecting
        self.active = False

    def set_active(self, active):
        self.active = active

    def display(self, screen):
        color = self.active_color if self.active else self.color
        pg.draw.line(screen, color, self.pos1, self.pos2, self.thick)
