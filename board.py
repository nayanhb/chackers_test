import pygame as py


class Board:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        # black = -1; white = 1; 2 = if the touch the end
        self.grid = [
            [0, -1, 0, -1, 0, -1, 0, -1],
            [-1, 0, -1, 0, -1, 0, -1, 0],
            [0, -1, 0, -1, 0, -1, 0, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
        ]

        self.lx, self.ly = None, None  # last click
        self.move = 0

    def update(self, events):
        size = min(self.w, self.h) // 8
        
        for event in events:
            if event.type == py.FINGERDOWN:
                cx = int(event.x * self.w) // size  # current click
                cy = int(event.y * self.h) // size
                if cx < 8 and cy < 8:
                    if self.lx == None:  # selection
                        if self.grid[cy][cx] != 0:
                            self.move = self.grid[cy][cx]
                            self.lx, self.ly = cx,cy
                        
                    elif self.lx != None:  # move
                        #print(self.lx,self.ly,self.legalmove())
                        if self.grid[cy][cx] == self.move:
                            self.lx, self.ly = cx, cy
                        elif [cx, cy] in self.legalmove() and self.grid[cy][cx] != self.move:
                            self.grid[self.ly][self.lx] = 0
                            self.grid[cy][cx] = self.move
                            dx = cx - self.lx
                            dy = cy - self.ly
                            if dx == -2 and dy == -2:
                                self.grid[self.ly - 1][self.lx - 1] = 0  # ty: ignore[unsupported-operator]
                            elif dx == 2 and dy == -2:
                                self.grid[self.ly - 1][self.lx + 1] = 0  # ty: ignore[unsupported-operator]
                            elif dx == -2 and dy == 2:
                                self.grid[self.ly + 1][self.lx - 1] = 0  # ty: ignore[unsupported-operator]
                            elif dx == 2 and dy == 2:
                                self.grid[self.ly + 1][self.lx + 1] = 0  # ty: ignore[unsupported-operator]
                            
                            if cy == 0 and self.grid[cy][cx] == 1:
                                self.grid[cy][cx] = 2
                            elif cy == 7 and self.grid[cy][cx] == -1:
                                self.grid[cy][cx] = -2
                            
                            self.move = 0
                            self.lx, self.ly = None, None
                        else:
                            if self.grid[cy][cx] != 0:#other oppent click
                                self.move = self.grid[cy][cx]
                                self.lx, self.ly = cx,cy
                            else:#empty
                                self.move = 0
                                self.lx, self.ly = None, None

    def legalmove(self):
        if self.lx == None: return []
        
        lmove = []
        
        if self.move == 1:
            if ( # left
                self.ly - 2 >= 0  # ty: ignore[unsupported-operator]
                and self.lx - 2 >= 0
                and (
                self.grid[self.ly - 1][self.lx - 1] == -self.move  # ty: ignore[unsupported-operator]
                or self.grid[self.ly - 1][self.lx - 1] == (-self.move << 1) # ty: ignore[unsupported-operator]
                )
                and self.grid[self.ly - 2][self.lx - 2] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx - 2,self.ly - 2])  # ty: ignore[unsupported-operator]
            
            elif (
                self.ly - 1 >= 0  # ty: ignore[unsupported-operator]
                and self.lx - 1 >= 0
                and self.grid[self.ly - 1][self.lx - 1] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx - 1,self.ly - 1])  # ty: ignore[unsupported-operator]
            
            
            if ( # right 
                self.ly - 2 >= 0  # ty: ignore[unsupported-operator]
                and self.lx + 2 < 8
                and (
                self.grid[self.ly - 1][self.lx + 1] == -self.move  # ty: ignore[unsupported-operator]
                or self.grid[self.ly - 1][self.lx + 1] == (-self.move << 1) # ty: ignore[unsupported-operator]
                )
                and self.grid[self.ly - 2][self.lx + 2] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx + 2,self.ly - 2])  # ty: ignore[unsupported-operator]
            
            elif (
                self.ly - 1 >= 0  # ty: ignore[unsupported-operator]
                and self.lx + 1 < 8
                and self.grid[self.ly - 1][self.lx + 1] == 0  # ty: ignore[unsupported-operator]
                ):
                lmove.append([self.lx + 1,self.ly - 1])  # ty: ignore[unsupported-operator]
            
            
        elif self.move == -1:
            if ( # left 
                self.lx - 2 >= 0
                and self.ly + 2 < 8  # ty: ignore[unsupported-operator]
                and (
                self.grid[self.ly + 1][self.lx - 1] == -self.move  # ty: ignore[unsupported-operator]
                or self.grid[self.ly + 1][self.lx - 1] == -self.move << 1 # ty: ignore[unsupported-operator]
                )
                and self.grid[self.ly + 2][self.lx - 2] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx - 2, self.ly + 2])  # ty: ignore[unsupported-operator]
            
            elif self.lx - 1 >= 0 and self.ly + 1 < 8 and self.grid[self.ly + 1][self.lx - 1] == 0:  # ty: ignore[unsupported-operator]
                lmove.append([self.lx - 1, self.ly + 1])  # ty: ignore[unsupported-operator]


            if ( # right 
                self.lx - 2 >= 0
                and self.lx + 2 < 8
                and self.ly + 2 < 8  # ty: ignore[unsupported-operator]
                and (
                self.grid[self.ly + 1][self.lx + 1] == -self.move  # ty: ignore[unsupported-operator]
                or self.grid[self.ly + 1][self.lx + 1] == -self.move << 1 # ty: ignore[unsupported-operator]
                )
                and self.grid[self.ly + 2][self.lx + 2] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx + 2, self.ly + 2])  # ty: ignore[unsupported-operator]
            
            elif (
                self.lx + 1 < 8
                and self.ly + 1 < 8  # ty: ignore[unsupported-operator]
                and self.grid[self.ly + 1][self.lx + 1] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx + 1, self.ly + 1])  # ty: ignore[unsupported-operator]
        
        
        elif self.move == 2 or self.move == -2:
            if ( # left
                self.ly - 2 >= 0  # ty: ignore[unsupported-operator]
                and self.lx - 2 >= 0
                and(
                self.grid[self.ly - 1][self.lx - 1] == -self.move  # ty: ignore[unsupported-operator]
                or self.grid[self.ly - 1][self.lx - 1] == -self.move >> 1 # ty: ignore[unsupported-operator]
                )
                and self.grid[self.ly - 2][self.lx - 2] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx - 2,self.ly - 2])  # ty: ignore[unsupported-operator]
            
            elif (
                self.ly - 1 >= 0  # ty: ignore[unsupported-operator]
                and self.lx - 1 >= 0
                and self.grid[self.ly - 1][self.lx - 1] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx - 1,self.ly - 1])  # ty: ignore[unsupported-operator]
            
            
            if ( # right 
                self.ly - 2 >= 0  # ty: ignore[unsupported-operator]
                and self.lx + 2 < 8
                and (
                self.grid[self.ly - 1][self.lx + 1] == -self.move  # ty: ignore[unsupported-operator]
                or self.grid[self.ly - 1][self.lx + 1] == -self.move >> 1 # ty: ignore[unsupported-operator]
                )
                and self.grid[self.ly - 2][self.lx + 2] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx + 2,self.ly - 2])  # ty: ignore[unsupported-operator]
            
            elif (
                self.ly - 1 >= 0  # ty: ignore[unsupported-operator]
                and self.lx + 1 < 8
                and self.grid[self.ly - 1][self.lx + 1] == 0  # ty: ignore[unsupported-operator]
                ):
                lmove.append([self.lx + 1,self.ly - 1])  # ty: ignore[unsupported-operator]
            
            if ( # left 
                self.lx - 2 >= 0
                and self.ly + 2 < 8  # ty: ignore[unsupported-operator]
                and (
                self.grid[self.ly + 1][self.lx - 1] == -self.move  # ty: ignore[unsupported-operator]
                or self.grid[self.ly + 1][self.lx - 1] == -self.move >> 1 # ty: ignore[unsupported-operator]
                )
                and self.grid[self.ly + 2][self.lx - 2] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx - 2, self.ly + 2])  # ty: ignore[unsupported-operator]
            
            elif self.lx - 1 >= 0 and self.ly + 1 < 8 and self.grid[self.ly + 1][self.lx - 1] == 0:  # ty: ignore[unsupported-operator]
                lmove.append([self.lx - 1, self.ly + 1])  # ty: ignore[unsupported-operator]


            if ( # right 
                self.lx + 2 < 8
                and self.ly + 2 < 8  # ty: ignore[unsupported-operator]
                and (
                self.grid[self.ly + 1][self.lx + 1] == -self.move  # ty: ignore[unsupported-operator]
                or self.grid[self.ly + 1][self.lx + 1] == -self.move >> 1 # ty: ignore[unsupported-operator]
                )
                and self.grid[self.ly + 2][self.lx + 2] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx + 2, self.ly + 2])  # ty: ignore[unsupported-operator]
            
            elif (
                self.lx + 1 < 8
                and self.ly + 1 < 8  # ty: ignore[unsupported-operator]
                and self.grid[self.ly + 1][self.lx + 1] == 0  # ty: ignore[unsupported-operator]
            ):
                lmove.append([self.lx + 1, self.ly + 1])  # ty: ignore[unsupported-operator]
        
        return lmove
