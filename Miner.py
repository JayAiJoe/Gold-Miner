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
                #basic Roomba behavior: forward until you hit a wall, then rotate, repeat
                gameover = False
                while not gameover:
                    if miner.scan(grid) == 0: #if empty, move forward
                        grid[miner.y][miner.x] = 0
                        miner.move(board)
                        grid[miner.y][miner.x] = 1
                        updateDisplay(grid, GRID_SIZE,screen,board)
                    elif miner.scan(grid) == -1 or miner.scan(grid) == pit: #if pit, rotate
                        miner.rotate(board)
                    else: #if gold, stop
                        gameover = True
                        print("treasure")
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
                        beacons.append(b)
                    elif placement_type == gold:
                        if board.prev_gold:
                            grid[board.prev_gold[0]][board.prev_gold[1]] = 0
                        prev_gold = [row,column]
                    updateDisplay(grid, GRID_SIZE,screen,board)
        
pygame.quit()
