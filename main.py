import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Defenders vs Zombie")
clock = pygame.time.Clock()

cell_size = 80
row, col = 6, 9
grid_start_x, grid_start_y = 40, 100

bg_img = pygame.image.load('assets/background.png').convert()
pea_img = pygame.image.load('assets/pea.png').convert_alpha()

shooter_frames = [
    pygame.image.load('assets/shooter_idle_0.png').convert_alpha(),
    pygame.image.load('assets/shooter_shoot_1.png').convert_alpha()
]
producer_frames = [
    pygame.image.load('assets/producer_idle_0.png').convert_alpha(),
    pygame.image.load('assets/producer_produce_1.png').convert_alpha()
]
wall_healthy = pygame.image.load('assets/wall_healthy.png').convert_alpha()
wall_damaged = pygame.image.load('assets/wall_damaged.png').convert_alpha()

zombie_walk = [
    pygame.image.load('assets/zombie_walk_0.png').convert_alpha(),
    pygame.image.load('assets/zombie_walk_1.png').convert_alpha()
]
zombie_eat = [
    pygame.image.load('assets/zombie_eat_0.png').convert_alpha(),
    pygame.image.load('assets/zombie_eat_1.png').convert_alpha()
]

btn_shooter_img = pygame.image.load('assets/btn_shooter.png').convert_alpha()
btn_producer_img = pygame.image.load('assets/btn_producer.png').convert_alpha()
btn_wall_img = pygame.image.load('assets/btn_wall.png').convert_alpha()
score = 0
try:
    with open('high_score.txt', 'r') as f:
        highScore = int(f.read().strip())
except:
    highScore = 0

class Defender:
    def __init__(self, row, col, health, cost):
        self.row = row
        self.col = col
        self.health = health
        self.cost = cost
        self.rect = pygame.Rect((grid_start_x + col * cell_size + 10, grid_start_y + row * cell_size + 10), (60, 60))

class Shooter(Defender):
    def __init__(self, row, col):
        super().__init__(row, col, 100, 100)
        self.shooter_timer = 0

    def shoot(self, zombies, bullets):
        self.shooter_timer += 1
        target = False
        for zombie in zombies:
            if zombie.row == self.row and zombie.rect.x >= self.rect.x and zombie.rect.x < 800:
                target = True
        if self.shooter_timer >= 90 and target == True:
            self.shooter_timer = 0
            bullets.append(Bullet(self.rect.right - 5, self.rect.centery - 8, self.row))

    def draw(self, surface):
        if self.shooter_timer > 80:
            surface.blit(shooter_frames[1], self.rect)
        else:
            surface.blit(shooter_frames[0], self.rect)

class Producer(Defender):
    def __init__(self, row, col):
        super().__init__(row, col, 80, 50)
        self.produce_timer = 0

    def produce(self):
        self.produce_timer += 1
        if self.produce_timer >= 480:
            self.produce_timer = 0
            return 25
        else:
            return 0

    def draw(self, surface):
        if self.produce_timer > 420:
            surface.blit(producer_frames[1], self.rect)
        else:
            surface.blit(producer_frames[0], self.rect)

class Wall(Defender):
    def __init__(self, row, col):
        super().__init__(row, col, 400, 50)

    def draw(self, surface):
        if self.health < 200:
            surface.blit(wall_damaged, self.rect)
        else:
            surface.blit(wall_healthy, self.rect)

class Zombie:
    def __init__(self, row):
        self.row = row
        self.health = 100
        self.speed = 0.3
        self.x = 800.0
        self.rect = pygame.Rect((800, grid_start_y + row * cell_size + 10), (40, 60))
        self.state = 'walking'
        self.eat_timer = 0

    def update(self):
        self.x -= self.speed
        self.rect.x = int(self.x)

    def draw(self, surface):
        if self.state == 'eating':
            idx = (pygame.time.get_ticks() // 200) % len(zombie_eat)
            surface.blit(zombie_eat[idx], self.rect)
        else:
            idx = (pygame.time.get_ticks() // 300) % len(zombie_walk)
            surface.blit(zombie_walk[idx], self.rect)

class Bullet:
    def __init__(self, x, y, row):
        self.row = row 
        self.x = x
        self.y = y
        self.speed = 5
        self.damage = 20
        self.rect = pygame.Rect((self.x, self.y), (16, 16))

    def update(self):
        self.x += self.speed
        self.rect.x = self.x 

    def draw(self, surface):
        surface.blit(pea_img, self.rect)

defenders = []
bullets = []
energy = 150
selected = None

font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 22)
big_font = pygame.font.Font(None, 50)

shooter_btn = pygame.Rect((40, 15), (100, 60))
producer_btn = pygame.Rect((150, 15), (100, 60))
wall_btn = pygame.Rect((260, 15), (100, 60))

buttons = [
    (shooter_btn, 'shooter', btn_shooter_img, 100),
    (producer_btn, 'producer', btn_producer_img, 50),
    (wall_btn, 'wall', btn_wall_img, 50)
]

zombies = []
spawn_timer = 0
spawn_interval = 400
state = 'start'
zombie_spawned = 0
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
                    mouse_x, mouse_y = event.pos
                    c = (mouse_x - grid_start_x) // cell_size
                    r = (mouse_y - grid_start_y) // cell_size
                    if 0 <= r < row and 0 <= c < col:
                        if selected is not None:
                            occupied = False
                            for d in defenders:
                                if d.row == r and d.col == c:
                                    occupied = True
                                    break
                            if not occupied:
                                new_defender = None
                                if selected == 'shooter':
                                    new_defender = Shooter(r, c)
                                elif selected == 'producer':
                                    new_defender = Producer(r, c)
                                elif selected == 'wall':
                                    new_defender = Wall(r, c)

                                if new_defender is not None and energy >= new_defender.cost:
                                    defenders.append(new_defender)
                                    energy -= new_defender.cost
        elif event.type == pygame.KEYDOWN:
            if state == 'start' and event.key == pygame.K_SPACE:
                state = 'playing'
            if state == 'lose' and event.key == pygame.K_SPACE:
                state = 'playing'
                defenders = []
                bullets = []
                zombies = []
                energy = 150
                spawn_timer = 0
                score = 0
                spawn_interval = 400
                selected = None
    if state == 'start':
        screen.fill((0, 0, 0))
        
        title_surf = big_font.render("DEFENDERS VS ZOMBIES", True, (80, 220, 80))
        title_rect = title_surf.get_rect(center=(400, 240))
        
        start_surf = font.render("Press SPACE to Start", True, (255, 255, 255))
        start_rect = start_surf.get_rect(center=(400, 320))
        
        highScore_text = small_font.render(f"High Score: {highScore}", True, (255, 215, 0))
        highscore_rect = highScore_text.get_rect(center=(400, 380))
        
        screen.blit(title_surf, title_rect)
        screen.blit(start_surf, start_rect)
        screen.blit(highScore_text, highscore_rect)

    else:
        if state == 'playing':
            score += 1
            spawn_timer += 1        
            if spawn_timer >= spawn_interval:
                spawn_interval = max(33, spawn_interval - 15)
                spawn_timer = 0
                zombies.append(Zombie(random.randint(0, row - 1)))

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
                if isinstance(d, Shooter):
                    d.shoot(zombies, bullets)
                if isinstance(d, Producer):
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
            defenders = [d for d in defenders if d.health > 0]

            for z in zombies:
                if z.rect.x < grid_start_x:
                    state = 'lose'

        screen.blit(bg_img, (0, 0))

        for defender in defenders:
            defender.draw(screen)

        for zombie in zombies:
            zombie.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        for button in buttons:
            screen.blit(button[2], button[0])
            if selected == button[1]:
                pygame.draw.rect(screen, (255, 255, 255), button[0], 3, border_radius=4)
            cost_txt = small_font.render(str(button[3]), True, (255, 255, 255))
            screen.blit(cost_txt, (button[0].right - cost_txt.get_width() - 8, button[0].bottom - cost_txt.get_height() - 4))

        text_surface = font.render(f"Energy : {energy}", True, (255, 255, 255))
        screen.blit(text_surface, (600, 30))

        if state == 'lose':
            highScore = max(score//60 , highScore)
            with open('high_score.txt', 'w') as f:
                f.write(str(highScore))
            lose_text = big_font.render("YOU LOSE", True, (255, 0, 0))
            lose_rect = lose_text.get_rect(center=(400, 300))

            Score_text = font.render(f"Score :{score//60}", True, (255, 255, 255))

            highScore_text = font.render(f"high Score : {highScore}", True, (255, 255, 255))

            restart_text = font.render("press Space to restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(400, 360))

            screen.blit(Score_text , (400 , 55))
            screen.blit(highScore_text , (600 , 55))
            screen.blit(lose_text, lose_rect)
            screen.blit(restart_text, restart_rect)

    pygame.display.update()
    clock.tick(60)