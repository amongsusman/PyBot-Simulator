import pygame
import os
import random
import time
import math

pygame.init()

#fonts 
gen = pygame.font.SysFont("Calibri", 30)

#constants
FPS = 60
WIDTH, HEIGHT = 1200, 800

#colors
WHITE = (255, 255, 255)

#images

#sfx

#player variables
user_text = ""
input_rect = pygame.Rect(0, (HEIGHT / 2) + 100, WIDTH, (HEIGHT - ((HEIGHT / 2) + 100)))
active = False
text_surface = gen.render(user_text, True, (0, 0, 0)) 

#classes
class ObjectInterface():
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
    def getXpos(self):
        return self.xpos
    def getYpos(self):
        return self.ypos
    def changeXpos(self, amount):
        self.xpos += amount
    def changeYpos(self, amount):
        self.ypos += amount

class Player():
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
    def getXpos(self):
        return [self.x1, self.x2, self.x3]
    def getYpos(self):
        return [self.y1, self.y2, self.y3]
    def changeXpos(self, amount):
        self.x1 += amount
        self.x2 += amount
        self.x3 += amount
    def changeYpos(self, amount):
        self.y1 += amount
        self.y2 += amount
        self.y3 += amount
#window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyBot Simulator")

def draw_window(pxs, pys):
    window.fill(WHITE)
    pygame.draw.line(window, (0, 0, 0), (0, (HEIGHT / 2) + 100), (WIDTH, (HEIGHT / 2) + 100), 5)
    window.blit(text_surface, (input_rect.x+100, input_rect.y+100))
    pygame.draw.polygon(window, (128, 128, 128), [[pxs[i], pys[i]] for i in range(3)])
    pygame.display.update()

def MOVE_FORWARD():
    pass
def ROTATE_LEFT():
    pass
def ROTATE_RIGHT():
    pass

def main():
    global user_text
    clock = pygame.time.Clock()
    clock.tick(FPS)
    run = True
    robot = Player(100, 100, 100, 130, 125, 115)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RIGHT:
                    robot.changeXpos(30)
                elif event.key == pygame.K_LEFT:
                    robot.changeXpos(-30)
                elif event.key == pygame.K_UP:
                    robot.changeYpos(-30)
                elif event.key == pygame.K_DOWN:
                    robot.changeYpos(30)
                if event.key == pygame.K_BACKSPACE: 
                    user_text = user_text[:-1] 
                else: 
                    user_text += event.unicode

        draw_window(robot.getXpos(), robot.getYpos())
    pygame.quit()

if __name__ == "__main__":
    main()

#things to do 
    #- algae (make smaller)
    #- bots



