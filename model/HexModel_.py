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
            self.board[i][j] = self.current_player
            self.current_player = 2 if self.current_player == 1 else 1
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
        i = random.randint(0, len(movements))
        return movements[i]
    
class MinMaxPlayer(Player):
    def __init__(self, player_id, h): # h-heuristic
        super().__init__(player_id)
        self.h = h

    def play(self, board:HexBoard) -> tuple:
        b_move, value = self.alpha_beta(board, 2, -float('inf'), float('inf'), self.h, True)
        return b_move

    def alpha_beta(self, board:HexBoard, p:int, a:float, b:float, h, max:bool):  # p-profundidad, a-alpha, b-beta, h-heuristic, max o min 
        if p == 0:
            return h(board.board)
        
        if max:
            value = -float('inf')
            b_move = None  # best_move
            for move in board.get_possible_moves():
                new_board = board.clone()
                new_value = self.alpha_beta(new_board.place_piece(move), p-1, a, b, h, not max)
                if new_value >= value:
                    b_move = move
                    value = new_value
                    a = max(a, value)
                    if a >= b:
                        break
            return b_move, value

        else:
            value = float('inf')
            b_move = None  # best_move
            for move in board.get_possible_moves():
                new_board = board.clone()
                new_value = self.alpha_beta(new_board.place_piece(move), p-1, a, b, h, not max)
                if new_value <= value:
                    b_move = move
                    value = new_value
                    b = min(b, value)
                    if a >= b:
                        break
            return b_move, value



         