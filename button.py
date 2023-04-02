#!/usr/bin/env python3
#https://stackoverflow.com/questions/72352081/how-to-create-button-with-transparent-background-and-shadow-in-pygame
#https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_ui_elements.md

import pygame

class Button():
    def __init__(self, text, width, height, pos, elevation, image, color, shadow, hover):
        #self.image = pygame.transform.scale(image, (int(width), int(height)))
        #self.rect = self.image.get_rect()
        self.elevation = elevation
        self.original_y_pos = pos[1]
        self.color = color
        self.color_shadow = shadow
        self.hover = hover
        self.clicked = False
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = color
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = shadow
        font = pygame.font.SysFont('rockwell', 50)
        self.text_surf = font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw_button(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        top_rect = self.top_rect.copy()
        bottom_rect = self.bottom_rect.copy()
        bottom_rect.x += 20
        bottom_rect.y += 20
        if top_rect.collidepoint(pos):
            self.top_color = self.color
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
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

        screen.blit(self.text_surf, self.text_rect)
        return action

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
ts, w, h, c1, c2 = 50, *screen.get_size(), (128, 128, 128), (96, 96, 96)
tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
for rect, color in tiles:
    pygame.draw.rect(background, color, rect)

font = pygame.font.SysFont(None, 80)
text = font.render("Button", True, (255, 255, 255))

button = Button("Button", 200, 70, (80, 120), 20, None, (128, 128, 255, 128), (64, 64, 128, 128), (255, 128, 255, 128))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False          

    screen.blit(background, (0, 0))
    button.draw_button(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()
