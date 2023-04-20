
#!/usr/bin/env python3
import pygame
import json
import sys
import time
import argparse

#DEFAULT_SIZE = (1280,800)
DEFAULT_SIZE = (1920,1080)

pygame.init()
#screen = pygame.display.set_mode(DEFAULT_SIZE)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

class Button():
    def __init__(self, target, width, height, pos, elevation, color, shadow, hover, debounce_ms = 1000):
        self.target = target
        self.elevation = elevation
        self.original_y_pos = pos[1]
        self.color = color
        self.color_shadow = shadow
        self.hover = hover
        self.clicked = False
        self.timer = int(time.time_ns()/1000)
        self.debounce_ms = debounce_ms
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = color
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = shadow

    def draw_button(self):
        action = False
        pos = pygame.mouse.get_pos()
        top_rect = self.top_rect.copy()
        bottom_rect = self.bottom_rect.copy()
        bottom_rect.x += 5
        bottom_rect.y += 5
        if top_rect.collidepoint(pos):
            self.top_color = self.color
            #Debounce
            if pygame.mouse.get_pressed()[0]:
                if int(time.time_ns()/1000) > self.timer + self.debounce_ms:
                    self.clicked = True
                    #Update timer
                    timer = int(time.time_ns()/1000)
                    bottom_rect.inflate_ip(self.elevation, self.elevation)
                    top_rect.inflate_ip(self.elevation, self.elevation)

            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
            self.top_color = self.hover
        else:
            self.top_color = self.color

        bottom_surf = pygame.Surface(bottom_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(bottom_surf, self.bottom_color, (0, 0, *bottom_rect.size), border_radius = 12)
        screen.blit(bottom_surf, bottom_rect.topleft)
        top_surf = pygame.Surface(top_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(top_surf, self.top_color, (0, 0, *top_rect.size), border_radius = 12)
        screen.blit(top_surf, top_rect.topleft)
        return(action)

def load_images(d):
    '''
    Load images into dict
    '''
    dict = {}
    for i in d.keys():
        img = pygame.image.load(i)
        #img = pygame.transform.scale(img, DEFAULT_SIZE)
        dict.update({i:img})
    return(dict)
def set_buttons(curr_pict,pl_list):
    '''
    Set nav buttons
    '''
    butt=[]
    try:
        butt_data = pl_list[curr_pict]
    except KeyError:
        #key not found, goto first
        butt_data = pl_list[list(pl_list.keys())[0]]
    for b in butt_data:
        for k in b.keys():
            btn_data=b[k]
            #b=(btn_data['pict'],btn_data['width'],btn_data['height'],(btn_data['xpos'],btn_data['ypos'],ELEVATION,COLOR, SHADOW, HOVER))
            butt.append(Button(btn_data['pict'],btn_data['width'],btn_data['height'],(btn_data['xpos'],btn_data['ypos']),
                               ELEVATION,COLOR, SHADOW, HOVER))
    return(butt)

def main():

    filename = args.filename
    #filename = 'pln1.json'
    try:
        with open(filename) as f:
            play_list = json.load(f)
    except FileNotFoundError:
        print('File not found: {}'.format(filename))
        sys.exit(1)

    #Load images into dict
    img_dict = load_images(play_list)
    current_pict = list(img_dict.keys())[0]
    pygame.display.set_caption(current_pict)
    buttons = []
    timer = time.time()
    running = True
    while running:
        #check timer
        if time.time()>timer + TIMEOUT:
            timer = time.time()
            current_pict = list(img_dict.keys())[0]
            buttons = []
        #set buttons
        if len(buttons) == 0:
            buttons = set_buttons(current_pict,play_list)
        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update the display
        screen.fill((0, 0, 0))
        try:
            screen.blit(img_dict[current_pict], (0, 0))
        except KeyError:
            screen.blit(img_dict[list(img_dict.keys())[0]], (0, 0))
        for button in buttons:
            button.draw_button()
            if button.clicked:
                #print(button.target)
                current_pict = button.target
                buttons = []
                break
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Slide show')
    parser.add_argument('filename',
                        help='Playlist file .json',)
    parser.add_argument('-v','--visible',
                        action='store_true',
                        help='Make command buttons visible',
                        required=False,
                        default=False
                        )

    args = parser.parse_args()
    if args.visible:
        COLOR = (128, 128, 255, 50)
        SHADOW = (64, 64, 128, 20)
        HOVER = (255, 128, 255, 20)
    else:
        COLOR = (128, 128, 255, 0)
        SHADOW = (64, 64, 128, 0)
        HOVER = (255, 128, 255, 20)
    ELEVATION = 5
    TIMEOUT=5*60
    main()
    pygame.quit()
    sys.exit(0)

