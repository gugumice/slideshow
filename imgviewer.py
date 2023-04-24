
#!/usr/bin/env python3
import pygame
import json
import sys
import time
import argparse


class Button():
    def __init__(self, target, width, height, pos, elevation, color, shadow, hover, debounce_s=1):
        self.target = target
        self.elevation = elevation
        self.original_y_pos = pos[1]
        self.color = color
        self.color_shadow = shadow
        self.hover = hover
        self.clicked = False
        self.timer = time.time_ns()
        self.debounce_s = debounce_s
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = color
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = shadow

    def draw_button(self):
        def timer_off(ct, ti, deb): return ct-ti > deb*10**9

        action = False
        pos = pygame.mouse.get_pos()
        top_rect = self.top_rect.copy()
        bottom_rect = self.bottom_rect.copy()
        bottom_rect.x += 5
        bottom_rect.y += 5
        if top_rect.collidepoint(pos):
            self.top_color = self.color
            if pygame.mouse.get_pressed()[0]:
                if timer_off(time.time_ns(), self.timer, self.debounce_s):
                    self.clicked = True
                    self.timer = time.time_ns
                    bottom_rect.inflate_ip(self.elevation, self.elevation)
                    top_rect.inflate_ip(self.elevation, self.elevation)

            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
            self.top_color = self.hover
        else:
            self.top_color = self.color

        bottom_surf = pygame.Surface(bottom_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(bottom_surf, self.bottom_color,
                         (0, 0, *bottom_rect.size), border_radius=12)
        screen.blit(bottom_surf, bottom_rect.topleft)
        top_surf = pygame.Surface(top_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(top_surf, self.top_color,
                         (0, 0, *top_rect.size), border_radius=12)
        screen.blit(top_surf, top_rect.topleft)
        return (action)


def load_images(d):
    dict = {}
    for i in d.keys():
        img = pygame.image.load(i)
        img = pygame.transform.smoothscale(img, (width, height))
        dict.update({i: img})
    return (dict)


def set_buttons(curr_pict, pl_list):
    butt = []
    try:
        butt_data = pl_list[curr_pict]
    except KeyError:
        # key not found, goto first
        butt_data = pl_list[list(pl_list.keys())[0]]
    for b in butt_data:
        for k in b.keys():
            btn_data = b[k]
            # b=(btn_data['pict'],btn_data['width'],btn_data['height'],(btn_data['xpos'],btn_data['ypos'],ELEVATION,COLOR, SHADOW, HOVER))
            butt.append(Button(btn_data['pict'], btn_data['width'], btn_data['height'], (btn_data['xpos'], btn_data['ypos']),
                               ELEVATION, COLOR, SHADOW, HOVER,))
    return (butt)


def main():
    filename = args.filename
    try:
        with open(filename) as f:
            play_list = json.load(f)
    except FileNotFoundError:
        print('File not found: {}'.format(filename))
        sys.exit(1)
    # Load images into dict
    img_dict = load_images(play_list)
    current_pict = list(img_dict.keys())[0]

    pygame.display.set_caption(current_pict)
    fnt = pygame.font.SysFont("monospace", 15)
    # If -v arg
    pict_name_img = fnt.render(current_pict, True, (255, 255, 255))
    pict_name_rect = pict_name_img.get_rect()
    pict_name_rect.topleft = (1, 1)
    buttons = []
    # If no activity, goto first slide
    idle_timer = time.time()
    running = True

    while running:
        # check timer
        if time.time() > idle_timer + TIMEOUT:
            idle_timer = time.time()
            current_pict = list(img_dict.keys())[0]
            buttons = []
            #print(time.asctime())
        # set buttons
        if len(buttons) == 0:
            buttons = set_buttons(current_pict, play_list)
        # Event loop
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
                # print(button.target)
                current_pict = button.target
                buttons = []
                idle_timer = time.time()
                break

        if args.visible:
            '''
            Grid for positioning buttons
            '''
            x = y = 0
            line_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            while x < width:
                x += 100
                pygame.draw.line(line_surf, '#ffffffdd',
                                 (x, 0), (x, height), 1)
                xcoord_img = fnt.render('{}'.format(x), True, (0, 0, 0))
                xcoord_rect = xcoord_img.get_rect()
                xcoord_rect.topleft = (x, 10)
                screen.blit(xcoord_img, xcoord_rect)

            while y < height:
                y += 100
                pygame.draw.line(line_surf, '#ffffffdd', (0, y), (width, y), 1)
                ycoord_img = fnt.render('{}'.format(y), True, (0, 0, 0))
                ycoord_rect = ycoord_img.get_rect()
                ycoord_rect.topleft = (10, y)
                screen.blit(ycoord_img, ycoord_rect)

            screen.blit(line_surf, (0, 0))
            screen.blit(pict_name_img, pict_name_rect)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PyGame image kiosk',
                                     description='Slide show',
                                     epilog='We apoligize for any inconveniance')
    parser.add_argument('filename',
                        help='Playlist file ".json"',)
    parser.add_argument('-v', '--visible',
                        action='store_true',
                        help='Make command buttons visible',
                        required=False,
                        default=False
                        )
    parser.add_argument('-r', '--resolution', nargs='+',
                        type=int,
                        metavar='x,y',
                        required=False,
                        help='Custom Screen size (h,v)')
    parser.add_argument('-i', '--idle',
                        metavar='mins',
                        default=5,
                        type=int,
                        required=False,
                        help='Idle timer (mins), default: 5')
    parser.add_argument('-d', '--debounce',
                        metavar='secs',
                        default=.5,
                        type=float,
                        required=False,
                        help='Time (secs) buttons are blocked after action, default: 0.5',
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
    # Idle timeout. Return to first slide if no action
    TIMEOUT = int(args.idle)*60
    pygame.init()
    if args.resolution is None:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        try:
            screen = pygame.display.set_mode(
                (int(args.resolution[0]), int(args.resolution[1])))
        except IndexError:
            print('Invalid screen parameters: {}'.format(list(args.resolution)))
            pygame.quit()
            sys.exit(0)
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    main()
    pygame.quit()
    sys.exit(0)
