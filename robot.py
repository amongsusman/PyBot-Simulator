import pygame
import os
import random
import time
import math

pygame.init()

#fonts 
gen = pygame.font.SysFont("consolas", 25)
gen2 = pygame.font.SysFont("consolas", 50)
gen3 = pygame.font.SysFont("consolas", 15)

#constants
FPS = 60
WIDTH, HEIGHT = 1200, 800

#colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

#sfx

#simulator variables
user_text = ""
input_rect = pygame.Rect(0, (HEIGHT / 2) + 100, WIDTH, (HEIGHT - ((HEIGHT / 2) + 100)))
run_button = pygame.Rect(WIDTH / 2 - 50, (HEIGHT / 2) + 100, 100, 45)
active = False
last = pygame.time.get_ticks()
delay = 100
cur_except = ""

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
    
#player variables
robot = Player(0, 0, 0, 50, 50, 25)    

#window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyBot Simulator")

def draw_grid():
    for x in range(0, WIDTH, 50):
        pygame.draw.line(window, BLACK, (x, 0), (x, (HEIGHT // 2) + 100))
    for y in range(0, (HEIGHT // 2) + 100, 50):
        pygame.draw.line(window, BLACK, (0, y), (WIDTH, y))
            
def drawText():
    lines = user_text.splitlines()
    for i, line in enumerate(lines):
        code = gen.render(line, True, BLACK) 
        window.blit(code, (10, (HEIGHT / 2) + 105 + i * 30))

def drawCodeBox():
    pygame.draw.line(window, BLACK, (0, (HEIGHT / 2) + 100), (WIDTH, (HEIGHT / 2) + 100), 5)
    pygame.draw.rect(window, GREEN, run_button)
    run_text = gen2.render("RUN", True, BLACK)
    window.blit(run_text, (run_button.x, run_button.y))

def drawException():
    lines = cur_except.splitlines()
    for i, line in enumerate(lines):
        excep_text = gen3.render(line, True, BLACK)
        window.blit(excep_text, (700, 525 + (i * 30)))

def deleteText():
    global delay, last, user_text
    keys = pygame.key.get_pressed() 
    if active and keys[pygame.K_BACKSPACE]:
        cur_time = pygame.time.get_ticks()
        if cur_time - last >= delay:
            if user_text:
                user_text = user_text[:-1]  
            last = cur_time
            user_text = user_text[:-1] 

def draw_window(pxs, pys):
    window.fill(WHITE)
    draw_grid()
    drawCodeBox()
    drawText()
    drawException()
    pygame.draw.polygon(window, GRAY, [[pxs[i], pys[i]] for i in range(3)])
    pygame.display.update()

class RobotActions:
    def __init__(self, robot):
        self.robot = robot
        self.dire = "right"
    def MOVE_FORWARD(self):
        if self.dire == "right":
            self.robot.x1 += 50
            self.robot.x2 += 50
            self.robot.x3 += 50
        elif self.dire == "down":
            self.robot.y1 += 50
            self.robot.y2 += 50
            self.robot.y3 += 50
        elif self.dire == "up":
            self.robot.y1 -= 50
            self.robot.y2 -= 50
            self.robot.y3 -= 50
        else:
            self.robot.x1 -= 50
            self.robot.x2 -= 50
            self.robot.x3 -= 50
        draw_window(robot.getXpos(), robot.getYpos())
        time.sleep(1)

    def ROTATE_LEFT(self):
        if self.dire == "right":
            self.robot.y1 += 50
            self.robot.x2 += 50
            self.robot.x3 -= 25
            self.robot.y3 -= 25
            self.dire = "up"
        elif self.dire == "down":
            self.robot.x1 -= 50
            self.robot.y2 += 50
            self.robot.x3 += 25
            self.robot.y3 -= 25
            self.dire = "right"
        elif self.dire == "up":
            self.robot.x1 += 50
            self.robot.y2 -= 50
            self.robot.x3 -= 25
            self.robot.y3 += 25
            self.dire = "left"
        else:
            self.robot.y1 -= 50
            self.robot.x2 -= 50
            self.robot.x3 += 25
            self.robot.y3 += 25
            self.dire = "down"
        draw_window(robot.getXpos(), robot.getYpos())
        time.sleep(1)

    def ROTATE_RIGHT(self):
        if self.dire == "right":
            self.robot.x1 += 50
            self.robot.y2 -= 50
            self.robot.x3 -= 25
            self.robot.y3 += 25
            self.dire = "down"
        elif self.dire == "down":
            self.robot.y1 += 50
            self.robot.x2 += 50
            self.robot.x3 -= 25
            self.robot.y3 -= 25
            self.dire = "left"
        elif self.dire == "up":
            self.robot.y1 -= 50
            self.robot.x2 -= 50
            self.robot.x3 += 25
            self.robot.y3 += 25
            self.dire = "right"
        else:
            self.robot.x1 -= 50
            self.robot.y2 += 50
            self.robot.x3 += 25
            self.robot.y3 -= 25
            self.dire = "up"
        draw_window(robot.getXpos(), robot.getYpos())
        time.sleep(1)
    def ok(self, *args):
        for arg in args:
            x, y = arg[0], arg[1]
            if (not ((0 <= x <= WIDTH))) or (not (0 <= y <= ((HEIGHT / 2) + 100))):
                return False
        return True
    def CAN_MOVE(self, direc):
        t1, t2, t3, t4, t5, t6 = self.robot.x1, self.robot.y1, self.robot.x2, self.robot.y2, self.robot.x3, self.robot.y3
        if direc == "forward":
            if self.ok([t1, t2 + 50], [t3, t4 + 50], [t5, t6 + 50]):
                return True
            return False
        elif direc == "backward":
            if self.ok([t1, t2 - 50], [t3, t4 - 50], [t5, t6 - 50]):
                return True
            return False
        elif direc == "left":
            if self.ok([t1 - 50, t2], [t3 - 50, t4], [t5 - 50, t6]):
                return True
            return False
        else:
            if self.ok([t1 + 50, t2], [t3 + 50, t4], [t5 + 50, t6]):
                return True
            return False
        
def main():
    global user_text, active, cur_except, robot
    clock = pygame.time.Clock()
    clock.tick(FPS)
    run = True  
    actions = RobotActions(robot)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False
                if run_button.collidepoint(event.pos):
                    try:
                        time.sleep(0.5)
                        user_text_with_actions = user_text.replace("MOVE_FORWARD()", "actions.MOVE_FORWARD()") \
                                                           .replace("ROTATE_LEFT()", "actions.ROTATE_LEFT()") \
                                                           .replace("ROTATE_RIGHT()", "actions.ROTATE_RIGHT()") \
                                                           .replace("CAN_MOVE(", "actions.CAN_MOVE(")
                        exec(user_text_with_actions, globals(), locals())
                        cur_except = ""
                    except Exception as e:
                        cnt = 0
                        new = []
                        for i in range(len(str(e))):
                            if cnt == 50:
                                cnt = 0
                                new.append("\n")
                            new.append(str(e)[i])
                            cnt += 1
                        cur_except = "".join(new)
                    finally:
                        robot.x1 = 0
                        robot.x2 = 0
                        robot.x3 = 50
                        robot.y1 = 0
                        robot.y2 = 50
                        robot.y3 = 25
                        actions.dire = "right"
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        user_text += "\n"
                    elif event.key == pygame.K_TAB:
                        user_text += "   "
                    else:
                        user_text += event.unicode
        deleteText()
        draw_window(robot.getXpos(), robot.getYpos())
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
