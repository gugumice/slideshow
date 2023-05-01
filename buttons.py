#/usr/bin/env python3
import pygame, sys
import time
BORDER_RADIUS = 5
BUTTON_TOP_COLOR = '#475F77'
BUTTON_TEXT_COLOR = '#FFFFFF'
BUTTON_HOOVER_COLOR = '#D74B4B'
BUTTON_BOTTOM_COLOR = '#354B5E'
def fn1():
    print('button1 clicked {}'.format(time.perf_counter()))

class Button(object):
    def __init__(self,text,width,height,pos,cb_func,elevation = 3, button_delay = .5) -> None:
        #Button delay
        self.timer = time.perf_counter()
        self.button_delay = button_delay
        
        self.pressed = False
        self.elevation = self.dyn_elevation = elevation
        self.def_y_pos = pos[1]
        #Top rect
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = BUTTON_TOP_COLOR
        #Text
        self.text_surf = gui_font.render(text,True,BUTTON_TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        #Bottom rect
        self.bottom_rect = pygame.Rect(pos,(width,elevation))
        self.bottom_color = BUTTON_BOTTOM_COLOR
        self.func = cb_func
    def call_back(self, *args):
        if self.func:
            return(self.func(*args))

    def draw(self):
        #elevation logic
        self.top_rect.y = self.def_y_pos - self.dyn_elevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dyn_elevation
        pygame.draw.rect(screen,self.top_color,self.top_rect,border_radius=BORDER_RADIUS)
        screen.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = BUTTON_HOOVER_COLOR
            if pygame.mouse.get_pressed()[0]:
                if time.perf_counter() > self.timer + self.button_delay:
                    self.dyn_elevation = 0
                    self.pressed = True
                    self.timer = time.perf_counter()
            else:
                if self.pressed == True:
                    self.call_back()
                    self.dyn_elevation = self.elevation
                    self.pressed = False
        else:
            self.dyn_elevation = self.elevation
            self.top_color = BUTTON_TOP_COLOR
def main(): 

    button1 = Button('Click me', 200,40,(200,200),fn1,elevation=3)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                running = False
        screen.fill('#DCDDD8')
        button1.draw()

        pygame.display.update()
        clock.tick(60)

    pygame.QUIT
    sys.exit(0)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption('Gui menu')
    clock = pygame.time.Clock()
    gui_font = pygame.font.Font(None,30)
    main()