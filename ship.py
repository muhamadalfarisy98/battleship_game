import pygame
import math
import random


game_title = "Simulation of Battleship Radar"

# color
red = (255, 0, 0)
blue_water = (9, 195, 219)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (0, 0, 0)

# bullet
bullets = []
bullet_speed = 15
bullet_radius = 5

# enemy ship
num_enemy_ship = 150
ship_speed = 0.7
enemy_ship_size = 10

# main ship
mainship_radius = 10

# screen size
screen_width = 1000
screen_height = 800

# center
center_x, center_y = screen_width // 2, screen_height // 2

# init pygame
pygame.init()

# radar
radars = [50, 100, 150]

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(game_title)


# Drawer - display drawer
class Drawer:
    def __init__(self) -> None:
        pass

    def draw_score(self, score):
        font = pygame.font.Font(None, 38)
        text = font.render("Score: " + str(score), True, blue)
        screen.blit(text, (10, 15))

    def draw_life(self, score):
        font = pygame.font.Font(None, 38)
        text = font.render("Lifes: " + str(score), True, blue)
        screen.blit(text, (850, 15))

    def draw_message(self, message):
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, red)
        screen.blit(text, (10, 90))

    def draw_instruction_attack(self):
        font = pygame.font.Font(None, 30)
        text = font.render("'Space' for attack", True, green)
        screen.blit(text, (650, 70))

    def draw_instruction_move(self):
        font = pygame.font.Font(None, 30)
        text = font.render("'Left or Right' to move thrower", True, green)
        screen.blit(text, (650, 90))

    def draw_info_enemy_number(self, enemy_number):
        font = pygame.font.Font(None, 30)
        text = font.render("Enemy counted: " + str(enemy_number), True, green)
        screen.blit(text, (10, 70))

    def draw_game_over_screen(self, score):
        screen.fill(white)
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over!", True, green)
        screen.blit(text, (400, 400))
        self.draw_score(score)
        pygame.display.flip()


# MainShip - kapal utama
class MainShip:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = mainship_radius
        self.last_shot_time = 0
        self.color_thrower = red
        self.shoot_delay = 500
        self.angle = 0
        self.radius_collision = 20

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), self.radius)
        pygame.draw.line(
            screen, self.color_thrower, (self.x, self.y), self.calculate_endpoint(), 2
        )

    def calculate_endpoint(self):
        radian_angle = math.radians(self.angle)
        end_x = self.x + self.radius * math.cos(radian_angle)
        end_y = self.y - self.radius * math.sin(radian_angle)
        return end_x, end_y

    def rotate_left(self):
        self.angle += 4

    def rotate_right(self):
        self.angle -= 4

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            bullets.append(Bullet(self.x, self.y, self.angle))
            self.last_shot_time = current_time
        return None

    def check_collision(self, ship):
        distance = math.sqrt(
            (ship.position[0] - self.x) ** 2 + (ship.position[1] - self.y) ** 2
        )
        return distance < self.radius_collision


class Bullet:
    def __init__(self, x, y, angle):
        self.radius = bullet_radius
        self.color = red
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = bullet_speed

    def move(self):
        radian_angle = math.radians(self.angle)
        self.x += self.speed * math.cos(radian_angle)
        self.y -= self.speed * math.sin(radian_angle)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class Enemy:
    def __init__(self, position, angle):
        self.screen = screen
        self.SHIP_COLOR = red
        self.SHIP_SPEED = ship_speed
        self.WIDTH, self.HEIGHT = screen_width, screen_height
        self.RADII = [50, 100, 150, 200, 300]
        self.radius_collision = 10
        self.position = [position[0], position[1]]
        self.angle = angle

    def draw_ship(self):
        ship_x, ship_y = self.position[0], self.position[1]
        pygame.draw.circle(
            self.screen, self.SHIP_COLOR, (int(ship_x), int(ship_y)), enemy_ship_size
        )

    def update_ship_position(self):
        self.position[0] += self.SHIP_SPEED * math.cos(math.radians(self.angle))
        self.position[1] -= self.SHIP_SPEED * math.sin(math.radians(self.angle))

        if self.position[0] < 0:
            self.position[0] = self.WIDTH
        elif self.position[0] > self.WIDTH:
            self.position[0] = 0

        if self.position[1] < 0:
            self.position[1] = self.HEIGHT
        elif self.position[1] > self.HEIGHT:
            self.position[1] = 0

    # check_collision - distance calculated by euclidean distance equation
    def check_collision(self, bullets):
        for bullet in bullets:
            distance = math.sqrt(
                (self.position[0] - bullet.x) ** 2 + (self.position[1] - bullet.y) ** 2
            )
            if distance < self.radius_collision:
                bullets.remove(bullet)
                return True
        return False


# Radar - defines radar class
class Radar:
    def __init__(self):
        self.WIDTH, self.HEIGHT = screen_width, screen_height
        self.BACKGROUND_COLOR = blue_water
        self.RADAR_COLOR = blue
        self.SHIP_COLOR = red
        self.NUM_SHIPS = num_enemy_ship
        self.radars = radars

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

    def draw_radar(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        for radius in self.radars:
            pygame.draw.circle(
                self.screen, self.RADAR_COLOR, (center_x, center_y), radius, 2
            )


if __name__ == "__main__":
    drawer = Drawer()
    radar = Radar()
    main_ship = MainShip(center_x, center_y)
    enemy_ships = [
        Enemy(
            [
                random.uniform(0, screen_width),
                random.uniform(0, screen_height),
            ],
            random.uniform(0, 360),
        )
        for _ in range(num_enemy_ship)
    ]

    running = True
    score = 0
    live = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_ship.shoot()

        radar.draw_radar()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            main_ship.rotate_left()
        if keys[pygame.K_RIGHT]:
            main_ship.rotate_right()

        # set bullet
        for bullet in bullets:
            bullet.move()
            bullet.draw()

        counted_ship = 0

        # enemy ship
        for ship in enemy_ships:
            ship.update_ship_position()
            distance_from_center = math.sqrt(
                (ship.position[0] - center_x) ** 2 + (ship.position[1] - center_y) ** 2
            )

            if distance_from_center <= ship.RADII[-1]:
                ship.draw_ship()

            if distance_from_center <= ship.RADII[0]:
                if main_ship.check_collision(ship):
                    enemy_ships.remove(ship)
                    live -= 1
                    continue

            if distance_from_center <= ship.RADII[-3]:
                counted_ship += 1
                if ship.check_collision(bullets):
                    score += 1
                    enemy_ships.remove(ship)

        # main ship
        main_ship.draw(radar.screen)

        # set score
        drawer.draw_score(score)

        # set live
        drawer.draw_life(live)

        # set detection
        drawer.draw_info_enemy_number(counted_ship)

        # set instruction
        drawer.draw_instruction_attack()
        drawer.draw_instruction_move()

        #  game over screen
        if live <= 0:
            drawer.draw_game_over_screen(score)

        pygame.display.flip()
        radar.clock.tick(20)

    pygame.quit()
