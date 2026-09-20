import pygame
import random
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
        self.shooter_timer = 0
    def shoot(self , zombies , bullets):
        self.shooter_timer += 1
        target = False
        for zombie in zombies:
            if zombie.row == self.row and zombie.rect.x >= self.rect.x and zombie.rect.x < 800:
                target = True
        if self.shooter_timer >= 90 and target == True:
            self.shooter_timer = 0
            bullets.append(Bullet(self.rect.right , self.rect.centery - 4 , self.row))

class Producer(Defender):
    def __init__(self, row, col):
        super().__init__(row, col,80 , 50 ,(230 , 200 , 0) ) 
        self.produce_timer = 0
    def produce(self):
        self.produce_timer += 1
        if self.produce_timer >= 480:
            self.produce_timer = 0
            return 25
        else:return 0

class Wall(Defender):
    def __init__(self, row, col):
        super().__init__(row, col, 400, 50, (130 , 80 , 30))

class Zombie:
    def __init__(self , row):
        self.row = row
        self.health = 100
        self.speed = 0.3
        self.x = 800
        self.rect = pygame.Rect((800 , grid_start_y + row * cell_size + 10) , (40 , 60))
        self.state = 'walking'
        self.eat_timer = 0
    def update(self):
        self.x -= self.speed
        self.rect.x = self.x
    def draw(self , surface):
        pygame.draw.rect(surface , (200 , 40 , 40) , self.rect)
class Bullet:
    def __init__(self , x , y , row):
        self.row = row 
        self.x = x
        self.y = y
        self.speed = 5
        self.damage = 20
        self.rect = pygame.Rect((self.x , self.y) , (15 , 8))
    def update(self):
        self.x += self.speed
        self.rect.x = self.x 
    def draw(self , surface):
        pygame.draw.rect(surface , (244 , 196 , 48) , self.rect)
defenders = []
bullets = []
energy = 150
selected = None
font = pygame.font.Font(None , 30)
small_font = pygame.font.Font(None , 22)
big_font = pygame.font.Font(None , 50)
shooter_btn = pygame.Rect((40 , 20) , (100 , 60))
producer_btn = pygame.Rect((150 , 20) , (100 , 60))
wall_btn = pygame.Rect((260 , 20) , (100 , 60))
buttons = [(shooter_btn , 'shooter' , (0 , 0 , 200) , 100) , (producer_btn , 'producer' , (230 , 200 , 0) , 50) , (wall_btn , 'wall' , (130 , 80 , 30) , 50)]
zombies = []
spawn_timer = 0
spawn_interval = 400
state = 'playing'
zombie_spawned = 0
total_zombie = 15
running = True
while running:
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and state == 'playing':
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
                elif event.type == pygame.KEYDOWN:
                    if state == 'lose' and event.key == pygame.K_SPACE:
                        state = 'playing'
                        defenders = []
                        bullets = []
                        zombies = []
                        energy = 150 
                        spawn_timer = 0
                        spawn_interval = 400
                        selected = None
    if state == 'playing':
        spawn_timer += 1
        if spawn_timer >= spawn_interval :
            spawn_timer = 0
            zombies.append(Zombie(random.randint(0 , row - 1)))
        for zombie in zombies:
            target = None
            for d in defenders:
                if d.row == zombie.row and zombie.rect.colliderect(d.rect):
                    target = d
            if target != None:
                zombie.state = 'eating'
                zombie.eat_timer += 1
                if zombie.eat_timer >= 30:
                    target.health -= 10
                    zombie.eat_timer = 0
            else:
                    zombie.state = 'walking'
                    zombie.update()   

        for d in defenders:
            if isinstance(d , Shooter):
                d.shoot(zombies , bullets)
            if isinstance(d , Producer):
                energy += d.produce()
        

        for bullet in bullets:
            bullet.update()
        for b in bullets[:]:
            for z in zombies:
                if b.row == z.row and b.rect.colliderect(z.rect):
                    z.health = z.health - b.damage
                    bullets.remove(b)
                    break
        bullets = [b for b in bullets if b.rect.x < 800]
        zombies = [z for z in zombies if z.health > 0]
        defenders = [d for d in defenders if d.health > 0 ]
        for z in zombies:
            if z.rect.x < grid_start_x:
                state = 'lose'
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

    for zombie in zombies:
        zombie.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for button in buttons:
        pygame.draw.rect(screen , button[2] , button[0])
        if selected == button[1]:
            pygame.draw.rect(screen , (255 , 255 , 255) , button[0] , 4)
        text = small_font.render(f"{button[1]} : {button[3]}" , True , (255 ,255 , 255))
        screen.blit(text , (button[0].x + 5 , button[0].y + 20))
        

    text_surface = font.render(f" Energy : {energy}" , True , (255 , 255 , 255))
    screen.blit(text_surface , (600 , 40))
    if state == 'lose':
        lose_text = big_font.render("YOU LOSE" , True , (255 , 0 , 0))
        lose_rect = lose_text.get_rect(center = (400 , 300))
        restart_text = font.render("press Space to restart" ,True , (255 , 255 , 255))
        restart_rect = restart_text.get_rect(center = (400 , 360))
        screen.blit(lose_text , lose_rect)
        screen.blit(restart_text , restart_rect)
    pygame.display.update()
    clock.tick(60)


