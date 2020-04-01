import os
import string
import pygame as pg

from paramater import*

pg.init()

def content_fit(content, size = 1000):
    if not isinstance(content, list):
        content = [content]
    # let content fit
    content_fit = []
    for con in content:
        if len(con) > size:
            c = con.split()
            while len(' '.join(c)) > (size -5):
                con_temp = []
                while len(' '.join(con_temp)) < (size -5) and c:
                    con_temp.append(c.pop(0))
                if con_temp:
                    content_fit.append(' '.join(con_temp))
            if c:
                content_fit.append(' '.join(c))
                    
        else:
            content_fit.append(con)
    return content_fit


class SelectBox():
    def __init__(self, x=0, y=0, w=10, h=10, color = BLACK, thick = 2, keep_select = True, to_drag = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.select_color = RED
        self.thick = thick
        self.rect = pg.Rect(x,y,w,h)
        
        # for selecting
        self.keep_select = keep_select
        self.active = False
        self.hit = 0
        
        # for dragging
        self.to_drag = to_drag
        self.drag = False
        self.offset_x = 0
        self.offset_y = 0
        
    def update_wh(self,w,h):
        self.x = x
        self.y = y
        self.rect.w = w
        self.rect.h = h        
    
    def update_pos(self,x,y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def update_color(self, color):
        self.color = color

    def handle_event(self,event):
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
                self.active = True if not self.keep_select else False
            else:
                self.active = False
            
            if self.keep_select:
                self.active = True if self.hit % 2 else False

        elif event.type == pg.MOUSEBUTTONUP:
            # for dragging
            if event.button == 1 and self.to_drag:
                self.drag = False
        
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

    def display(self, screen, select = False):
        pg.draw.rect(screen, self.color, self.rect, self.thick)

        if self.active or select:
            pg.draw.rect(screen, self.select_color, self.rect, 2)

    def display_select(self, screen, select = False):
        pg.draw.rect(screen, self.color, self.rect, self.thick)
        pg.draw.rect(screen, self.select_color, self.rect, 3)

    def display_no_select(self, screen, select = False):
        pg.draw.rect(screen, self.color, self.rect, self.thick)
    



class ImgBox(SelectBox):
    def __init__(self, x=0, y=0, w=10, h=10, color = BLACK, thick = 2, keep_select = True, to_drag = False):
        super().__init__(x=x, y=y, w=w, h=h, color = color, thick = thick, keep_select = keep_select, to_drag = to_drag)

    def add_img(self, filename, size, as_rect = True, to_center = True):
        # image
        image = pg.image.load(os.getcwd() + filename)
        self.raw_image = image
        self.size = size
        self.image = pg.transform.scale(image, size)
        
        if as_rect:
            if to_center:
                self.rect = self.image.get_rect(center = (self.x, self.y))
            else:
                self.rect = self.image.get_rect(topleft = (self.x, self.y))
        
        self.as_rect = as_rect
        self.to_center = to_center
        
    def rotate_img(self, rotate = 0):
        image = pg.transform.scale(self.raw_image, self.size)
        self.image = pg.transform.rotate(image, rotate)
              
        if self.as_rect:
            if self.to_center:
                self.rect = self.image.get_rect(center = (self.x, self.y))
            else:
                self.rect = self.image.get_rect(topleft = (self.x, self.y))                
 
    def display(self, screen, select = False):
        if self.as_rect:
            screen.blit(self.image, self.rect)
        else:
            image_rect = self.image.get_rect(center = self.rect.center)
            screen.blit(self.image, image_rect)
        
        if self.active or select:
            pg.draw.rect(screen, self.color, self.rect, self.thick)

    def display_no_rect(self, screen, select = False):
        if self.as_rect:
            screen.blit(self.image, self.rect)
        else:
            image_rect = self.image.get_rect(center = self.rect.center)
            screen.blit(self.image, image_rect)
        


class WordBox(SelectBox):
    def __init__(self, x=0, y=0, w=10, h=10, color = BLACK, thick = 2, keep_select = True, to_drag = False):
        super().__init__(x=x, y=y, w=w, h=h, color = color, thick = thick, keep_select = keep_select, to_drag = to_drag)
        self.fill_color = ''

    def add_fill_color(self, color):
        self.fill_color = color
        
    def add_text(self, text, size, color, rotate = 0, as_rect = True, to_center = True):
        self.name = text
        self.org_text = string.capwords(text)
        self.text_size = size
        self.text_color = color
        self.font = pg.font.SysFont('Calibri', size, True, False)
        text = self.font.render(string.capwords(text), True, color)
        self.text = pg.transform.rotate(text, rotate) if rotate else text
        if as_rect:
            if to_center:
                self.rect = self.text.get_rect(center = (self.x, self.y))
            else:
                self.rect = self.text.get_rect(topleft = (self.x, self.y))
        self.as_rect = as_rect
        self.to_center = to_center

    def display(self, screen, select = False):
        if self.as_rect:
            screen.blit(self.text, self.rect)
        else:
            content = content_fit(content=self.org_text, size = 35)
            for txt in content:
                text = self.font.render(string.capwords(txt), True, self.color)
                if self.to_center:
                    text_rect = text.get_rect(center = self.rect.center)
                else:
                    text_rect = text.get_rect(topleft = self.rect.topleft)
                screen.blit(text, text_rect)
        
        if self.active or select:
            pg.draw.rect(screen, self.color, rect, self.thick)
            


class InfoBox(SelectBox):
    def __init__(self, x=0, y=0, w=10, h=10, color = BLACK, keep_select = True, to_drag = False):
        super().__init__(x=x, y=y, w=w, h=h, color = color, keep_select = keep_select, to_drag = to_drag)

    def add_title(self, title, size = 32, color = BLACK):
        font= pg.font.SysFont('Calibri', size, True, False)
        self.title = font.render(title, True, color)
    
    def add_body(self, body, size = 24, color = BLACK, line_space = 25, indent = 50):
        self.body = body if isinstance(body, list) else [body]
        self.FONT_body = pg.font.SysFont('Calibri', size, True, False)
        self.line_space = line_space
        self.indent = indent
        self.body_color = color

    def display(self, screen, thick = 2, select = False):
        
        # Blit the title
        screen.blit(self.title, (self.x+10, self.y+5))
        
        # Blit the body
        n = len(self.body)
        for i, txt in enumerate(self.body):
            content = content_fit(txt)
            for text in content:
                body_surface = self.FONT_body.render(txt, True, self.body_color)
                body_rect = pg.Rect( self.x+ self.indent, self.y + (i+1) * self.line_space,
                               self.w//2, self.h//n)
                screen.blit(body_surface, body_rect)
        
        # Blit the rect.
        rect = pg.Rect(self.x, self.y, self.w, self.h)
        pg.draw.rect(screen, self.color, rect, thick)


class Link():
    def __init__(self, pos1, pos2, color = BLACK, thick = 3):
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
        
        

class de_ImgBox(SelectBox):
    def __init__(self, x=0, y=0, w=10, h=10, color = BLACK, thick = 2, keep_select = True, to_drag = False):
        super().__init__(x=x, y=y, w=w, h=h, color = color, thick = thick, keep_select = keep_select, to_drag = to_drag)

    def add_img(self, filename, size, as_rect = True, to_center = True):
        # image
        image = pg.image.load(os.getcwd() + filename)
        self.raw_image = image
        self.size = size
        self.image = pg.transform.scale(image, size)
        
        if as_rect:
            if to_center:
                self.rect = self.image.get_rect(center = (self.x, self.y))
            else:
                self.rect = self.image.get_rect(topleft = (self.x, self.y))
        
        self.as_rect = as_rect
        self.to_center = to_center
        
    def rotate_img(self, rotate = 0):
        image = pg.transform.scale(self.raw_image, self.size)
        self.image = pg.transform.rotate(image, rotate)
        
        if self.as_rect:
            if self.to_center:
                self.rect = self.image.get_rect(center = (self.x, self.y))
            else:
                self.rect = self.image.get_rect(topleft = (self.x, self.y))                
 
    def display(self, screen):
        if self.as_rect:
            screen.blit(self.image, self.rect)
        else:
            image_rect = self.image.get_rect(center = self.rect.center)
            screen.blit(self.image, image_rect)
        
        if self.active:
            pg.draw.rect(screen, self.color, self.rect, self.thick)