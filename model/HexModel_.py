import random

HEX_DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1)]

class HexBoard:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 1

    # Por el momento solo dos jugadores, una casilla puede ser 0, 1 o -1, 0 casilla vacia, 1 jugador 1, -1 jugador 2
    # Si vemos el tablero como un cuadrado, los bordes del jugador 1 seran izqu y derecha, jugador 2 arriba y abajo
    def get_not_cuurent_player(self):
        return 2 if self.current_player == 1 else 1

    def place_piece(self, row:int, col:int, player:int) -> bool:
        i = row
        j = col
        if self.board[i][j] == 0:
            self.board[i][j] = player
            self.current_player = 2 if player == 1 else 1
            return True
        else:
            return False
        

    def get_possible_moves(self) -> list:
        possible_movements = []
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    possible_movements.append((i,j))
            
        return possible_movements

    def check_connection(self, player_id:int):

        # solo hay que comprobar las casillas ocupadas de dos laterales adyacentes
        reds = []
        blues = []
        # aniadimos a las casillas a comprobar solo las que estan en uno de los bordes

        for i in range(self.size):
            if self.board[i][0] == 1:
                reds.append((i, 0))
            if self.board[0][i] == 2:
                blues.append((0,i))
        if player_id == 2:
            board_mask = [[True for _ in range(self.size)] for _ in range(self.size)]
            for red in reds:
                result = deep_hexagonal_search(self.board, board_mask, red, 1)
                if result:
                    return result
        else:
            board_mask = [[True for _ in range(self.size)] for _ in range(self.size)]
            for blue in blues:
                result = deep_hexagonal_search(self.board, board_mask, blue, 2)
                if result:
                    return result
        return False
    
    def clone(self) -> "HexBoard":
        hex_cloned = HexBoard(self.size)
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                hex_cloned.board[i][j] = self.board[i][j]

        return hex_cloned




        

def deep_hexagonal_search(board, board_mask, actual_cell, player): # no es necesario devolver que jugador gano ya que solo puede ganar el ultimo que jugo
    cola = []
    row = actual_cell[0]
    col = actual_cell[1]
    cola.append(actual_cell)
    board_mask[row][col] = False

    while(len(cola) != 0):
        cell = cola.pop(0)
        row = cell[0]
        col = cell[1]
        board_mask[row][col] = False
        if player == 1:  # entonces verificar que la casilla esta en la ultima columna
            if col == len(board) - 1:
                return True
            adjacents = get_adjacents(board, board_mask, cell, player)
            for adjacent in adjacents:
                cola.append(adjacent)
                board_mask[adjacent[0]][adjacent[1]] = False
            
        else: # player == 'Blue'
            if row == len(board) - 1:
                return True 
            adjacents = get_adjacents(board, board_mask, cell, player)
            for adjacent in adjacents:
                cola.append(adjacent)
    return False

def get_adjacents(board, board_mask, cell, player):
    result = []
    for dir in HEX_DIRECTIONS:
        new_c = (cell[0] + dir[0], cell[1] + dir[1])  # itera por todas las direcciones del hexagono y comprueba que no se haya pasado por ahi y que tenga mismo color
        if new_c[0] >= 0 and new_c[0] < len(board) and new_c[1] >= 0 and new_c[1] < len(board) and board_mask[new_c[0]][new_c[1]] and board[new_c[0]][new_c[1]] == player:
            result.append(new_c)

    return result

class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    def play(self, board: HexBoard) -> tuple:
        raise not NotImplementedError("Implementa este método")
    

class RandomPlayer(Player):
    def play(self, board:HexBoard) -> tuple:
        movements = board.get_possible_moves()
        i = random.randint(0, len(movements) - 1)
        return movements[i]
    
class MinMaxPlayer(Player):
    def __init__(self, player_id, h): # h-heuristic
        super().__init__(player_id)
        self.h = h

    def play(self, board:HexBoard) -> tuple:
        b_move, value = self.alpha_beta(board, 3, -float('inf'), float('inf'), self.h, True)
        print(value)
        return b_move

    def alpha_beta(self, board:HexBoard, p:int, a:float, b:float, h, max_:bool):  # p-profundidad, a-alpha, b-beta, h-heuristic, max o min 
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

def connection_heurisitc(board:HexBoard, player:int):
    '''
    Si hay una casilla de player sin vecinos entonces no se añade a set, si hay una casilla que tiene al menos un vecino, entonces
    se almacena en set tanto la casilla como la vecina, ya que la propia se añade cuando se itera por la casilla vecina, esta heuristica
    sencilla cuenta cuantas casillas hay conectadas, y devuelve la cantidad de casillas de player menos la cant del adversario y lo divide
    entre la suma total de puntos, así se asegura que se devuelva un valor entre -1 y 1, mientras más se acerque a 1, mejor para 
    player y peor para adversario, mientras más se acerque a -1 peor para player y mejor para adversario
    '''

    adversary = 2 if player == 1 else 1
    p_c = 0  # player_count
    p_set = set()  # player_set

    a_c = 0  # adversary_count
    a_set = set()  # adversary_set
    board_mask = [[True for _ in range(len(board))] for _ in range(len(board))]  # para cumplir con el parametro de get_adjacents()

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == player:
                adjacents = get_adjacents(board, board_mask,(i,j), player)
                for adjacent in adjacents:
                    if adjacent not in p_set:
                        p_set.add(adjacent)
                        p_c += 1
            
            if board[i][j] == adversary:
                adjacents = get_adjacents(board, board_mask, (i,j), adversary)
                for adjacent in adjacents:
                    if adjacent not in a_set:
                        a_set.add(adjacent)
                        a_c += 1

    if (p_c != 0 or a_c != 0):
        result = (p_c - a_c)/max(p_c,a_c)
        return result
    else:
        return 0
                
def templates_heuristics(board:HexBoard, player:int, time=1000):
    bridges = get_bridges(board)



def get_bridges(board:HexBoard):
    result = []
    set_ = set()
    for i in range(len(board.board)):
        for j in range(len(board.board)):
            p = board.board[i][j]
            if p != 0:
                if i-1 >= 0 and j-1 >= 0:  # arriba izquierda
                    new_p = board.board[i-1][j-1]
                    if p == new_p and board.board[i-1][j] == 0 and board.board[i][j-1] == 0:  # verifica tambien que las casillas de en medio esten vacias
                        if (i,j) not in set_ :
                            result.append((i,j))
                            set_.add((i,j))
                        if (i-1, j-1) not in set_:
                            result.append((i-1,j-1))
                            set_.add((i-1,j-1))
                                        
                if i+1 < len(board.board) and j+1 < len(board.board):  # abajo derecha
                    new_p = board.board[i+1][j+1]
                    if p == new_p and board.board[i+1][j] == 0 and board.board[i][j+1] == 0:
                        if (i,j) not in set_ :
                            result.append((i,j))
                            set_.add((i,j))
                        if (i+1,j+1) not in set_:
                            result.append((i+1,j+1))
                            set_.add((i+1,j+1))

                if i-2 >= 0 and j+1 < len(board.board):  # 2 arriba derecha
                    new_p = board.board[i-2][j+1]
                    if p == new_p and board.board[i-1][j] == 0 and board.board[i-1][j+1] == 0:
                        if (i,j) not in set_ :
                            result.append((i,j))
                            set_.add((i,j))
                        if (i-2,j+1) not in set_:
                            result.append((i-2,j+1))
                            set_.add((i-2,j+1))
                        
                if i-1 >= 0 and j+2 < len(board.board):  # arriba 2 derecha
                    new_p = board.board[i-1][j+2]
                    if p == new_p and board.board[i-1][j+1] == 0 and board.board[i][j+1] == 0:
                        if (i,j) not in set_:
                            result.append((i,j))
                            set_.add((i,j))
                        if (i-1, j+2) not in set_:
                            result.append((i-1, j+2))
                            set_.add((i-1, j+2))

                if i+2 < len(board.board) and j-1 >= 0 :  # 2 abajo izquierda
                    new_p = board.board[i+2][j-1]
                    if p == new_p and board.board[i+1][j] == 0 and board.board[i+1][j-1] == 0:
                        if (i,j) not in set_ :
                            result.append((i,j))
                            set_.add((i,j))
                        if (i+2,j-1) not in set_:
                            result.append((i+2,j-1))
                            set_.add((i+2,j-1))
                
                if i+1 < len(board.board) and j-2 >= 0 :  # abajo 2 izquierda
                    new_p = board.board[i+1][j-2]
                    if p == new_p and board.board[i+1][j-1] == 0 and board.board[i][j-1] == 0:
                        if (i,j) not in set_ :
                            result.append((i,j))
                            set_.add((i,j))
                        if (i+1,j-2) not in set_:
                            result.append((i+1,j-2))
                            set_.add((i+1,j-2))

        
    return result



def get_if_bord_unblockable(board:HexBoard):
    result = []
    size = len(board.board)
    for i in range(size):
        for j in range(size):
            p = board.board[i][j]
            if p == 1:
                if j > size//2:
                    if no_block(board, i, j, size, p, 2):
                        result.append(i,j)
                else:
                    if no_block(board, i, j, size, p, 0):
                        result.append(i,j)
            elif p == 2:
                pass
            

def no_block(board:HexBoard, i , j, size, p, dir):  # 0: izq, 1: arriba, 2: derecha, 3: abajo
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
        
def template_a2(pos, board:HexBoard, player):  # devuelve true si la casilla parametro formase una plantilla en caso de que se hubiera jugado ahi
    i,j = pos                                  # modificar el como si estuviera a un parametro de si esta de verdad
    size = len(board.board)
    if player == 1:
        if j-1 == 0 and i+1 < size:
            if board.board[i][j-1] == 0 and board.board[i+1][j-1] == 0:
                return True
        if j+1 == size-1 and i-1 >= 0:
            if board.board[i][j+1] == 0 and board.board[i-1][j+1] == 0:
                return True
    elif player == 2:
        if i+1 == size-1 and j-1 >= 0:
            if board.board[i+1][j] == 0 and board.board[i+1][j-1] == 0:
                return True
        if i-1 == 0 and j-1 >= 0:
            if board.board[i-1][j-1] == 0 and board.board[i-1][j] == 0:
                return True
    
    return False

def template_a3(pos, board:HexBoard, player):
    i,j = pos
    size = len(board.board)
    if player == 1:
        if j-2 == 0 and i + 3 < size:
            if template_a2((i, j-1), board, player) and board.board[i+1][j] == 0 and board.board[i+1][j-1] == 0 and template_a2((i+2, j-1), board, player):  # los iguales a 0 permiten que sean puente
                return True
        if j-2 == 0 and i-1 >= 0 and i+2 < size:
            if template_a2((i+1, j-1), board, player) and board.board[i][j-1] == 0 and board.board[i-1][j] == 0 and template_a2((i-1, j-1), board, player):
                return True
        if j+2 == size-1 and i-2 >= 0 and i+1 < size:
            if template_a2((i-1, j+1), board, player) and board.board[i][j+1] == 0 and board.board[i+1][j] == 0 and template_a2((i+1, j+1), board, player):
                return True
        if j+2 == size-1 and i-3 >= 0:
            if template_a2((i, j+1), board, player) and board.board[i-1][j] == 0 and board.board[i-1][j+1] == 0 and template_a2((i-2, j+1), board, player):
                return True
            
    elif player == 2:
        if i-2 == 0 and j + 3 < size:
            if template_a2((i-1, j), board, player) and board.board[i][j+1] == 0 and board.board[i-1][j+1] == 0 and template_a2((i-1, j+2), board, player):  # los iguales a 0 permiten que sean puente
                return True
        if i-2 == 0 and j-1 >= 0 and j+2 < size:
            if template_a2((i-1, j+1), board, player) and board.board[i-1][j] == 0 and board.board[i][j-1] == 0 and template_a2((i-1, j-1), board, player):
                return True
        if i+2 == size-1 and j-2 >= 0 and j+1 < size:
            if template_a2((i+1, j-1), board, player) and board.board[i+1][j] == 0 and board.board[i][j+1] == 0 and template_a2((i+1, j+1), board, player):
                return True
        if i+2 == size-1 and j-3 >= 0:
            if template_a2((i+1, j), board, player) and board.board[i][j-1] == 0 and board.board[i+1][j-1] == 0 and template_a2((i+1, j-2), board, player):
                return True
        
    return False
