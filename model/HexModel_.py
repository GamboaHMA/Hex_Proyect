class HexModel:
    def __init__(self, size):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.current_player = 'Red'

    # Por el momento solo dos jugadores, una casilla puede ser 0, 1 o -1, 0 casilla vacia, 1 jugador 1, -1 jugador 2
    # Si vemos el tablero como un cuadrado, los bordes del jugador 1 seran izqu y derecha, jugador 2 arriba y abajo

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

        # todavia, esta mal
        fila_1 = self.board[0]
        fila_size = self.board[self.size - 1]

        columna_1 = [fila[0] for fila in self.board]
        columna_size = [fila[self.size - 1] for fila in self.board]

        if 1 in columna_1 and 1 in columna_size:
            return True
        elif -1 in fila_1 and -1 in fila_size:
            return True
        else:
            return False

            