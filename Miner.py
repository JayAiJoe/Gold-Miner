import pygame
import sys
import random


# colors
PIT = (0, 0, 0)
BEACON = (0, 0, 255)
MINER = (0, 255, 0)
GOLD = (212,175,55)
GROUND = (211,211,211)

# display constants
WIDTH = 30
HEIGHT = 30
MARGIN = 5
GRID_SIZE = 8
WINDOW_WIDTH = 852
WINDOW_HEIGHT = 480
WINDOW_SIZE = [WINDOW_WIDTH,WINDOW_HEIGHT]

# codes
ground = 0
pit = 2
beacon = 3
gold = 4

next_tile = 0
def updateDisplay(grid, gridSize,screen,board):
    # Set the screen background
    screen.fill((0,0,0))
 
    # Draw then update the grid display
    for row in range(gridSize):
        for column in range(gridSize):
            color = GROUND
            if grid[row][column] == 1:
                color = MINER
            elif grid[row][column] == pit:
                color = PIT
            elif grid[row][column] == beacon:
                color = BEACON
            elif grid[row][column] == gold:
                color = GOLD
            pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])

    font = pygame.font.Font('freesansbold.ttf', 20)
    
    # Draw the buttons
    pygame.draw.rect(screen,(255,0,0),[2*WINDOW_WIDTH/3,WINDOW_HEIGHT/2,140,40])
    pygame.draw.rect(screen,(0,255,0),[2*WINDOW_WIDTH/3,WINDOW_HEIGHT/2-50,140,40])
    pygame.draw.rect(screen,(0,255,0),[2*WINDOW_WIDTH/3,WINDOW_HEIGHT/2-100,65,40])
    pygame.draw.rect(screen,GOLD,[2*WINDOW_WIDTH/3+75,WINDOW_HEIGHT/2-100,65,40])
    pygame.draw.rect(screen,BEACON,[2*WINDOW_WIDTH/3,WINDOW_HEIGHT/2-150,140,40])
    screen.blit(font.render('Pits', True, (0,0,0)), (2*WINDOW_WIDTH/3+10,WINDOW_HEIGHT/2-88))
    screen.blit(font.render('Gold', True, (255,255,255)),(2*WINDOW_WIDTH/3 + 85,WINDOW_HEIGHT/2-88))
    screen.blit(font.render('Beacons', True, (255,255,255)),(2*WINDOW_WIDTH/3 + 32,WINDOW_HEIGHT/2-138))
    screen.blit(font.render('Random', True, (0,0,0)),(2*WINDOW_WIDTH/3 + 33,WINDOW_HEIGHT/2- 38))
    screen.blit(font.render('Smart', True, (255,255,255)),(2*WINDOW_WIDTH/3 + 41,WINDOW_HEIGHT/2 + 12))

    # Counters
    screen.blit(font.render("Moves : " + str(board.move_ctr), True, (255,255,255)),(2*WINDOW_WIDTH/3,WINDOW_HEIGHT/2 + 70))
    screen.blit(font.render("Rotations : " + str(board.rotate_ctr), True, (255,255,255)),(2*WINDOW_WIDTH/3,WINDOW_HEIGHT/2 + 120))
    

    clock.tick(60)
    pygame.display.flip()


class Board:
    def __init__(self):
        self.prev_gold = None
        self.beacons = []
        self.move_ctr = 0
        self.rotate_ctr = 0

        
class Beacon:
    def __init__(self,position):
        self.to_gold = 0
        self.pos = position

    def find_gold(self,grid):
        y = self.pos[0]
        x = self.pos[1]
        distance = 0
        while x < GRID_SIZE:
            if grid[y][x] == pit:
                break
            elif grid[y][x] == gold:
                distance = x - self.pos[1]
            x += 1
        y = self.pos[0]
        x = self.pos[1]
        if distance == 0:
            while x >= 0:
                if grid[y][x] == pit:
                    break
                elif grid[y][x] == gold:
                    distance = self.pos[1] - x
                x -= 1
        y = self.pos[0]
        x = self.pos[1]
        if distance == 0:
            while y < GRID_SIZE:
                if grid[y][x] == pit:
                    break
                elif grid[y][x] == gold:
                    distance = y - self.pos[0]
                y += 1
        y = self.pos[0]
        x = self.pos[1]
        if distance == 0:
            while y >= 0:
                if grid[y][x] == pit:
                    break
                elif grid[y][x] == gold:
                    distance = self.pos[0] - y
                y -= 1
        self.to_gold = distance

class Miner():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.front = 1

    #moves the miner forward
    #returns true if move was successful, false otherwise    
    def move(self, board):
        if self.front == 0:
            if self.y > 0:
                self.y -= 1
            else:
                return False
        elif self.front == 1:
            if self.x < 7:
                self.x += 1
            else:
                return False
        elif self.front == 2:
            if self.y < 7:
                self.y += 1
            else:
                return False
        else:
            if self.x > 0:
                self.x -= 1
            else:
                return False
        board.move_ctr += 1
        return True

    #scans block in front of miner
    #returns 0-4 based on type, -1 if edge
    def scan(self,grid):
        if self.front == 0:
            if self.y > 0:
                return grid[self.y-1][self.x]
            else:
                return -1
        elif self.front == 1:
            if self.x < 7:
                return grid[self.y][self.x+1]
            else:
                return -1
        elif self.front == 2:
            if self.y < 7:
                return grid[self.y+1][self.x]
            else:
                return -1
        else:
            if self.x > 0:
                return grid[self.y][self.x-1]
            else:
                return -1            

    #rotate the miner 90 degrees clockwise
    def rotate(self,board):
        board.rotate_ctr += 1
        self.front = (self.front+1)%4
        global next_tile
        if self.front == 0:
            if self.y > 0:
                next_tile = [self.y-1,self.x]
            else:
                next_tile = -1
        elif self.front == 1:
            if self.x < GRID_SIZE-1:
                next_tile = [self.y,self.x+1]
            else:
                next_tile = -1
        elif self.front == 2:
            if self.y < GRID_SIZE-1:
                next_tile = [self.y+1,self.x]
            else:
                next_tile = -1
        else:
            if self.x > 0:
                next_tile = [self.y,self.x-1]
            else:
                next_tile = -1            
        updateDisplay(grid, GRID_SIZE,screen,board)
    #backtrack the miner n moves
    def backtrack(self,board,n):
        board.rotate_ctr += 2
        self.front = (self.front+2)%4
        for i in range(n):
            self.move(board)
            
    def moveto(self,board,coordinate):
        if self.x > coordinate[1]:
            while self.front != 1:
                self.rotate(board)
            while self.x > coordinate[1]:
                self.move(board)
        elif self.x < coordinate[1]:
            while self.front != 3:
                self.rotate(board)
            while self.x < coordinate[1]:
                self.move(board)
        elif self.y > coordinate[0]:
            while self.front != 0:
                self.rotate(board)
            while self.y > coordinate[0]:
                self.move(board)
        elif self.y < coordinate[0]:
            while self.front != 2:
                self.rotate(board)
            while self.y < coordinate[0]:
                self.move(board)


#-------------------MAIN PROGRAM----------------------
# initialize display
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Gold Miner")

# initialize miner, grid and board info
board = Board()
miner = Miner()
place_type = pit
grid = []
for row in range(GRID_SIZE):
    grid.append([])
    for column in range(GRID_SIZE):
        grid[row].append(0)  # Append a cell

# Display buttons
pygame.draw.rect(screen,MINER,[WINDOW_WIDTH/2,WINDOW_HEIGHT/2,140,40])
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

grid[miner.y][miner.x] = 1
updateDisplay(grid, GRID_SIZE,screen,board)
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # random miner
            if 2*WINDOW_WIDTH/3 <= pos[0] <= 2*WINDOW_WIDTH/3 + 140 and WINDOW_HEIGHT/2-40 <= pos[1] <= WINDOW_HEIGHT/2-10:
                #---------------WRITE LOGIC HERE------------------
                # 1/3 rotate, 2/3 move, does not scan ahead so it may fall into a pit
                gameover = False
                while not gameover:
                    turn = random.randint(0,2)
                    if turn == 1:
                        miner.rotate(board)
                    else:
                        next_tile = miner.scan(grid)
                        grid[miner.y][miner.x] = 0
                        miner.move(board)
                        grid[miner.y][miner.x] = 1
                        updateDisplay(grid, GRID_SIZE,screen,board)
                        if next_tile == pit:
                            gameover = True
                            print("Lose")
                        elif next_tile == gold:
                            gameover = True
                            print("Win")
                    pygame.time.delay(250)
                #--------------------------------------------------
            
            # smart miner
            if 2*WINDOW_WIDTH/3 <= pos[0] <= 2*WINDOW_WIDTH/3 + 140 and WINDOW_HEIGHT/2 <= pos[1] <= WINDOW_HEIGHT/2+40:
                #---------------WRITE LOGIC HERE------------------
                #Scans all 4 sides then determines best square to move to, changes behavior once a beacon is activated
                gameover = False
                checked =[]
                coordinates=[]
                while not gameover:
                    beaconF = 0
                    fullscan = True
                    while fullscan: #rotates to find best path
                        bestmove =[0,1,2,3]
                        right_tile = miner.scan(grid)
                        if right_tile == gold:
                            break
                        elif right_tile == pit or right_tile == -1:
                            bestmove.remove(1)
                        miner.rotate(board)
                        down_tile = miner.scan(grid)
                        if down_tile == gold:
                            break
                        elif down_tile == pit or down_tile == -1:
                            bestmove.remove(2)
                        miner.rotate(board)
                        left_tile = miner.scan(grid)
                        if left_tile == gold:
                            break
                        elif left_tile == pit or left_tile == -1:
                            bestmove.remove(3)
                        miner.rotate(board)
                        up_tile = miner.scan(grid)
                        if up_tile == gold:
                            break
                        elif up_tile == pit or up_tile == -1:
                            bestmove.remove(0)
                        miner.rotate(board)
                        
                        if right_tile == beacon:
                            bestmove = 1
                            beaconF = 1
                        elif down_tile == beacon:
                            bestmove = 2
                            beaconF = 1
                        elif left_tile == beacon:
                            bestmove = 3
                            beaconF = 1
                        elif up_tile == beacon:
                            bestmove = 0
                            beaconF = 1
                        fullscan = False
                    try:
                        while miner.front not in bestmove:
                            miner.rotate(board)
                    except TypeError:
                        while miner.front != bestmove:
                            miner.rotate(board)
                    lastpos = [miner.y,miner.x]
                    if next_tile in checked:
                        miner.move(board)
                        while miner.front != 1:
                            miner.rotate(board)
                        grid[lastpos[0]][lastpos[1]] = 2
                        grid[miner.y][miner.x] = 1
                        updateDisplay(grid, GRID_SIZE,screen,board)
                        continue
                    if lastpos not in checked:
                        checked.append(lastpos)
                    miner.move(board)
                    grid[lastpos[0]][lastpos[1]] = 0
                    grid[miner.y][miner.x] = 1
                    updateDisplay(grid, GRID_SIZE,screen,board)
                    while miner.front != 1:
                        miner.rotate(board)
                    if beaconF == 1:
                        for i in range(len(board.beacons)):
                            if board.beacons[i].pos == [miner.y,miner.x]:
                                board.beacons[i].find_gold(grid)
                                beaconMove = board.beacons[i].to_gold
                                break
                        if beaconMove != 0:
                            if miner.y+beaconMove < GRID_SIZE:
                                if [miner.y+beaconMove,miner.x] not in checked:
                                    coordinates.append([miner.y+beaconMove,miner.x])
                            if miner.y-beaconMove >= 0:
                                if [miner.y-beaconMove,miner.x] not in checked:
                                    coordinates.append([miner.y-beaconMove,miner.x])
                            if miner.x+beaconMove < GRID_SIZE:
                                if [miner.y,miner.x+beaconMove] not in checked:
                                    coordinates.append([miner.y,miner.x+beaconMove])
                            if miner.x-beaconMove >= 0:
                                if [miner.y,miner.x-beaconMove] not in checked:
                                    coordinates.append([miner.y,miner.x-beaconMove])
                            while [miner.y,miner.x] != prev_gold:
                                print(coordinates)
                                for j in coordinates:
                                    print(j)
                                    coordinate = j
                                    gonext =0 
                                    moves = 0
                                    if miner.x < coordinate[1]: #to the right
                                        while miner.front != 1:
                                            miner.rotate(board)
                                        while miner.x < coordinate[1]:
                                            lastpos = [miner.y,miner.x]
                                            if miner.scan(grid) == pit:
                                                board.rotate_ctr += 2
                                                miner.front = (miner.front+2)%4
                                                for k in range(moves):
                                                    print(moves)
                                                    miner.move(board)
                                                    grid[lastpos[0]][lastpos[1]] = 0
                                                    grid[miner.y][miner.x] = 1
                                                    updateDisplay(grid, GRID_SIZE,screen,board)
                                                gonext = 1
                                                break
                                            miner.move(board)
                                            moves +=1
                                            grid[lastpos[0]][lastpos[1]] = 0
                                            grid[board.beacons[i].pos[0]][board.beacons[i].pos[1]] = 3
                                            grid[miner.y][miner.x] = 1
                                            updateDisplay(grid, GRID_SIZE,screen,board)
                                        if gonext == 1:
                                            continue
                                    elif miner.x > coordinate[1]: #to the left
                                        while miner.front != 3:
                                            miner.rotate(board)
                                        while miner.x > coordinate[1]:
                                            lastpos = [miner.y,miner.x]
                                            if miner.scan(grid) == pit:
                                                board.rotate_ctr += 2
                                                miner.front = (miner.front+2)%4
                                                for k in range(moves):
                                                    print(moves)
                                                    miner.move(board)
                                                    grid[lastpos[0]][lastpos[1]] = 0
                                                    grid[miner.y][miner.x] = 1
                                                    updateDisplay(grid, GRID_SIZE,screen,board)
                                                gonext = 1
                                                break
                                            miner.move(board)
                                            moves+=1
                                            grid[lastpos[0]][lastpos[1]] = 0
                                            grid[board.beacons[i].pos[0]][board.beacons[i].pos[1]] = 3
                                            grid[miner.y][miner.x] = 1
                                            updateDisplay(grid, GRID_SIZE,screen,board)
                                        if gonext == 1:
                                            continue
                                    elif miner.y > coordinate[0]:#upwards
                                        while miner.front != 0:
                                            miner.rotate(board)
                                        while miner.y > coordinate[0]:
                                            lastpos = [miner.y,miner.x]
                                            if miner.scan(grid) == pit:
                                                board.rotate_ctr += 2
                                                miner.front = (miner.front+2)%4
                                                for k in range(moves):
                                                    print(moves)
                                                    miner.move(board)
                                                    grid[lastpos[0]][lastpos[1]] = 0
                                                    grid[miner.y][miner.x] = 1
                                                    updateDisplay(grid, GRID_SIZE,screen,board)
                                                gonext = 1
                                                break
                                            miner.move(board)
                                            moves+=1
                                            grid[lastpos[0]][lastpos[1]] = 0
                                            grid[board.beacons[i].pos[0]][board.beacons[i].pos[1]] = 3
                                            grid[miner.y][miner.x] = 1
                                            updateDisplay(grid, GRID_SIZE,screen,board)
                                        if gonext == 1:
                                            continue
                                    elif miner.y < coordinate[0]:#downwards
                                        while miner.front != 2:
                                            miner.rotate(board)
                                        while miner.y < coordinate[0]:
                                            lastpos = [miner.y,miner.x]
                                            if miner.scan(grid) == pit:
                                                board.rotate_ctr += 2
                                                miner.front = (miner.front+2)%4
                                                for k in range(moves):
                                                    print(moves)
                                                    miner.move(board)
                                                    grid[lastpos[0]][lastpos[1]] = 0
                                                    grid[miner.y][miner.x] = 1
                                                    updateDisplay(grid, GRID_SIZE,screen,board)
                                                gonext = 1
                                                break
                                            miner.move(board)
                                            moves+=1
                                            grid[lastpos[0]][lastpos[1]] = 0
                                            grid[board.beacons[i].pos[0]][board.beacons[i].pos[1]] = 3
                                            grid[miner.y][miner.x] = 1
                                            updateDisplay(grid, GRID_SIZE,screen,board)
                                        if gonext == 1:
                                            continue
                                    if [miner.y,miner.x] != prev_gold:
                                        board.rotate_ctr += 2
                                        miner.front = (miner.front+2)%4
                                        for k in range(beaconMove):
                                            lastpos = [miner.y,miner.x]
                                            miner.move(board)
                                            grid[lastpos[0]][lastpos[1]] = 0
                                            grid[miner.y][miner.x] = 1
                                            updateDisplay(grid, GRID_SIZE,screen,board)
                                    else:
                                        break
                    if [miner.y,miner.x] == prev_gold:
                        gameover = True
                        print("Win")
                        break
                    pygame.time.delay(250)
                #--------------------------------------------------

            # determine typew of object to place
            elif 2*WINDOW_WIDTH/3 <= pos[0] <= 2*WINDOW_WIDTH/3 + 65 and WINDOW_HEIGHT/2-100 <= pos[1] <= WINDOW_HEIGHT/2-60:
                placement_type = pit
            elif 2*WINDOW_WIDTH/3+75 <= pos[0] <= 2*WINDOW_WIDTH/3 + 140 and WINDOW_HEIGHT/2-100 <= pos[1] <= WINDOW_HEIGHT/2-60:
                placement_type = gold
            elif 2*WINDOW_WIDTH/3 <= pos[0] <= 2*WINDOW_WIDTH/3 + 140 and WINDOW_HEIGHT/2-150 <= pos[1] <= WINDOW_HEIGHT/2+40:
                placement_type = beacon
            
            # place objects by clicking on grid
            else:
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if row < GRID_SIZE and column < GRID_SIZE:
                    grid[row][column] = placement_type
                    if placement_type == beacon:
                        b = Beacon([row,column])
                        b.find_gold(grid)
                        board.beacons.append(b)
                    elif placement_type == gold:
                        if board.prev_gold:
                            grid[board.prev_gold[0]][board.prev_gold[1]] = 0
                        prev_gold = [row,column]
                    updateDisplay(grid, GRID_SIZE,screen,board)
        
pygame.quit()
