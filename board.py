import pygame as py

class Move:
    def __init__(self, frm, to):
        self.frm = tuple(frm)
        self.to = list(to)

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

        self.turn = 1

    def move(self, move:Move):
        print(self.captures(self.getAllLegalMoves()))
        for key, moves in self.getAllLegalMoves().items():
            if move.frm == key:
                for i in moves:
                    if move.to == i:
                        self.grid[move.to[1]][move.to[0]] = self.grid[move.frm[1]][move.frm[0]]
                        self.grid[move.frm[1]][move.frm[0]] = 0
                        self.turn = -self.turn
                        
                        if abs(move.frm[0] - move.to[0]) == 2:
                            self.grid[(move.frm[1]+move.to[1])//2][(move.frm[0]+move.to[0])//2] = 0
                        
                            if self.captures(self.getAllLegalMoves()):
                                self.turn = -self.turn
                        break
        if (move.to[1] == 0 and self.grid[move.to[1]][move.to[0]] == 1) or (move.to[1] == 7 and self.grid[move.to[1]][move.to[0]] == -1):
            self.grid[move.to[1]][move.to[0]] = self.grid[move.to[1]][move.to[0]] << 1
            
    def getLegalMove(self, x: int, y: int):
        if not (0 <= x < 8 and 0 <= y < 8):
            return []

        lmoves = list()
        if self.grid[y][x] == 1:
            # left
            if (
                x - 2 >= 0
                and y - 2 >= 0
                and (self.grid[y - 1][x - 1] == -1 or self.grid[y - 1][x - 1] == -2)
                and self.grid[y - 2][x - 2] == 0
            ):
                lmoves.append([x - 2, y - 2])
            elif (
                x - 1 >= 0
                and y - 1 >= 0
                and self.grid[y - 1][x - 1] == 0
            ):
                lmoves.append([x - 1,y - 1])
            # right 
            if (
                x + 2 < 8
                and y - 2 >= 0
                and (self.grid[y - 1][x + 1] == -1 or self.grid[y - 1][x + 1] == -2)
                and self.grid[y - 2][x + 2] == 0
            ):
                lmoves.append([x + 2, y - 2])
            elif (
                x + 1 < 8
                and y - 1 >= 0
                and self.grid[y - 1][x + 1] == 0
            ):
                lmoves.append([x + 1,y - 1])
        
        elif self.grid[y][x] == -1:
            # left
            if (
                x - 2 >= 0
                and y + 2 < 8
                and (self.grid[y + 1][x - 1] == 1 or self.grid[y + 1][x - 1] == 2)
                and self.grid[y + 2][x - 2] == 0
            ):
                lmoves.append([x - 2, y + 2])
            elif (
                x - 1 >= 0
                and y + 1 < 8
                and self.grid[y + 1][x - 1] == 0
            ):
                lmoves.append([x - 1,y + 1])
            # right 
            if (
                x + 2 < 8
                and y + 2 < 8
                and (self.grid[y + 1][x + 1] == 1 or self.grid[y + 1][x + 1] == 2)
                and self.grid[y + 2][x + 2] == 0
            ):
                lmoves.append([x + 2, y + 2])
            elif (
                x + 1 < 8
                and y + 1 < 8
                and self.grid[y + 1][x + 1] == 0
            ):
                lmoves.append([x + 1,y + 1])
        
        elif abs(self.grid[y][x]) == 2:
            sign = 1 if self.grid[y][x] > 0 else -1
            # UP
            # left
            if (
                x - 2 >= 0
                and y - 2 >= 0
                and (self.grid[y - 1][x - 1] == -sign or self.grid[y - 1][x - 1] == -(sign << 1))
                and self.grid[y - 2][x - 2] == 0
            ):
                lmoves.append([x - 2, y - 2])
            elif (
                x - 1 >= 0
                and y - 1 >= 0
                and self.grid[y - 1][x - 1] == 0
            ):
                lmoves.append([x - 1,y - 1])
            # right 
            if (
                x + 2 < 8
                and y - 2 >= 0
                and (self.grid[y - 1][x + 1] == -sign or self.grid[y - 1][x + 1] == -(sign << 1))
                and self.grid[y - 2][x + 2] == 0
            ):
                lmoves.append([x + 2, y - 2])
            elif (
                x + 1 < 8
                and y - 1 >= 0
                and self.grid[y - 1][x + 1] == 0
            ):
                lmoves.append([x + 1,y - 1])
            # DOWN
            # left
            if (
                x - 2 >= 0
                and y + 2 < 8
                and (self.grid[y + 1][x - 1] == -sign or self.grid[y + 1][x - 1] == -(sign << 1))
                and self.grid[y + 2][x - 2] == 0
            ):
                lmoves.append([x - 2, y + 2])
            elif (
                x - 1 >= 0
                and y + 1 < 8
                and self.grid[y + 1][x - 1] == 0
            ):
                lmoves.append([x - 1,y + 1])
            # right 
            if (
                x + 2 < 8
                and y + 2 < 8
                and (self.grid[y + 1][x + 1] == -sign or self.grid[y + 1][x + 1] == -(sign << 1))
                and self.grid[y + 2][x + 2] == 0
            ):
                lmoves.append([x + 2, y + 2])
            elif (
                x + 1 < 8
                and y + 1 < 8
                and self.grid[y + 1][x + 1] == 0
            ):
                lmoves.append([x + 1,y + 1])
            
        return (x,y),lmoves
        
    def getAllLegalMoves(self) -> dict:
        lmoves = dict()
        capture = False
        for x in range(8):
            for y in range(8):
                if self.grid[y][x] * self.turn > 0:
                    pos , moves = self.getLegalMove(x,y)
                    
                    for move in moves:
                        if abs(pos[0] - move[0]) == 2:
                            capture = True
                    
                    lmoves[pos] = moves
        
        
        if capture:
            newMoves = self.captures(lmoves)
            return newMoves
        
        return lmoves

    def captures(self,lmoves):
        newMoves = dict()
        for pos, moves in lmoves.items():
            captures = [move for move in moves if abs(pos[0] - move[0]) == 2]
            if captures:
                newMoves[pos] = captures
                
        return newMoves