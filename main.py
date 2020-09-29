import pygame
pygame.init()
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH , WIDTH + 160))
pygame.display.set_caption("Path-Finding-Visualizer")

RED = (255, 0, 0)
REDi = (52, 152, 219)
GREEN = (0, 255, 0)
GREENi = (88, 214, 141)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
YELLOWj = (244, 218, 63)
YELLOWi = (165, 105, 189)
WHITE = (255, 255, 255)
GREYi = (240, 240, 240)
BLACK = (0, 0, 0)
CYAN = (0, 255, 150)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot():
    def __init__(self,row,col,width,total_row):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = GREYi
        self.neighbour = []
        self.width = width
        self.total_row = total_row
    
    def get_pos(self):
        return self.row, self.col

    def isClosed(self):
        return self.color == RED
    
    def isOpen(self):
        return self.color == GREEN
    
    def isBarrier(self):
        return self.color == BLACK

    def isStart(self):
        return self.color == ORANGE

    def isEnd(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def makeClosed(self):
        self.color = RED
    
    def makeOpen(self):
        self.color = GREEN

    def makeBarrier(self):
        self.color = BLACK

    def makeStart(self):
        self.color = ORANGE

    def makeEnd(self):
        self.color =  TURQUOISE

    def makePath(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win , self.color , (self.x , self.y , self.width , self.width) )

    def updateNeighbour(self, grid):
        self.neighbour = []
        if self.row < self.total_row-1 and not grid[self.row+1][self.col-10].isBarrier():
            self.neighbour.append(grid[self.row+1][self.col-10])

        if self.col-10 > 0 and not grid[self.row][self.col-1-10].isBarrier():
            self.neighbour.append(grid[self.row][self.col-1-10])     

        if self.row > 0 and not grid[self.row-1][self.col-10].isBarrier():
            self.neighbour.append(grid[self.row-1][self.col-10])

        if self.col-10 < self.total_row-1 and not grid[self.row][self.col+1-10].isBarrier():
            self.neighbour.append(grid[self.row][self.col+1-10])

    def __lt__(self, other):
        return False

class button():
    def __init__(self , x, y, length , breath , click , text = '', index = 1):
        self.x = x
        self.y = y
        self.length = length
        self.breath = breath
        self.click = click
        self.color = CYAN
        self.text = text
        self.index = index
        if index == 1:
            self.color = REDi
        elif index == 6:
            self.color = YELLOWj
        elif index == 7:
            self.color = YELLOWi

    def draw(self , win):
        pygame.draw.rect(win , self.color , (self.x , self.y , self.length , self.breath))
        if self.index < 6 :
            if self.text != '':
                font = pygame.font.SysFont('arial',30 )
                text = font.render(self.text, 1, (0,0,0))
                win.blit(text, (self.x + 10, self.y +5))
        else:
            if self.text != '':
                font = pygame.font.SysFont('georgia',45 , 1)
                text = font.render(self.text, 1, (255,255,255))
                win.blit(text, (self.x + 10, self.y))

def h(p1,p2):
    x1 , y1 = p1
    x2 , y2 = p2
    return abs(x1-x2) + abs (y1-y2)

def reconstruct_path(cameFrom , current , draw):
    while current in cameFrom:
        current = cameFrom[current]
        current.makePath()
        #print(current.x)
        draw()


def algorithm(draw , grid , start , end):
    #print('herw in 1')
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count , start))
    cameFrom = {}
    gScore = {spot : float("inf") for row in grid for spot in row}
    gScore[start] = 0
    fScore = {spot : float("inf") for row in grid for spot in row}
    fScore[start] = h(start.get_pos() , end.get_pos())

    openSetHash = {start}
    
    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == end:
            reconstruct_path(cameFrom , end , draw)
            start.makeStart()
            end.makeEnd()
            return True
        
        for neighbor in current.neighbour:
            tempGScore = gScore[current] + 1

            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + h(neighbor.get_pos(),end.get_pos())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbor] , count , neighbor))
                    openSetHash.add(neighbor)
                    neighbor.makeOpen()
        draw()
        if current != start:
            current.makeClosed()
    return False

def greedy_dfs(draw , grid , start , end):
    #print('herw in 1')
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count , start))
    cameFrom = {}
    fScore = {spot : float("inf") for row in grid for spot in row}
    fScore[start] = h(start.get_pos() , end.get_pos())

    openSetHash = {start}
    
    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = openSet.get()[2]

        if current == end:
            reconstruct_path(cameFrom , end , draw)
            start.makeStart()
            end.makeEnd()
            return True
        
        for neighbor in current.neighbour:
            
            fScore[neighbor] = h(neighbor.get_pos(),end.get_pos())
            if neighbor not in openSetHash:
                count += 1
                openSet.put((fScore[neighbor] , count , neighbor))
                openSetHash.add(neighbor)
                cameFrom[neighbor] = current
                neighbor.makeOpen()
        draw()
        if current != start:
            current.makeClosed()
    return False

def algodikshitras(draw , grid , start , end):
    print('herw in 2')
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count , start))
    cameFrom = {}
    gScore = {spot : float("inf") for row in grid for spot in row}
    gScore[start] = 0

    openSetHash = {start}
    
    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == end:
            reconstruct_path(cameFrom , end , draw)
            start.makeStart()
            end.makeEnd()
            return True
        
        for neighbor in current.neighbour:
            tempGScore = gScore[current] + 1

            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGScore
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((gScore[neighbor] , count , neighbor))
                    openSetHash.add(neighbor)
                    neighbor.makeOpen()
        draw()
        if current != start:
            current.makeClosed()
    return False

def dfs(draw , grid , start , end):
    openset = []
    openset.append(start)
    cameFrom  = {}
    openSetHash = {start}

    while len(openset) != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = openset.pop()
        #openSetHash.remove(current)
        openSetHash.add(current)

        if current == end:
            reconstruct_path(cameFrom , end , draw)
            start.makeStart()
            end.makeEnd()
            return True

        for neighbor in current.neighbour:
            if neighbor not in openSetHash:
                openset.append(neighbor)
                #openSetHash.add(neighbor)
                cameFrom[neighbor] = current
        current.makeOpen()
        draw()
        if current != start:
            current.makeClosed()
    return False

def makeGrid(rows , width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j + 10 , gap , rows)
            grid[i].append(spot)
    return grid

def drawGrid(win , rows , width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win , GREY , (0 , i*gap + 160) , (width , i*gap + 160))
        for j in range(rows):
               pygame.draw.line(win , GREY , (j*gap , 160) , ( j*gap , width + 160))

def draw(win , grid , rows , width):
   
    for row in grid:
        for spot in row:
            spot.draw(win)

    drawGrid(win , rows , width)
    pygame.display.update()

def drawbutt(win , butt):
    win.fill(WHITE)
    for bb in butt:
        bb.draw(win)

    pygame.display.update()

def drawnewbutt(win , butt):
    for bb in butt:
        bb.draw(win)

    pygame.display.update()

def getClickedPos(pos , rows , width):
    gap = width // rows
    y, x = pos
    x = x - 160
    row = y // gap
    col = x // gap 
    return row , col

def checkover(pos, x , y , length , breath):
    if pos[0] > x and pos[0] < x + length:
        if pos[1] > y and pos[1] < y + breath:
            return True
            
    return False

def isover(win,pos,butt,index):
    for i in butt:
        check = checkover(pos , i.x , i.y , i.length , i.breath)
        if check == True:
            for j in butt:
                j.color = CYAN
            i.color = REDi
            index = i.index
            
    drawnewbutt(win,butt)
    return index

def isoverStartReset(win,pos,butt,index):
    check = False
    for i in butt:
        check = checkover(pos , i.x , i.y , i.length , i.breath)
        if check == True:
            index = i.index
    return index


def makebutton():
    butt = []
    but = button(50 , 80 , 100 , 50 , False , 'A* Algo' , 1)
    butt.append(but)
    but = button(170 , 80 , 130 , 50 , False , 'Dijkstra' ,2)
    butt.append(but)
    but = button(320 , 80 , 120 , 50 , False , 'BFS' ,3)
    butt.append(but)
    but = button(80 , 20 , 120 , 50 , False , 'DFS' ,4)
    butt.append(but)
    but = button(220 , 20 , 160 , 50 , False , 'Greedy BFS' ,5)
    butt.append(but) 
    return butt

def makestartResetButt():
    butt = []
    but = button(500 , 10 , 200 , 60 , False , 'START' , 6)
    butt.append(but)
    but = button(500 , 80 , 180 , 60 , False , 'RESET' ,7)
    butt.append(but)
    return butt

def main(win, width):
    rows = 50
    grid = makeGrid(rows , width)
    butt = makebutton()
    startReset = makestartResetButt()
   
    start = None
    end = None

    run = True
    index = 1
    isit = -1
    drawbutt(win,butt)
    startReset[0].draw(win)
    startReset[1].draw(win)
    pygame.display.update()

    while run:
        draw(win , grid , rows , width)
       
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False   
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                index = isover(win,pos,butt,index)
                
                isit = isoverStartReset(win,pos,startReset,-1)
                #print(index)
                #print(isit)
                row , col = getClickedPos(pos , rows , width)
                spot = grid[row][col]
                if pos[1]>160 :
                    if not start and spot != end:
                        start = spot
                        start.makeStart()

                    elif not end and spot != start:
                        end = spot
                        end.makeEnd()

                    elif spot != end and spot != start:
                        spot.makeBarrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row , col = getClickedPos(pos , rows , width)
                spot = grid[row][col]
                spot.reset()
                if(spot == start):
                    start = None
                elif(spot == end):
                    end = None

            
            if isit == 6 and start and end:
                isit = -1
                for row in grid:
                    for spot in row:
                        spot.updateNeighbour(grid)
                #print(index)
                if index == 1:
                    algorithm(lambda:  draw(win , grid , rows , width), grid , start ,end )
                elif index == 2:
                    algodikshitras(lambda:  draw(win , grid , rows , width), grid , start ,end )
                elif index == 3:
                    algodikshitras(lambda:  draw(win , grid , rows , width), grid , start ,end )
                elif index == 4:
                    dfs(lambda : draw(win , grid , rows , width), grid , start ,end )
                elif index == 5:
                    greedy_dfs(lambda : draw(win , grid , rows , width), grid , start ,end )

            if isit == 7:
                isit = -1
                start = None
                end = None
                grid = makeGrid(rows , width)

    pygame.quit()

main(WIN , WIDTH)