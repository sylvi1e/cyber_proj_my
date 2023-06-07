import pygame
import math
POINTS=[]
LINE=[]
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self,other):
        return math.sqrt((self.x-other.x)(self.x-other.x)+(self.y-other.y)(self.y-other.y))
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __str__(self):
        return "(x: "+str(self.x)+" ,y: "+str(self.y)+")"
def is_in(p,l):
    for i in p:
        if l==i:
            return True
    return False
def writeline(point0,point1):
    l=[]
    if point0 == point1:
        return [point0]
    try:
        m=(point0.y-point1.y)/(point0.x-point1.x)
    except ZeroDivisionError:
        if point0.y<point1.y:
            l.append(point0)
            for i in range(point0.y + 1, point1.y):
                l.append(Point(point0.x, i))
            l.append(point1)
            return l
        else:
            l.append(point1)
            for i in range(point1.y + 1, point0.y):
                l.append(Point(point0.x, i))
            l.append(point0)
            return l

    '''y-y1=m(x-x1)'''
    '''"y=mx+y1-mx1"'''
    '''x*m+y1-m*x1'''
    if abs(point0.x-point1.x)>=abs(point0.y-point1.y):
        l.append(point0)
        for i in range(int(min(point0.x,point1.x))+1,int(max(point0.x,point1.x))):
            l.append(Point(i,int(i*m+point0.y-m*point0.x)))
        l.append(point1)
    else:
        '''y-y1=m(x-x1)'''
        '''"y/m-y1/m+x1=x"'''
        '''y/m-y1/m+x1'''
        l.append(point0)
        for i in range(int(min(point0.y,point1.y))+1,int(max(point0.y,point1.y))):
            l.append(Point(int(i/m-point0.y/m+point0.x), i))
        l.append(point1)
    return l
def draw():
    pygame.init()
    screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF)
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    run = True
    draw = False
    while run:
        if draw:
            x1, y1 = pygame.mouse.get_pos()
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x1, y1))
            po = writeline(Point(x, y), Point(x1, y1))
            for i in po:
                if not is_in(LINE, i):
                    # print(i,end=", ")
                    LINE.append(i)
            x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = not True
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                if not draw:
                    LINE = []
                    POINTS = []
                    screen.fill((255, 255, 255))
                    draw = True
                else:
                    draw = False
                    for i in LINE:
                        if not is_in(POINTS, i):
                            POINTS.append(i)

                x, y = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                draw = False
                LINE = []
                POINTS = []
                screen.fill((255, 255, 255))
        pygame.display.flip()
        clock.tick(120)
    pygame.quit()
    return [[i.x,i.y] for i in POINTS]
def show(Points):
    pygame.init()
    screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF)

    clock = pygame.time.Clock()
    run = True
    screen.fill((255, 255, 255))
    for i in Points:
        pygame.draw.line(screen, (0, 0, 0), (i[0], i[1]), (i[0], i[1]))
    pygame.display.flip()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = not True
        clock.tick(120)
    pygame.quit()
