import pygame
import math
from model import HexModel_

class HexView:
    def __init__(self, model:HexModel_.HexModel, screen_size=600):
        self.model = model
        self.screen_size = screen_size
        self.cell_size = screen_size // model.size
        pygame.init()
        self.screen = pygame.display.set_mode((screen_size, screen_size))
        self.colors = {'Red': (255, 0, 0), 'Blue': (0, 0, 255)}

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        for row in range(self.model.size):
            for col in range(self.model.size):
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2
                vertices = get_hex_vertices((x,y), self.cell_size // 2)

                pygame.draw.polygon(self.screen, (0,0,0), vertices, 1)

                if self.model.board[row][col]:
                    ratio = self.cell_size // 2 - self.cell_size // 10
                    token_vertices = get_hex_vertices((x,y), ratio)
                    pygame.draw.polygon(self.screen, (self.colors[self.model.board[row][col]]), token_vertices, 0)

        pygame.display.flip()

    def handle_click(self, pos):
        row = pos[1] // self.cell_size
        col = pos[0] // self.cell_size
        if self.model.make_move((row, col)):
            self.draw_board()
            if self.model.game_over():
                print(f"jugador {self.model.current_player} ha ganado")
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
        vertice_x = int(x + ratio * math.cos(angle))
        vertice_y = int(y + ratio * math.sin(angle))
        vertices.append((vertice_x, vertice_y))
    return vertices