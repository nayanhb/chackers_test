from time import sleep

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
        self.must_continue = None

    def move(self, move:Move) -> bool:
        legal_move = self.getAllLegalMoves()
        
        if move.frm not in legal_move or move.to not in legal_move[move.frm]:
            return False
        
        piece = self.grid[move.frm[1]][move.frm[0]]
        is_capture = abs(move.frm[0] - move.to[0]) == 2
        
        self.grid[move.to[1]][move.to[0]] = piece
        self.grid[move.frm[1]][move.frm[0]] = 0
        
        if is_capture:
            middle_x = (move.frm[0] + move.to[0]) // 2
            middle_y = (move.frm[1] + move.to[1]) // 2
            self.grid[middle_y][middle_x] = 0
        
        #promotion
        if (move.to[1] == 0 and piece == 1) or (move.to[1] == 7 and piece == -1):
            self.grid[move.to[1]][move.to[0]] *= 2
            
        if is_capture and self.multikil(move.to):
            self.must_continue = tuple(move.to)
        else:
            self.must_continue = None
            self.turn *= -1
        return True
        
    def win(self) -> tuple[bool,int]:
        black = any(-1 in row or -2 in row for row in self.grid)
        white = any(1 in row or 2 in row for row in self.grid)
        
        if not black:
            return True,1
        elif not white:
            return True,-1
        
        if not self.getAllLegalMoves():
            return True,-self.turn
        
        return False,0
        
    def getLegalMove(self, x: int, y: int):
        """It gives a dictionary of all possible move of the given piece"""
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
        if self.must_continue is not None:
            pos = self.must_continue
            _, moves = self.getLegalMove(*pos)
            captures = [move for move in moves if abs(pos[0] - move[0]) == 2]
            return {pos: captures} if captures else {}
        
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
    
    def allMove(self) -> list:
        moves = list()
        for frm, move in self.getAllLegalMoves().items():
            for to in move:
                moves.append(Move(frm,to))
        return moves
        
    def multikil(self,pos) -> list:
        _,moves = self.getLegalMove(*pos)
        
        return [destination
                for destination in moves
                if abs(pos[0] - destination[0]) == 2
                ]