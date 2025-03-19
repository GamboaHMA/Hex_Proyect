class HexBoard:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.turn = 1 

    # Por el momento solo dos jugadores, una casilla puede ser 0, 1 o -1, 0 casilla vacia, 1 jugador 1, -1 jugador 2
    # Si vemos el tablero como un cuadrado, los bordes del jugador 1 seran izqu y derecha, jugador 2 arriba y abajo

    def game_over(self):

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

            