from board import Board
import pygame as py
"""
SETTINGS
"""
SIZE = 850


def drawBoard(screen,size,board:Board):
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
    
    moves = board.legalmove()
    if moves:
        py.draw.rect(screen,(10,10,10),(board.lx*size,board.ly*size,size,size),5)
        for move in moves:
            py.draw.rect(screen,(10,10,10),(move[0]*size,move[1]*size,size,size),5)

py.init()

clock = py.time.Clock()
screen = py.display.set_mode((SIZE,SIZE))
w, h = screen.get_size()

board = Board(w,h)

running = True
while running:
    clock.tick(60)
    
    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            running = False
    
    board.update(events)
    
    screen.fill((10, 15, 5))
    
    drawBoard(screen,w, board)

    py.display.flip()

py.quit()