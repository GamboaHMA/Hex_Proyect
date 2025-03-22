HEX_DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1)]

class HexModel:
    def __init__(self, size):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.current_player = 'Red'

    # Por el momento solo dos jugadores, una casilla puede ser 0, 1 o -1, 0 casilla vacia, 1 jugador 1, -1 jugador 2
    # Si vemos el tablero como un cuadrado, los bordes del jugador 1 seran izqu y derecha, jugador 2 arriba y abajo
    def get_not_cuurent_player(self):
        return 'Blue' if self.current_player == 'Red' else 'Red'

    def make_move(self, coord):
        i = coord[0] 
        j = coord[1]
        if self.board[i][j] == None:
            self.board[i][j] = self.current_player
            self.current_player = 'Blue' if self.current_player == 'Red' else 'Red'
            return True
        else:
            return False
        

    def get_possible_movements(self):
        possible_movements = []
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == None:
                    possible_movements.append((i,j))
            
        return possible_movements

    def game_over(self):

        # solo hay que comprobar las casillas ocupadas de dos laterales adyacentes
        reds = []
        blues = []
        # aniadimos a las casillas a comprobar solo las que estan en uno de los bordes
        for i in range(self.size):
            if self.board[i][0] == 'Red':
                reds.append((i, 0))
            if self.board[0][i] == 'Blue':
                blues.append((0,i))

        board_mask = [[True for _ in range(self.size)] for _ in range(self.size)]
        for red in reds:
            result = deep_hexagonal_search(self.board, board_mask, red, 'Red')
            if result:
                return result
        
        board_mask = [[True for _ in range(self.size)] for _ in range(self.size)]
        for blue in blues:
            result = deep_hexagonal_search(self.board, board_mask, blue, 'Blue')
            if result:
                return result
        
        return False


        

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
        if player == 'Red':  # entonces verificar que la casilla esta en la ultima columna
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