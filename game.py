"""
# game.py
# Handle touch input
# Select a piece
# Display its legal moves
# Send chosen move to board.update()

"""
from board import Board,Move
import pygame as py
"""
SETTINGS
"""
SIZE = 850

def update(lastPos,pos):
    if pos[0] >= 8 or pos[0] < 0:
        return
    board.move(Move(lastPos,pos))
    lastPos = pos
    return lastPos
    

def drawBoard(screen,size,board:Board,posx,posy):
    size = size // 8
    #Board
    for y in range(8):
        for x in range(8):
            if (x + y) & 1 == 0:
                py.draw.rect(screen,(255,255,255),(x*size,y*size, size, size))
            else:
                py.draw.rect(screen,(20,155,20),(x*size,y*size, size, size))
    #pieces
    for y in range(8):
        for x in range(8):
            piece = board.grid[y][x]
            if piece == 1:
                py.draw.circle(screen,(230,230,230),((x + 0.5)*size,(y + 0.5)*size),size//2 - 10)
            elif piece == -1:
                py.draw.circle(screen,(0,0,0),((x + 0.5)*size,(y + 0.5)*size),size//2 - 10)
            elif piece == 2:
                py.draw.circle(screen,(230,230,230),((x + 0.5)*size,(y + 0.5)*size),size//2 - 10)
                py.draw.circle(screen,(0,0,0),((x + 0.5)*size,(y + 0.5)*size),size//2 - 10,5)
                py.draw.circle(screen,(0,0,0),((x + 0.5)*size,(y + 0.5)*size),5)
            elif piece == -2:
                py.draw.circle(screen,(0,0,0),((x + 0.5)*size,(y + 0.5)*size),size//2 - 10)
                py.draw.circle(screen,(230,230,230),((x + 0.5)*size,(y + 0.5)*size),size//2 - 10,5)
                py.draw.circle(screen,(230,230,230),((x + 0.5)*size,(y + 0.5)*size),5)
    
    moves = board.getLegalMove(posx,posy)[1]
    if moves and board.grid[posy][posx] * board.turn > 0:
        for move in moves:
            py.draw.rect(screen,(20,10,20),(move[0]*size,move[1]*size, size, size),10)

py.init()

clock = py.time.Clock()
screen = py.display.set_mode((SIZE,SIZE))
w, h = screen.get_size()

SIZE = w

board = Board(w,h)
x = y = 0

lastPos:list= [0,0]

running = True
while running:
    clock.tick(60)
    
    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            running = False
        if event.type == py.FINGERDOWN:
            x,y = event.x * w, event.y * h
            x, y = int(x // (SIZE // 8)),int(y // (SIZE // 8))
            lastPos = update(lastPos,[x,y])
            
    # board.update(events)
    
    screen.fill((10, 15, 5))
    
    drawBoard(screen,w, board,x,y)

    py.display.flip()
    
py.quit()