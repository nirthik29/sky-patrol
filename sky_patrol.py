import math
import random
import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 600
FPS = 60
GROUND_Y = 505

SKY = (119, 190, 232)
WHITE = (245, 248, 250)
DARK = (35, 48, 61)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sky Patrol")

clock = pygame.time.Clock()

font = pygame.font.SysFont("verdana", 20, bold=True)
small_font = pygame.font.SysFont("verdana", 14)
big_font = pygame.font.SysFont("verdana", 42, bold=True)


def draw_text(surface, text, x, y, colour=WHITE, use_font=font):
    image = use_font.render(text, True, colour)
    surface.blit(image, (x, y))


# ==============================
# PLAYER AIRCRAFT
# ==============================

class Plane:

    def __init__(self):
        self.x = 145
        self.y = HEIGHT // 2
        self.speed = 5
        self.cooldown = 0

        self.rect = pygame.Rect(
            self.x - 48,
            self.y - 19,
            100,
            38
        )

    def update(self, keys):

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.y = max(65, min(GROUND_Y - 55, self.y))

        self.rect.center = (self.x, self.y)

        if self.cooldown:
            self.cooldown -= 1

    def draw(self, surface):

        x, y = self.x, self.y

        pygame.draw.polygon(
            surface, (175, 190, 199),
            [
                (x-43, y-5),
                (x-65, y-25),
                (x-55, y+5),
                (x-34, y+8)
            ]
        )

        pygame.draw.polygon(
            surface, (205, 215, 220),
            [
                (x-38, y+4),
                (x-57, y+23),
                (x-18, y+12)
            ]
        )

        pygame.draw.polygon(
            surface, (165, 181, 190),
            [
                (x-12, y-4),
                (x+10, y-47),
                (x+27, y-45),
                (x+19, y-4),
                (x+39, y+8),
                (x+16, y+13)
            ]
        )

        pygame.draw.polygon(
            surface, (194, 207, 213),
            [
                (x-15, y+5),
                (x+15, y+10),
                (x+39, y+44),
                (x+17, y+39),
                (x-29, y+11)
            ]
        )

        pygame.draw.ellipse(
            surface, (224, 231, 233),
            (x-53, y-12, 105, 25)
        )

        pygame.draw.polygon(
            surface, (232, 238, 240),
            [
                (x+40, y-10),
                (x+62, y),
                (x+40, y+10)
            ]
        )

        # Cockpit

        pygame.draw.ellipse(
            surface, (55, 104, 137),
            (x+2, y-9, 23, 13)
        )

        pygame.draw.ellipse(
            surface, (133, 196, 222),
            (x+6, y-8, 12, 5)
        )

        pygame.draw.line(
            surface, (105, 121, 130),
            (x-32, y), (x+30, y), 2
        )

        pygame.draw.circle(
            surface, (90, 102, 110),
            (x-48, y+1), 5
        )

        pygame.draw.line(
            surface, (190, 48, 43),
            (x-5, y-28), (x+15, y-17), 4
        )

        pygame.draw.line(
            surface, (190, 48, 43),
            (x-5, y+26), (x+15, y+17), 4
        )

    def fire(self):

        if self.cooldown == 0:

            self.cooldown = 16

            return Bullet(
                self.x + 57,
                self.y - 2
            )

        return None


# ==============================
# BULLETS
# ==============================

class Bullet:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.rect = pygame.Rect(x, y, 18, 5)

    def update(self):

        self.x += 11

        self.rect.x = int(self.x)

    def draw(self, surface):

        pygame.draw.ellipse(
            surface, (255, 224, 105),
            self.rect
        )

        pygame.draw.line(
            surface, (255, 250, 190),
            (self.rect.left - 8, self.rect.centery),
            (self.rect.left, self.rect.centery), 2
        )


# ==============================
# HUMAN OBSTACLES
# ==============================

class Person:

    OUTFITS = [
        ((35, 89, 160), (235, 194, 150)),
        ((170, 57, 65), (190, 135, 95)),
        ((54, 130, 91), (232, 188, 145)),
        ((117, 78, 151), (205, 158, 119)),
        ((224, 145, 44), (225, 180, 137))
    ]

    def __init__(self, x):

        self.x = x
        self.y = GROUND_Y - 31

        self.outfit, self.skin = random.choice(self.OUTFITS)

        self.phase = random.random() * 6

        self.rect = pygame.Rect(
            x - 11,
            self.y - 27,
            22,
            55
        )

    def update(self, speed):

        self.x -= speed
        self.phase += 0.16

        self.rect.centerx = int(self.x)

    def draw(self, surface):

        x = int(self.x)
        y = int(self.y)

        swing = int(math.sin(self.phase) * 4)

        # Legs

        pygame.draw.line(
            surface, (45, 48, 55),
            (x-4, y+10),
            (x-7+swing, y+27), 5
        )

        pygame.draw.line(
            surface, (45, 48, 55),
            (x+4, y+10),
            (x+7-swing, y+27), 5
        )

        # Body

        pygame.draw.rect(
            surface, self.outfit,
            (x-8, y-13, 16, 27),
            border_radius=4
        )

        # Arms

        pygame.draw.line(
            surface, self.skin,
            (x-7, y-8),
            (x-13-swing, y+5), 4
        )

        pygame.draw.line(
            surface, self.skin,
            (x+7, y-8),
            (x+13+swing, y+4), 4
        )

        # Head

        pygame.draw.circle(
            surface, self.skin,
            (x, y-21), 8
        )

        pygame.draw.arc(
            surface, (55, 40, 32),
            (x-8, y-29, 16, 14),
            0, math.pi, 3
        )


# ==============================
# TANKER
# ==============================

class Tanker:

    def __init__(self, x):

        self.x = x
        self.y = GROUND_Y - 25

        self.rect = pygame.Rect(
            x-48, self.y-24, 96, 48
        )

    def update(self, speed):

        self.x -= speed

        self.rect.x = int(self.x - 48)

    def draw(self, surface):

        x = int(self.x)
        y = int(self.y)

        pygame.draw.rect(
            surface, (196, 205, 207),
            (x-43, y-23, 72, 29),
            border_radius=8
        )

        pygame.draw.rect(
            surface, (52, 105, 145),
            (x+26, y-17, 25, 23),
            border_radius=4
        )

        pygame.draw.polygon(
            surface, (119, 173, 197),
            [
                (x+30, y-16),
                (x+46, y-16),
                (x+48, y-5),
                (x+30, y-5)
            ]
        )

        pygame.draw.line(
            surface, (232, 163, 55),
            (x-39, y-9),
            (x+25, y-9), 4
        )

        for wx in (x-28, x+5, x+39):

            pygame.draw.circle(
                surface, (38, 42, 46),
                (wx, y+8), 9
            )

            pygame.draw.circle(
                surface, (160, 166, 169),
                (wx, y+8), 4
            )

        pygame.draw.rect(
            surface, (80, 88, 92),
            (x-50, y+4, 9, 5)
        )


# ==============================
# TREES
# ==============================

class Tree:

    def __init__(self, x):

        self.x = x

        self.height = random.randint(65, 105)
        self.width = random.randint(34, 49)

        self.rect = pygame.Rect(
            int(self.x - self.width // 2),
            int(GROUND_Y - self.height - self.width // 2),
            self.width,
            self.height + self.width // 2
        )

    def update(self, speed):

        self.x -= speed

        self.rect.x = int(
            self.x - self.width // 2
        )

    def draw(self, surface):

        x = int(self.x)

        pygame.draw.rect(
            surface, (105, 72, 47),
            (
                x-5,
                GROUND_Y-self.height//2,
                10,
                self.height//2
            )
        )

        pygame.draw.circle(
            surface, (43, 119, 68),
            (x, GROUND_Y-self.height),
            self.width//2
        )

        pygame.draw.circle(
            surface, (55, 145, 77),
            (x-13, GROUND_Y-self.height+12),
            self.width//3
        )

        pygame.draw.circle(
            surface, (35, 105, 61),
            (x+14, GROUND_Y-self.height+13),
            self.width//3
        )


# ==============================
# MOVING BIRDS
# ==============================

class Bird:

    def __init__(self, x):

        self.x = x

        self.base_y = random.randint(95, 300)

        self.phase = random.random() * 6

        self.speed = random.uniform(2.2, 3.4)

        self.rect = pygame.Rect(
            x-13,
            self.base_y-8,
            28,
            16
        )

    def update(self, world_speed):

        self.x -= self.speed + world_speed * 0.35

        self.phase += 0.22

        self.rect.center = (
            int(self.x),
            int(self.base_y + math.sin(self.phase)*13)
        )

    def draw(self, surface):

        x, y = self.rect.center

        flap = int(math.sin(self.phase * 2) * 7)

        pygame.draw.arc(
            surface, DARK,
            (x-12, y-7-flap, 13, 12),
            0, math.pi, 2
        )

        pygame.draw.arc(
            surface, DARK,
            (x, y-7-flap, 13, 12),
            0, math.pi, 2
        )


# ==============================
# BACKGROUND
# ==============================

def draw_background(surface, offset):

    surface.fill(SKY)

    # Clouds

    for i in range(5):

        cx = int(
            (i * 245 - offset * 0.25)
            % (WIDTH + 150)
        ) - 60

        cy = 80 + (i % 3) * 52

        pygame.draw.circle(
            surface, (238, 247, 250),
            (cx, cy), 19
        )

        pygame.draw.circle(
            surface, (238, 247, 250),
            (cx+22, cy-7), 24
        )

        pygame.draw.circle(
            surface, (238, 247, 250),
            (cx+46, cy), 17
        )

    # Hills

    pygame.draw.rect(
        surface, (105, 164, 112),
        (0, 420, WIDTH, 90)
    )

    for i in range(8):

        hx = int(
            (i*190 - offset*0.55)
            % (WIDTH+220)
        ) - 100

        pygame.draw.ellipse(
            surface, (83, 147, 99),
            (hx, 375, 230, 100)
        )

    # Ground

    pygame.draw.rect(
        surface, (84, 143, 74),
        (0, GROUND_Y, WIDTH, HEIGHT-GROUND_Y)
    )

    pygame.draw.line(
        surface, (220, 211, 153),
        (0, GROUND_Y),
        (WIDTH, GROUND_Y), 4
    )


# ==============================
# RESET GAME
# ==============================

def reset_game():

    return {
        "plane": Plane(),
        "bullets": [],
        "people": [],
        "tankers": [],
        "trees": [],
        "birds": [],
        "score": 0,
        "lives": 3,
        "world_speed": 4,
        "spawn": 0,
        "background_offset": 0,
        "paused": False,
        "game_over": False
    }


# ==============================
# MAIN GAME LOOP
# ==============================

game = reset_game()

running = True

while running:

    dt = clock.tick(FPS)

    keys = pygame.key.get_pressed()

    # Event handling

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

            elif event.key == pygame.K_p and not game["game_over"]:

                game["paused"] = not game["paused"]

            elif event.key == pygame.K_r and game["game_over"]:

                game = reset_game()

    # Game updates

    if not game["paused"] and not game["game_over"]:

        plane = game["plane"]

        plane.update(keys)

        # Shooting

        if keys[pygame.K_SPACE]:

            shot = plane.fire()

            if shot:

                game["bullets"].append(shot)

        # Spawn obstacles

        game["spawn"] += 1

        if game["spawn"] > 62:

            game["spawn"] = 0

            roll = random.random()

            if roll < 0.34:

                game["people"].append(
                    Person(WIDTH + 30)
                )

            elif roll < 0.54:

                game["tankers"].append(
                    Tanker(WIDTH + 65)
                )

            elif roll < 0.80:

                game["trees"].append(
                    Tree(WIDTH + 20)
                )

            else:

                game["birds"].append(
                    Bird(WIDTH + 25)
                )

        game["background_offset"] += game["world_speed"]

        # Bullet movement

        for item in game["bullets"]:

            item.update()

        game["bullets"] = [
            b for b in game["bullets"]
            if b.x < WIDTH + 30
        ]

        # Obstacle movement

        for group in (
            "people",
            "tankers",
            "trees",
            "birds"
        ):

            for item in game[group]:

                item.update(game["world_speed"])

        # Collision detection

        for group in (
            "people",
            "tankers",
            "trees",
            "birds"
        ):

            for obstacle in game[group][:]:

                if plane.rect.colliderect(obstacle.rect):

                    game[group].remove(obstacle)

                    game["lives"] -= 1

                    if game["lives"] <= 0:

                        game["game_over"] = True

        # Bullets hit tankers, not people

        for bullet in game["bullets"][:]:

            hit = False

            for obstacle in game["tankers"][:]:

                if bullet.rect.colliderect(obstacle.rect):

                    game["tankers"].remove(obstacle)

                    hit = True

                    game["score"] += 10

                    break

            if hit and bullet in game["bullets"]:

                game["bullets"].remove(bullet)

        # Remove objects outside screen

        for group in (
            "people",
            "tankers",
            "trees",
            "birds"
        ):

            game[group] = [
                obj for obj in game[group]
                if obj.x > -120
            ]

        game["score"] += 1

        game["world_speed"] = min(
            7,
            4 + game["score"] // 900
        )

    # ==============================
    # DRAW EVERYTHING
    # ==============================

    draw_background(
        screen,
        game["background_offset"]
    )

    for tree in game["trees"]:

        tree.draw(screen)

    for person in game["people"]:

        person.draw(screen)

    for tanker in game["tankers"]:

        tanker.draw(screen)

    for bird in game["birds"]:

        bird.draw(screen)

    for bullet in game["bullets"]:

        bullet.draw(screen)

    game["plane"].draw(screen)

    # Scoreboard

    pygame.draw.rect(
        screen, (28, 45, 58),
        (0, 0, WIDTH, 43)
    )

    draw_text(
        screen,
        f"SCORE  {game['score']}",
        18, 10
    )

    draw_text(
        screen,
        f"LIVES  {game['lives']}",
        210, 10
    )

    draw_text(
        screen,
        "W/S or arrows: fly    SPACE: fire    P: pause",
        385, 12,
        (222, 232, 238),
        small_font
    )

    # Pause screen

    if game["paused"]:

        label = big_font.render(
            "PAUSED", True, WHITE
        )

        screen.blit(
            label,
            label.get_rect(
                center=(WIDTH//2, HEIGHT//2)
            )
        )

    # Game over screen

    if game["game_over"]:

        shade = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        shade.fill((8, 18, 28, 175))

        screen.blit(shade, (0, 0))

        title = big_font.render(
            "FLIGHT ENDED",
            True,
            WHITE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH//2, HEIGHT//2 - 35)
            )
        )

        draw_text(
            screen,
            f"Final score: {game['score']}",
            WIDTH//2 - 90,
            HEIGHT//2 + 12
        )

        draw_text(
            screen,
            "Press R to play again  |  ESC to quit",
            WIDTH//2 - 190,
            HEIGHT//2 + 52,
            WHITE,
            small_font
        )

    pygame.display.flip()


# ==============================
# EXIT
# ==============================

pygame.quit()
sys.exit()