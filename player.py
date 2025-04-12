
class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    def play(self, board) -> tuple:
        raise not NotImplementedError("Implementa este método")
    

class MinMaxPlayer(Player):
    def __init__(self, player_id, h): # h-heuristic
        super().__init__(player_id)
        self.h = h

    def play(self, board) -> tuple:
        b_move, value = self.alpha_beta(board, 3, -float('inf'), float('inf'), self.h, True)
        print(value)
        return b_move

    def alpha_beta(self, board, p:int, a:float, b:float, h, max_:bool):  # p-profundidad, a-alpha, b-beta, h-heuristic, max o min 
        if p == 0:
            return 0, h(board.board, self.player_id)
        
        if max_:
            value = -float('inf')
            b_move = None  # best_move
            for x, y in board.get_possible_moves():
                new_board = board.clone()
                new_board.place_piece(x, y, self.player_id)
                new_value = self.alpha_beta(new_board, p-1, a, b, h, not max_)
                if new_value[1] > value:  # indexado en 1 porque devuelve una tupla, valor en pos 1
                    b_move = (x, y)
                    value = new_value[1]
                    a = max(a, value)
                    if a >= b:
                        break
            return b_move, value

        else:
            value = float('inf')
            b_move = None  # best_move
            for x, y in board.get_possible_moves():
                adversary = 2 if self.player_id == 1 else 1
                new_board = board.clone()
                new_board.place_piece(x, y, adversary)
                new_value = self.alpha_beta(new_board, p-1, a, b, h, not max_)
                if new_value[1] < value:   # indexado en 1 porque devuelve una tupla, valor en pos 1
                    b_move = (x, y)
                    value = new_value[1]
                    b = min(b, value)
                    if a >= b:
                        break
            return b_move, value

def templates_heuristics(board, player:int, time=1000):
    bridges = get_bridges(board)



def get_bridges(board):
    result = []
    set_ = set()
    for i in len(board.board):
        for j in len(board.board):
            p = board.board[i][j]
            if p != 0:
                if i-1 >= 0 and j-1 >= 0:
                    new_p = board[i-1][j-1]
                    if p == new_p:     # arriba izquierda
                        if p not in set_ :
                            result.append((i,j), (i-1,j-1))
                            set_.add(p)
                            if new_p not in set_:
                                set_.add(new_p)
                        elif new_p not in set_:
                            result.append((i,j), (i-1,j-1))
                            set_.add(new_p)
                            if p not in set_:
                                set_.add(p)
                                        
                if i+1 < len(board.board) and j+1 < len(board.board):  # abajo derecha
                    new_p = board.board[i+1][j+1]
                    if p == new_p:
                        if p not in set_ :
                            result.append((i,j), (i+1,j+1))
                            set_.add(p)
                            if new_p not in set_:
                                set_.add(new_p)
                        elif new_p not in set_:
                            result.append((i,j), (i+1,j+1))
                            set_.add(new_p)
                            if p not in set_:
                                set_.add(p)
                if i-2 >= 0 and j+1 < len(board.board):  # 2 arriba derecha
                    new_p = board.board[i-2][j+1]
                    if p == new_p:
                        if p not in set_ :
                            result.append((i,j), (i-2,j+1))
                            set_.add(p)
                            if new_p not in set_:
                                set_.add(new_p)
                        elif new_p not in set_:
                            result.append((i,j), (i-2,j+1))
                            set_.add(new_p)
                            if p not in set_:
                                set_.add(p)

                if i+2 < len(board.board) and j-1 >= 0 :  # 2 abajo izquierda
                    new_p = board.board[i+2][j-1]
                    if p == new_p:
                        if p not in set_ :
                            result.append((i,j), (i+2,j-1))
                            set_.add(p)
                            if new_p not in set_:
                                set_.add(new_p)
                        elif new_p not in set_:
                            result.append((i,j), (i+2,j-1))
                            set_.add(new_p)
                            if p not in set_:
                                set_.add(p)
        
    return result


def get_if_bord_unblockable(board):
    result = []
    size = len(board.board)
    for i in range(size):
        for j in range(size):
            p = board.board[i][j]
            
            if j > size//2:
                if no_block(board, i, j, size, p, 3):
                    result.append(i,j)
            elif j <= size//2:
                if no_block(board, i, j, size, p, 2):
                    result.append(i,j)
            

def no_block(board, i , j, size, p, dir):  # 0: izq, 1: arriba, 2: derecha, 3: abajo
    if dir == 3:
        if i+1 < size:
            if j-1 >=0:
                if board[i][j] == p or board[i][j] == 0:
                    if no_block(board, i+1, j, size, p, dir) and no_block(board, i+1, j-1) :
                        return True
                    else:
                        return False
                else: return False
            else:
                if board[i][j] == p or board[i][j] == 0:
                    return no_block(board, i+1, j, size, p, dir)
                else: return False
        else :
            if board[i][j] == p or board[i][j] == 0:
                return True
            else:
                return False 
        
    elif dir == 0:
        if j-1 >= 0:
            if i+1 < size:
                if board[i][j] == p or board[i][j] == 0:
                    if no_block(board, i+1, j-1, size, p, dir) and no_block(board, i, j-1) :
                        return True
                    else:
                        return False
                else: return False
            else:
                if board[i][j] == p or board[i][j] == 0:
                    return no_block(board, i, j-1, size, p, dir)
                else: return False
        else :
            if board[i][j] == p or board[i][j] == 0:
                return True
            else:
                return False 
    
    elif dir == 1:
        if i-1 >= 0:
            if j+1 < size:
                if board[i][j] == p or board[i][j] == 0:
                    if no_block(board, i-1, j+1, size, p, dir) and no_block(board, i+1, j-1) :
                        return True
                    else:
                        return False
                else: return False
            else:
                if board[i][j] == p or board[i][j] == 0:
                    return no_block(board, i-1, j, size, p, dir)
                else: return False
        else :
            if board[i][j] == p or board[i][j] == 0:
                return True
            else:
                return False 

    elif dir == 2:
        if i+1 < size:
            if j-1 >= 0:
                if board[i][j] == p or board[i][j] == 0:
                    if no_block(board, i+1, j-1, size, p, dir) and no_block(board, i+1, j-1) :
                        return True
                    else:
                        return False
                else: return False
            else:
                if board[i][j] == p or board[i][j] == 0:
                    return no_block(board, i+1, j, size, p, dir)
                else: return False
        else :
            if board[i][j] == p or board[i][j] == 0:
                return True
            else:
                return False 
        
                
         
