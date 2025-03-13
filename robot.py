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
VALID_KEYS = (
    pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, 
    pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, 
    pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, 
    pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, 
    pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, 
    pygame.K_y, pygame.K_z, 
    pygame.K_SPACE, pygame.K_PERIOD, pygame.K_COMMA, pygame.K_MINUS, pygame.K_EQUALS,
    pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET, pygame.K_SEMICOLON, pygame.K_QUOTE,
    pygame.K_BACKQUOTE, pygame.K_SLASH, pygame.K_BACKSLASH
)

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
last_enter_pos = []
squaresSelected = [[False] * 24 for _ in range(10)]

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
            if self.check_collision([xs[0] + 50, ys[0]], [xs[1] + 50, ys[1]], [xs[2] + 50, ys[2]]):
                self.robot.x1 += 50
                self.robot.x2 += 50
                self.robot.x3 += 50
            else:
                cur_except = "robot will go out of bounds :("
        elif self.dire == "left":
            xs = (self.robot.x1, self.robot.x2, self.robot.x3)
            ys = (self.robot.y1, self.robot.y2, self.robot.y3)
            if self.check_collision([xs[0] - 50, ys[0]], [xs[1] - 50, ys[1]], [xs[2] - 50, ys[2]]):
                self.robot.x1 -= 50
                self.robot.x2 -= 50
                self.robot.x3 -= 50
            else:
                cur_except = "robot will go out of bounds :("
        elif self.dire == "up":
            xs = (self.robot.x1, self.robot.x2, self.robot.x3)
            ys = (self.robot.y1, self.robot.y2, self.robot.y3)
            if self.check_collision([xs[0], ys[0] - 50], [xs[1], ys[1] - 50], [xs[2], ys[2] - 50]):
                self.robot.y1 -= 50
                self.robot.y2 -= 50
                self.robot.y3 -= 50
            else:
                cur_except = "robot will go out of bounds :("
        else:
            xs = (self.robot.x1, self.robot.x2, self.robot.x3)
            ys = (self.robot.y1, self.robot.y2, self.robot.y3)
            if self.check_collision([xs[0], ys[0] + 50], [xs[1], ys[1] + 50], [xs[2], ys[2] + 50]):
                self.robot.y1 += 50
                self.robot.y2 += 50
                self.robot.y3 += 50
            else:
                cur_except = "robot will go out of bounds :("
        draw_window(robot.getXpos(), robot.getYpos())
        if cur_except != "robot will go out of bounds :(":
            time.sleep(0.25)

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
            time.sleep(0.25)

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
            time.sleep(0.25)

    def check_collision(self, *args):
        wall_hits = {}
        for arg in args:
            x, y = arg[0], arg[1]
            if not ((0 <= x <= WIDTH) & (0 <= y <= ((HEIGHT / 2) + 100))):
                return False
            for wall in self.badSquares:
                temp1, temp2 = wall[0], wall[1]
                if (temp1 <= y <= (temp1 + 50)) and (temp2 <= x <= (temp2 + 50)):
                    wall_hits[wall] = 1 + wall_hits.get(wall, 0)
        if wall_hits.values() and len(args) == max(wall_hits.values()):
            return False
        return True
    
    def CAN_MOVE(self, direc):
        global cur_except
        x1, y1, x2, y2, x3, y3 = self.robot.x1, self.robot.y1, self.robot.x2, self.robot.y2, self.robot.x3, self.robot.y3
        if self.dire == "left":
            if direc == "left" and self.check_collision([x1, y1 + 50], [x2, y2 + 50], [x3, y3 + 50]):
                return True
            elif direc == "right" and self.check_collision([x1, y1 - 50], [x2, y2 - 50], [x3, y3 - 50]):
                return True
            elif direc == "forward" and self.check_collision([x1 - 50, y1], [x2 - 50, y2], [x3 - 50, y3]):
                return True
            elif direc == "backward" and self.check_collision([x1 + 50, y1], [x2 + 50, y2], [x3 + 50, y3]):
                return True
        elif self.dire == "right":
            if direc == "left" and self.check_collision([x1, y1 - 50], [x2, y2 - 50], [x3, y3 - 50]):
                return True
            elif direc == "right" and self.check_collision([x1, y1 + 50], [x2, y2 + 50], [x3, y3 + 50]):
                return True
            elif direc == "forward" and self.check_collision([x1 + 50, y1], [x2 + 50, y2], [x3 + 50, y3]):
                return True
            elif direc == "backward" and self.check_collision([x1 - 50, y1], [x2 - 50, y2], [x3 - 50, y3]):
                return True
        elif self.dire == "up":
            if direc == "left" and self.check_collision([x1 - 50, y1], [x2 - 50, y2], [x3 - 50, y3]):
                return True
            elif direc == "right" and self.check_collision([x1 + 50, y1], [x2 + 50, y2], [x3 + 50, y3]):
                return True
            elif direc == "forward" and self.check_collision([x1, y1 - 50], [x2, y2 - 50], [x3, y3 - 50]):
                return True
            elif direc == "backward" and self.check_collision([x1, y1 + 50], [x2, y2 + 50], [x3, y3 + 50]):
                return True
        else:
            if direc == "left" and self.check_collision([x1 + 50, y1], [x2 + 50, y2], [x3 + 50, y3]):
                return True
            elif direc == "right" and self.check_collision([x1 - 50, y1], [x2 - 50, y2], [x3 - 50, y3]):
                return True
            elif direc == "forward" and self.check_collision([x1, y1 + 50], [x2, y2 + 50], [x3, y3 + 50]):
                return True
            elif direc == "backward" and self.check_collision([x1, y1 - 50], [x2, y2 - 50], [x3, y3 - 50]):
                return True
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
    #only shows the text currently on screen
    lines = lines[pointer:]
    for i, line in enumerate(lines):
        #goes through each line of the user_text and prints them out on separate lines
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
    global delayBackspace, lastBackspace, user_text, last_mouse_pos, last_enter_pos
    keys = pygame.key.get_pressed() 
    if active and keys[pygame.K_BACKSPACE]:
        cur_time = pygame.time.get_ticks()
        if cur_time - lastBackspace >= delayBackspace:
            lastBackspace = cur_time
            if user_text and user_text[-1] == "\n":
                last_mouse_pos = last_enter_pos[-1]
                last_enter_pos.pop()
            user_text = user_text[:-1]             
            if last_mouse_pos != (None, None):
                #it can't go further left and the y-position is always the same
                last_mouse_pos = (max(10, last_mouse_pos[0] - 14), last_mouse_pos[1])
            
def mouseFlicker(pos):
    global delayMouse, lastMouse, cursorAvailable
    if pos == (None, None):
        return
    cur_time = pygame.time.get_ticks()
    if cur_time - lastMouse >= delayMouse:
        #makes flickering effect
            #if cursor is on, it becomes off, vice versa
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
    global user_text, active, cur_except, robot, last_mouse_pos, actions, pointer, last_enter_pos
    clock = pygame.time.Clock()
    clock.tick(FPS)
    run = True  
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 4:
                    if active:
                        pointer = max(0, pointer - 1)
                elif event.button == 5:
                    if active:
                        pointer += 1
                elif event.button == 1:
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
                            time.sleep(0.25)
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
                            #resets the robot position and direction
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
                            last_enter_pos.append(last_mouse_pos)
                            #changes the y position by 30 pixels
                            last_mouse_pos = (10, last_mouse_pos[1] + 30)
                        user_text += "\n"
                    elif event.key == pygame.K_TAB:
                        if last_mouse_pos != (None, None):
                            #42 for 14 pixels per space
                            last_mouse_pos = (last_mouse_pos[0] + 42, last_mouse_pos[1])
                        user_text += "   "
                    elif event.key in VALID_KEYS:
                        if last_mouse_pos != (None, None):
                            last_mouse_pos = (last_mouse_pos[0] + 14, last_mouse_pos[1])
                        user_text += event.unicode
        draw_window(robot.getXpos(), robot.getYpos())
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
