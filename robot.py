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
MALICIOUS = ["import", "os", "open", "exec", "eval"]

#colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)

#sfx

#simulator variables
user_text = ""
input_rect = pygame.Rect(0, (HEIGHT / 2) + 100, WIDTH, (HEIGHT - ((HEIGHT / 2) + 100)))
run_button = pygame.Rect(WIDTH / 2 - 110, (HEIGHT / 2) + 100, 220, 45)
active = False
lastBackspace = pygame.time.get_ticks()
lastMouse = pygame.time.get_ticks()
delayBackspace = 75
delayMouse = 500
cursorAvailable = False
cur_except = ""
pointer = 0
last_mouse_pos = (None, None)
squaresSelected = [[False] * 24 for i in range(10)]

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
    
class RobotActions:
    def __init__(self, robot):
        self.robot = robot
        self.dire = "right"
        self.badSquares = set()
    def MOVE_FORWARD(self):
        global cur_except
        if self.dire == "right":
            xs = (self.robot.x1, self.robot.x2, self.robot.x3)
            ys = (self.robot.y1, self.robot.y2, self.robot.y3)
            if self.ok([xs[0] + 50, ys[0]], [xs[1] + 50, ys[1]], [xs[2] + 50, ys[2]]):
                self.robot.x1 += 50
                self.robot.x2 += 50
                self.robot.x3 += 50
            else:
                cur_except = "robot will go out of bounds :("
        elif self.dire == "left":
            xs = (self.robot.x1, self.robot.x2, self.robot.x3)
            ys = (self.robot.y1, self.robot.y2, self.robot.y3)
            if self.ok([xs[0] - 50, ys[0]], [xs[1] - 50, ys[1]], [xs[2] - 50, ys[2]]):
                self.robot.x1 -= 50
                self.robot.x2 -= 50
                self.robot.x3 -= 50
            else:
                cur_except = "robot will go out of bounds :("
        elif self.dire == "up":
            xs = (self.robot.x1, self.robot.x2, self.robot.x3)
            ys = (self.robot.y1, self.robot.y2, self.robot.y3)
            if self.ok([xs[0], ys[0] - 50], [xs[1], ys[1] - 50], [xs[2], ys[2] - 50]):
                self.robot.y1 -= 50
                self.robot.y2 -= 50
                self.robot.y3 -= 50
            else:
                cur_except = "robot will go out of bounds :("
        else:
            xs = (self.robot.x1, self.robot.x2, self.robot.x3)
            ys = (self.robot.y1, self.robot.y2, self.robot.y3)
            if self.ok([xs[0], ys[0] + 50], [xs[1], ys[1] + 50], [xs[2], ys[2] + 50]):
                self.robot.y1 += 50
                self.robot.y2 += 50
                self.robot.y3 += 50
            else:
                cur_except = "robot will go out of bounds :("
        draw_window(robot.getXpos(), robot.getYpos())
        if cur_except != "robot will go out of bounds :(":
            time.sleep(0.5)

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
        if cur_except != "robot will go out of bounds :(":
            draw_window(robot.getXpos(), robot.getYpos())
            time.sleep(0.5)

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
        if cur_except != "robot will go out of bounds :(":
            draw_window(robot.getXpos(), robot.getYpos())
            time.sleep(0.5)

    def ok(self, *args):
        hitMap = {}
        for arg in args:
            x, y = arg[0], arg[1]
            if not ((0 <= x <= WIDTH) & (0 <= y <= ((HEIGHT / 2) + 100))):
                return False
            for bad in self.badSquares:
                temp1, temp2 = bad[0], bad[1]
                if (temp1 <= y <= (temp1 + 50)) and (temp2 <= x <= (temp2 + 50)):
                    hitMap[bad] = 1 + hitMap.get(bad, 0)
                    break
        if len(args) == max(hitMap.values()):
            return False
        return True
    
    def CAN_MOVE(self, direc):
        global cur_except
        t1, t2, t3, t4, t5, t6 = self.robot.x1, self.robot.y1, self.robot.x2, self.robot.y2, self.robot.x3, self.robot.y3
        if direc == "forward":
            if self.ok([t1, t2 + 50], [t3, t4 + 50], [t5, t6 + 50]):
                return True
        elif direc == "backward":
            if self.ok([t1, t2 - 50], [t3, t4 - 50], [t5, t6 - 50]):
                return True
        elif direc == "left":
            if self.ok([t1 - 50, t2], [t3 - 50, t4], [t5 - 50, t6]):
                return True
        else:
            if self.ok([t1 + 50, t2], [t3 + 50, t4], [t5 + 50, t6]):
                return True
        cur_except = "robot will go out of bounds :("
        return False

#player variables
robot = Player(0, 0, 0, 50, 50, 25)    
actions = RobotActions(robot)

#window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyBot Simulator")

def draw_grid():
    for x in range(0, WIDTH, 50):
        for y in range(0, (HEIGHT // 2) + 100, 50):
            rect = pygame.Rect(x, y, 50, 50)
            newx, newy = x // 50, y // 50
            #flip x and y because y is the row index while x is the column index
            if squaresSelected[newy][newx]:
                pygame.draw.rect(window, BLACK, rect)
            else:
                pygame.draw.rect(window, WHITE, rect)
            border_rect = rect.inflate(5, 5)  
            pygame.draw.rect(window, BLACK, border_rect, 4) 
            
def drawText():
    lines = user_text.splitlines()
    lines = lines[pointer:]
    for i, line in enumerate(lines):
        code = gen.render(line, True, BLACK) 
        window.blit(code, (10, (HEIGHT / 2) + 105 + i * 30))

def drawCodeBox():
    pygame.draw.line(window, BLACK, (0, (HEIGHT / 2) + 100), (WIDTH, (HEIGHT / 2) + 100), 5)
    pygame.draw.rect(window, PURPLE, input_rect)
    pygame.draw.rect(window, GREEN, run_button)
    run_text = gen2.render("Run Code", True, BLACK)
    window.blit(run_text, (run_button.x, run_button.y))

def drawException():
    lines = cur_except.splitlines()
    for i, line in enumerate(lines):
        excep_text = gen3.render(line, True, WHITE)
        window.blit(excep_text, (735, 525 + (i * 30)))

def deleteText():
    global delayBackspace, lastBackspace, user_text, last_mouse_pos
    keys = pygame.key.get_pressed() 
    if active and keys[pygame.K_BACKSPACE]:
        cur_time = pygame.time.get_ticks()
        if cur_time - lastBackspace >= delayBackspace:
            lastBackspace = cur_time
            user_text = user_text[:-1]             
            if last_mouse_pos != (None, None):
                last_mouse_pos = (max(10, last_mouse_pos[0] - 14), last_mouse_pos[1])
            
def mouseFlicker(pos):
    global delayMouse, lastMouse, cursorAvailable
    if pos == (None, None):
        return
    cur_time = pygame.time.get_ticks()
    if cur_time - lastMouse >= delayMouse:
        cursorAvailable = not cursorAvailable
        lastMouse = cur_time  
    if cursorAvailable:
        pygame.draw.line(window, BLACK, (pos[0], pos[1] - 10), (pos[0], pos[1] + 10), 2)

def selectSquare(posx, posy):
    diff1 = posx % 50
    diff2 = posy % 50
    posx -= diff1
    posy -= diff2
    posx //= 50
    posy //= 50
    #flip x and y because y is the row index while x is the column index
    if squaresSelected[posy][posx] == True:
        actions.badSquares.discard((posy * 50, posx * 50))
        squaresSelected[posy][posx] = not squaresSelected[posy][posx]
    else:
        actions.badSquares.add((posy * 50, posx * 50))
        squaresSelected[posy][posx] = not squaresSelected[posy][posx]

def draw_window(pxs, pys):
    window.fill(WHITE)
    draw_grid()
    drawCodeBox()
    drawText()
    deleteText()
    drawException()
    mouseFlicker(last_mouse_pos)
    pygame.draw.polygon(window, GRAY, [[pxs[i], pys[i]] for i in range(3)])
    pygame.display.update()
        
def main():
    global user_text, active, cur_except, robot, last_mouse_pos, actions, pointer
    clock = pygame.time.Clock()
    clock.tick(FPS)
    run = True  
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if active and event.button == 4:
                    pointer = max(0, pointer - 1)
                elif active and event.button == 5:
                    pointer += 1
                if input_rect.collidepoint(event.pos): 
                    last_mouse_pos = pygame.mouse.get_pos()
                    active = True
                else: 
                    selectSquare(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    last_mouse_pos = (None, None)
                    active = False
                if run_button.collidepoint(event.pos):
                    cur_except = ""
                    try:
                        time.sleep(0.5)
                        for bad in MALICIOUS:
                            if bad in user_text:
                                raise Exception
                        else:
                            user_text_with_actions = user_text.replace("MOVE_FORWARD()", "actions.MOVE_FORWARD()") \
                                                            .replace("ROTATE_LEFT()", "actions.ROTATE_LEFT()") \
                                                            .replace("ROTATE_RIGHT()", "actions.ROTATE_RIGHT()") \
                                                            .replace("CAN_MOVE(", "actions.CAN_MOVE(")
                            exec(user_text_with_actions, globals(), locals())
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
                        #when the user types in something malicious
                        if not cur_except:
                            cur_except = "program no like malicious code :("
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
                        if last_mouse_pos != (None, None):
                            last_mouse_pos = (10, last_mouse_pos[1] + 30)
                        user_text += "\n"
                    elif event.key == pygame.K_TAB:
                        if last_mouse_pos != (None, None):
                            last_mouse_pos = (last_mouse_pos[0] + 42, last_mouse_pos[1])
                        user_text += "   "
                    elif event.key not in [pygame.K_BACKSPACE, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_CAPSLOCK]:
                        if last_mouse_pos != (None, None):
                            last_mouse_pos = (last_mouse_pos[0] + 14, last_mouse_pos[1])
                        user_text += event.unicode
        draw_window(robot.getXpos(), robot.getYpos())
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
