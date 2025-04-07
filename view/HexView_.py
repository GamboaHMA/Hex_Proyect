import pygame
import math
from model.HexModel_ import *

PROPORTION = 1.6  # proporcion entre la diagonal mayor con respecto a la diagonal menor del rombo que forman los sizexsize casillas hexagonales
RL_PS = [((160, 3), (6, 280)), ((378, 306), (208, 592))] # init_redline_point
BL_PS = [((6, 307), (165, 589)),((209, 5), (372, 280))] # end_redline_point


class HexCell:
    def __init__(self, model_coords, screen_coords):
        self.model_coords = model_coords
        self.screen_coords = screen_coords

class HexView:
    def __init__(self, model:HexBoard, screen_size=600):
        self.model = model
        self.screen_size = screen_size
        self.cell_size = int(screen_size // model.size // PROPORTION)
        self.view_hex_matrix = get_view_hex_matrix(self.model, self.screen_size, self.cell_size)
        pygame.init()
        self.screen = pygame.display.set_mode((screen_size, screen_size))
        self.colors = {1: (255, 0, 0), 2: (0, 0, 255)}  # 1: Red, 2:Blue

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.line(self.screen, self.colors[1], RL_PS[0][0], RL_PS[0][1], 5)
        pygame.draw.line(self.screen, self.colors[1], RL_PS[1][0], RL_PS[1][1], 5)
        pygame.draw.line(self.screen, self.colors[2], BL_PS[0][0], BL_PS[0][1], 5)
        pygame.draw.line(self.screen, self.colors[2], BL_PS[1][0], BL_PS[1][1], 5)


        for row in self.view_hex_matrix:
            for hex in row:
                hex_:HexCell = hex
                x_screen = hex_.screen_coords[0]
                y_screen = hex_.screen_coords[1]
                vertices = get_hex_vertices((x_screen,y_screen), self.cell_size // 2)

                pygame.draw.polygon(self.screen, (0,0,0), vertices, 1)

                x_model = hex_.model_coords[0]
                y_model = hex_.model_coords[1]
                if self.model.board[x_model][y_model]:
                    ratio = self.cell_size // 2 - self.cell_size // 10
                    token_vertices = get_hex_vertices((x_screen,y_screen), ratio)
                    pygame.draw.polygon(self.screen, (self.colors[self.model.board[x_model][y_model]]), token_vertices, 0)

        pygame.display.flip()

    def handle_click(self, pos):
        cell_clicked:HexCell = get_cell_clicked(self.view_hex_matrix, self.model.size, self.screen_size, pos)
        row = cell_clicked.model_coords[0]
        col = cell_clicked.model_coords[1]
        if self.model.place_piece(row, col, self.model.current_player):
            self.draw_board()
            if self.model.check_connection(self.model.current_player):
                self.model.current_player
                print(f"jugador {self.model.get_not_cuurent_player()} ha ganado")
                pygame.quit()
                exit()

    def run(self):
        running = True
        self.draw_board()
        while(running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
        pygame.quit()

    




















def get_hex_vertices(center, ratio):
    x, y = center
    vertices = []
    for i in range(6):
        angle = 2 * math.pi / 6*i
        vertice_x = int(x + ratio * math.sin(angle))
        vertice_y = int(y + ratio * math.cos(angle))
        vertices.append((vertice_x, vertice_y))
    return vertices


def get_view_hex_matrix(model_board:HexBoard, screen_size, cell_size):
    result = []
    count = 1
    multiplier = 1

    size = model_board.size
    minor_diagonal_long = int(screen_size // PROPORTION)
    
    x_init = int(minor_diagonal_long // 2) # para asignarle la posicion en la pantalla
    y = int(cell_size // 2)

    while(count != 0):
                                                                                           
        if multiplier > 0:                                                 #                /\
            hex_file_model_coords = distribute_n_in_n_plus_1_spaces(count) #               /  \
        else:                                                              #               \  /
            hex_file_model_coords = distribute_n_in_n_plus_1_spaces(count, size - count)  # \/
        x = x_init - int((len(hex_file_model_coords)-1) * (cell_size // 2))
        hex_file = [] # fila del rombo que forman las celdas hexagonales
        for model_coords in hex_file_model_coords:
            screen_coords = (x, y)
            if model_coords[0] == 11:
                asd= 1
            hex_cell = HexCell(model_coords, screen_coords)
            hex_file.append(hex_cell)
            x = x + cell_size

        result.append(hex_file)
                                                           # es lo que va avanzando el eje de las Y, ya que si Y divide a hex a la mitad,
        #y = int(y + (math.sqrt(int(cell_size//2) + cell_size))) # de un hexagono a otro a cell_size de dist, y de un hexagono no partido por la mitad por Y a Y hay cell_size de dist 
        y = y + int(math.sqrt(cell_size**2 - int((cell_size//2)**2)))
        if count == size:
            multiplier = multiplier*-1
        count += multiplier
    
    return result


def distribute_n_in_n_plus_1_spaces(n, extra=0):
    if n == 1 and extra == 1:
        return [(0,0)]
    elif n == 1 and extra != 0:
        return [(extra, extra)]
    else:
        points = []
        for i in range(n):
            points.append((n-1-i + extra, i + extra))
        return points
    
def get_cell_clicked(view_hex_matrix, cell_size, screen_size, pos):
    minor_dist = float('inf')
    min_hex = None
    for row in view_hex_matrix:
        for hex in row:
            hex_:HexCell = hex
            point = hex_.screen_coords
            dist = euclidian_dist(point, pos)
            if dist <= minor_dist:
                minor_dist = dist
                min_hex = hex_
    return min_hex


def euclidian_dist(p1, p2):
    result = 0
    for i in range(len(p1)):
        result = result + (p1[i] - p2[i])**2 

    return result