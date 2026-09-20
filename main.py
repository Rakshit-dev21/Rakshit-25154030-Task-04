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

defenders = []
energy = 150
selected = None
font = pygame.font.Font(None , 30)
small_font = pygame.font.Font(None , 22)
shooter_btn = pygame.Rect((40 , 20) , (100 , 60))
producer_btn = pygame.Rect((150 , 20) , (100 , 60))
wall_btn = pygame.Rect((260 , 20) , (100 , 60))
buttons = [(shooter_btn , 'shooter' , (0 , 0 , 200) , 100) , (producer_btn , 'producer' , (230 , 200 , 0) , 50) , (wall_btn , 'wall' , (130 , 80 , 30) , 50)]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_btn = False
            if event.button == 1:
                for button in buttons:
                    if button[0].collidepoint(event.pos):
                        selected = button[1]
                        clicked_btn = True
                if not clicked_btn:
                    mouse_x , mouse_y = event.pos
                    print(mouse_x , mouse_y)
                    c = (mouse_x - grid_start_x) // cell_size
                    r = (mouse_y - grid_start_y) // cell_size
                    print(r , c)
                    if(0 <= r < row and 0 <= c < col):
                        if selected is not None:
                            occupied = False
                            for d in defenders:
                                if d.row == r and d.col == c:
                                    occupied = True
                                    break
                            if not occupied:
                                new_defender = None
                                if selected == 'shooter':
                                    new_defender = Shooter(r , c)
                                elif selected == 'producer':
                                    new_defender = Producer(r , c)
                                elif selected == 'wall':
                                    new_defender = Wall(r , c)

                                if new_defender is not None and energy >= new_defender.cost:
                                    defenders.append(new_defender)
                                    energy -= new_defender.cost


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

    for button in buttons:
        pygame.draw.rect(screen , button[2] , button[0])
        if selected == button[1]:
            pygame.draw.rect(screen , (255 , 255 , 255) , button[0] , 4)
        text = small_font.render(f"{button[1]} : {button[3]}" , True , (255 ,255 , 255))
        screen.blit(text , (button[0].x + 5 , button[0].y + 20))
        

    text_surface = font.render(f" Energy : {energy}" , True , (255 , 255 , 255))
    screen.blit(text_surface , (600 , 40))
    pygame.display.update()
    clock.tick(60)


