import pygame
from sys import exit
pygame.init()
screen = pygame.display.set_mode((800 , 600))
pygame.display.set_caption("Defenders vs Zombie")
clock = pygame.time.Clock()
cell_size = 80
row , col = 5 , 9
grid_start_x , grid_start_y = 40 , 100
class Defender:
    def __init__(self , row , col , health , cost , color):
        self.row = row
        self.col = col
        self.health = health
        self.cost = cost
        self.color = color
        self.rect = pygame.Rect((grid_start_x + col * cell_size + 10 , grid_start_y + row * cell_size + 10) , (60 , 60))
    def draw(self , surface):
        pygame.draw.rect(surface , self.color , self.rect)

class Shooter(Defender):
    def __init__(self, row, col):
        super().__init__(row, col, 100 , 100, (0 ,0 ,200))
class Producer(Defender):
    def __init__(self, row, col):
        super().__init__(row, col,80 , 50 ,(230 , 200 , 0) ) 
class Wall(Defender):
    def __init__(self, row, col):
        super().__init__(row, col, 400, 50, (130 , 80 , 30))

defenders = [Shooter(0 , 0) , Producer( 1 , 0) , Wall(1 , 8)]


 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((30 , 30 ,30))
    for i in range(row):
        for j in range(col):
            x = grid_start_x + j * cell_size
            y = grid_start_y + i * cell_size
            cell_rect = pygame.Rect((x, y), (cell_size, cell_size))
            if (i + j) % 2 == 0:
                color = (60, 140, 60)
            else:
                color = (80, 160, 80)
            pygame.draw.rect(screen, color, cell_rect)
            pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)

    for defender in defenders:
        defender.draw(screen)
    pygame.display.update()
    clock.tick(60)


