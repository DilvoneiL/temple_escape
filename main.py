import random
import math
from pygame import Rect




STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_WIN = "win"
game_state = STATE_MENU

music_on = True
sfx_on = True

mouse_pos = (0, 0)

relics = []
relics_collected = 0
enemies = []
walls = []
bushes = []

# --- CONFIGURAÇÕES ---
TILE_SIZE = 32
WIDTH = 30 * TILE_SIZE  # 960
HEIGHT = 20 * TILE_SIZE # 640

TILE_TYPES = {
    1: "wall",
    0: "ground",
    "R": "relic",
    "B": "bush",
    "E": "enemy",
    "P": "player",
    "D": "door",   
}

# Mapa base cercado de paredes
MAP_GRID = []
for row in range(20):
    line = []
    for col in range(30):
        if row == 0 or row == 19 or col == 0 or col == 29:
            line.append(1)
        else:
            line.append(0)
    MAP_GRID.append(line)

def add_room(x1, y1, x2, y2):
    """Cria uma sala retangular com parede 1 tile de espessura."""
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if x == x1 or x == x2 or y == y1 or y == y2:
                MAP_GRID[y][x] = 1
            else:
                MAP_GRID[y][x] = 0

# -------------------------
# 3 SALAS + CORREDORES
# -------------------------

# Sala 1 (top-left)
add_room(2, 2, 10, 7)

# Sala 2 (top-right)
add_room(19, 2, 27, 7)

# Sala 3 (bottom-middle)
add_room(11, 12, 18, 17)

# Corredor horizontal central
for x in range(1, 29):
    MAP_GRID[9][x] = 0

# Corredor vertical até sala 3
for y in range(9, 18):
    MAP_GRID[y][14] = 0

# Aberturas (portas internas) para conectar as salas ao corredor
MAP_GRID[5][10] = 0   # abertura Sala 1 (parede direita)
MAP_GRID[6][10] = 0   # abertura Sala 1 (parede direita)
MAP_GRID[5][19] = 0   # abertura Sala 2 (parede esquerda)
MAP_GRID[5][20] = 0   # abertura Sala 2 (parede esquerda)
MAP_GRID[12][14] = 0  # abertura Sala 3 (parede de cima)
MAP_GRID[12][15] = 0  # abertura Sala 3 (parede de cima)


# -------------------------
# ENTIDADES (1 relic + 1 enemy por sala)
# -------------------------

# Player (começa no corredor)
MAP_GRID[9][2] = "P"

# Sala 1: enemy guardando relic
MAP_GRID[4][6] = "E"
MAP_GRID[6][8] = "R"

# Sala 2: enemy guardando relic
MAP_GRID[4][23] = "E"
MAP_GRID[6][21] = "R"

# Sala 3: enemy guardando relic
MAP_GRID[14][16] = "E"
MAP_GRID[16][12] = "R"

# Bushes (opcional, pra stealth)
MAP_GRID[4][4] = "B"
MAP_GRID[6][24] = "B"
MAP_GRID[15][13] = "B"
MAP_GRID[15][15] = "B"

# Porta de saída na borda direita (substitui a parede)
MAP_GRID[9][29] = "D"

def draw_ground():
    for y, row in enumerate(MAP_GRID):
        for x, _ in enumerate(row):  # percorre todos os tiles
            screen.blit("ground", (x * TILE_SIZE, y * TILE_SIZE))




def load_map():
    global walls, relics, bushes, door, player, enemies
    walls = []
    relics = []
    bushes = []
    enemies = []
    door = None
    player = None

    for y, row in enumerate(MAP_GRID):
        for x, tile in enumerate(row):
            pos = (x * TILE_SIZE, y * TILE_SIZE)

            if tile == 1:
                walls.append(Wall(pos, (TILE_SIZE, TILE_SIZE)))
            elif tile == "R":
                relics.append(Relic(pos))
            elif tile == "B":
                bushes.append(Bush(pos))
            elif tile == "E":
                enemies.append(Enemy(pos, (pos[0] + TILE_SIZE * 3, pos[1])))
            elif tile == "D" and door is None:
                door = ExitDoor(pos)
            elif tile == "P":
                player = Player(pos)

    # Garante que o player exista
    if player is None:
        player = Player((TILE_SIZE * 2, TILE_SIZE * 2))


class Button:
    def __init__(self, text, pos, callback):
        self.text = text
        self.rect = Rect(pos[0], pos[1], 220, 50)
        self.callback = callback
        self.hover = False

    def draw(self):
        color = "darkgreen" if self.hover else "green"
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(self.text, center=self.rect.center,
                         fontsize=32, color="white")

    def update_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)

    def click(self):
        if self.hover:
            self.callback()


def start_game():
    global game_state, relics_collected, relics, enemies, walls, player, door
    relics_collected = 0
    if music_on:
        try:
            music.play("bgm")
        except:
            print("Erro: bgm.ogg não encontrado na pasta /music")
    

    load_map()
    game_state = STATE_PLAYING


def toggle_audio():
    global music_on, sfx_on
    music_on = not music_on
    sfx_on = not sfx_on
    
    try:
        if music_on:
            music.play("bgm")
        else:
            music.stop()
    except Exception as e:
        print("Erro ao tocar música:", e)


def exit_game():
    exit()

def play_again():
    start_game()

def back_to_menu():
    global game_state
    game_state = STATE_MENU

end_buttons = [
    Button("Play Again", (WIDTH // 2 - 110, HEIGHT // 2 + 40), play_again),
    Button("Back to Menu", (WIDTH // 2 - 110, HEIGHT // 2 + 110), back_to_menu),
    Button("Exit", (WIDTH // 2 - 110, HEIGHT // 2 + 180), exit_game),
]
buttons = [
    Button("Start Game", (WIDTH // 2 - 110, 200), start_game),
    Button("Music / Sound On-Off", (WIDTH // 2 - 110, 280), toggle_audio),
    Button("Exit", (WIDTH // 2 - 110, 360), exit_game),
]

# === Classe Relic ===
class Relic:
    def __init__(self, pos):
        self.pos = pos
        self.collected = False
        self.image = "relic"

    def draw(self):
        if not self.collected:
            screen.blit(self.image, self.pos)
         # DEBUG: desenhar hitbox
        hitbox = Rect(self.pos[0], self.pos[1], 32, 32)
        # screen.draw.rect(hitbox, (255, 255, 0))  # Amarelo

    def check_collision(self, player_rect):
        if not self.collected and player_rect.colliderect(Rect(self.pos[0], self.pos[1], 32, 32)):
            self.collected = True
            global relics_collected
            relics_collected += 1
            if sfx_on:
                sounds.pickup.play()

# === Classe Door ===
class ExitDoor:
    def __init__(self, pos):
        self.pos = pos
        self.image_closed = "door"
        self.image_open = "door_open"
        self.opened = False
        self.rect = Rect(pos[0], pos[1], TILE_SIZE , TILE_SIZE )  # 32x32
    def draw(self):
        if self.opened:
            screen.blit(self.image_open, self.pos)
        else:
            screen.blit(self.image_closed, self.pos)
         # DEBUG: desenhar hitbox da porta (em rosa)
        door_rect = Rect(self.pos[0], self.pos[1], 32, 32)
    def check_collision(self, player_rect):
        if self.opened and player_rect.colliderect(Rect(self.pos[0], self.pos[1], 48, 64)):
            return True
        return False


# === Classe Player ===
class Player:
    def __init__(self, pos):
        self.pos = list(pos)
        self.dest = list(pos)
        self.speed = 2.5
        self.direction = "down"
        self.state = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.anim_speed = 0.15
        self.hidden = False
        self.images = {
            "idle_down": [f"soldier_idle_{i:02}" for i in range(5)],
            "walk_down": [f"soldier_walk_{i:02}" for i in range(7)],
        }

    def update(self):
        dx = self.dest[0] - self.pos[0]
        dy = self.dest[1] - self.pos[1]
        dist = math.hypot(dx, dy)

        previous_state = self.state

        if dist > 2:
            angle = math.atan2(dy, dx)
            self.pos[0] += math.cos(angle) * self.speed
            self.pos[1] += math.sin(angle) * self.speed
            self.state = "walk"
        else:
            self.state = "idle"

        # Resetar o índice se o estado mudar
        if self.state != previous_state:
            self.frame_index = 0

        # Atualizar animação com segurança
        self.frame_timer += self.anim_speed
        current_anim = self.images.get(f"{self.state}_{self.direction}", [])
        if current_anim and self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(current_anim)


    def draw(self):
        key = f"{self.state}_{self.direction}"
        current_anim = self.images.get(key, [])
        if current_anim:
            image = current_anim[self.frame_index]
            screen.blit(image, self.pos)
            if self.hidden:
                screen.surface.set_alpha(100)
                screen.blit(image, self.pos)
                screen.surface.set_alpha(255)
            else:
                screen.blit(image, self.pos)
    def get_rect(self):
         return Rect(self.pos[0] + 38, self.pos[1] + 38, 18, 18)

# === Classe enemy ===
class Enemy:
    def __init__(self, point_a, point_b, vertical=False):
        self.pos = list(point_a)
        self.point_a = list(point_a)
        self.point_b = list(point_b)
        self.vertical = vertical
        self.speed = 1.5
        self.direction = 1  # 1 = indo para B, -1 = voltando para A
        self.state = "walk"
        self.mode = "patrol"  # ou "hunt"
        self.frame_index = 0
        self.frame_timer = 0
        self.anim_speed = 0.15
        self.images = {
            "idle_down": [f"orc_idle_{i:02}" for i in range(5)],
            "walk_down": [f"orc_walk_{i:02}" for i in range(7)],
        }
        self.facing = "down"
    def get_rect(self, pos=None):
        if pos is None:
            pos = self.pos
        return Rect(pos[0] + 38, pos[1] + 38, 20, 20)
    
    def update(self, dt, player_pos, walls, bushes, player_hidden=False):
        previous_state = self.state
        prev_pos = list(self.pos)

        def will_collide(pos):
            rect = Rect(pos[0] + 38, pos[1] + 38, 20, 20)
            for wall in walls:
                if rect.colliderect(wall.rect):
                    return True
            for bush in bushes:
                if rect.colliderect(bush.rect):
                    return True
            return False

        if self.mode == "hunt" and not player_hidden:
            dx = player_pos[0] - self.pos[0]
            dy = player_pos[1] - self.pos[1]
            dist = math.hypot(dx, dy)

            if dist > 4:
                angle = math.atan2(dy, dx)
                step_x = math.cos(angle) * self.speed
                step_y = math.sin(angle) * self.speed

                test_pos = [self.pos[0] + step_x, self.pos[1] + step_y]
                if not will_collide(test_pos):
                    self.pos = test_pos
                    self.state = "walk"
                else:
                    # Tentar mover só em X
                    test_pos_x = [self.pos[0] + step_x, self.pos[1]]
                    test_pos_y = [self.pos[0], self.pos[1] + step_y]

                    if not will_collide(test_pos_x):
                        self.pos = test_pos_x
                        self.state = "walk"
                    elif not will_collide(test_pos_y):
                        self.pos = test_pos_y
                        self.state = "walk"
                    else:
                        self.state = "idle"
            else:
                self.state = "idle"

        else:
            self.mode = "patrol"
            axis = 1 if self.vertical else 0
            step = self.speed if self.direction == 1 else -self.speed

            test_pos = self.pos[:]
            test_pos[axis] += step

            if will_collide(test_pos):
                self.direction *= -1  # inverte antes de andar
                test_pos[axis] = self.pos[axis] + (-step)
                if not will_collide(test_pos):
                    self.pos[axis] = test_pos[axis]
                    self.state = "walk"
                else:
                    self.state = "idle"  # travado, espera
            else:
                self.pos[axis] = test_pos[axis]
                self.state = "walk"

            # detectar player
            dist_to_player = math.hypot(player_pos[0] - self.pos[0], player_pos[1] - self.pos[1])
            if dist_to_player < 150 and not player_hidden:
                self.mode = "hunt"

        # animação
        if self.state != previous_state:
            self.frame_index = 0

        self.frame_timer += dt
        current_anim = self.images.get("walk_down", [])
        if current_anim and self.frame_timer >= self.anim_speed:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(current_anim)
    def draw(self):
        anim_key = f"{self.state}_down"
        current_anim = self.images.get(anim_key, [])
        if current_anim:
            image = current_anim[self.frame_index]
            screen.blit(image, self.pos)


#== Classe WALL ==#
class Wall:
    def __init__(self, pos, size):
        margin = 3
        self.image = "wall"
        self.rect = Rect(
            pos[0] + margin,
            pos[1] + margin,
            size[0] - 2 * margin,
            size[1] - 2 * margin
        )
        self.draw_pos = pos
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Bush:
    def __init__(self, pos):
        self.pos = pos
        self.image = "bush"
        self.rect = Rect(pos[0] + 4, pos[1] + 4, 24, 24)  # hitbox menor que a imagem

    def draw(self):
        screen.blit(self.image, self.pos)

player = Player((WIDTH // 2, HEIGHT // 2))
door = ExitDoor((WIDTH - 100, HEIGHT // 2 - 32))

def on_music_end():
    if music_on:
        music.play("bgm")


def draw():
    screen.clear()
    
    if game_state == STATE_MENU:
        screen.draw.text("Temple Escape", center=(WIDTH // 2, 100),
                         fontsize=48, color="white")
        for button in buttons:
            button.draw()

    elif game_state == STATE_PLAYING:
        draw_ground()
        for relic in relics:
            relic.draw()
        door.draw()
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for wall in walls:
            wall.draw()
        for bush in bushes:
            bush.draw()
        # HUD
        screen.draw.filled_rect(
            Rect(0, -5, 0, 40),
            (0, 0, 0, 30)
        )
        screen.draw.text(f"Relics: {relics_collected}/3", topleft=(10, 10), fontsize=24, color="white")
        if relics_collected == 3:
            screen.draw.text("All relics collected! Find the exit!",
                             center=(WIDTH // 2, 20), fontsize=28, color="yellow")
        

    elif game_state == STATE_GAME_OVER:
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=64, color="red")
        for button in end_buttons:
            button.draw()

    elif game_state == STATE_WIN:
        screen.draw.text("You Escaped!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=64, color="yellow")
        for button in end_buttons:
            button.draw()

def update(dt):
    global game_state

    if game_state == STATE_MENU:
        for button in buttons:
            button.update_hover(mouse_pos)
    elif game_state in (STATE_GAME_OVER, STATE_WIN):
        for button in end_buttons:
            button.update_hover(mouse_pos)

    elif game_state == STATE_PLAYING:
        prev_pos = list(player.pos)
        player.update()
        player_rect = player.get_rect()
        was_hidden = player.hidden
        player.hidden = False

        for bush in bushes:
            if player_rect.colliderect(bush.rect):
                player.hidden = True
                break
        # Tocar som só ao entrar no bush
        if player.hidden and not was_hidden and sfx_on:
            try:
                sounds.hide.play()
            except:
                print("Som 'hide.ogg' não encontrado.")
        for wall in walls:
            if player_rect.colliderect(wall.rect):
                player.pos = prev_pos
                player.dest = prev_pos  # Cancela o movimento
                break
            

        if relics_collected == 3:
            door.opened = True

        for relic in relics:
            relic.check_collision(player_rect)
        
        for enemy in enemies:
            enemy.update(dt, player.pos, walls, bushes, player_hidden = player.hidden)
            if enemy.get_rect().colliderect(player_rect):
                game_state = STATE_GAME_OVER
                if sfx_on:
                    sounds.hit.play()
                    
        if door.opened and door.check_collision(player_rect):
            if sfx_on:
                sounds.door.play()
            game_state = STATE_WIN



def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos


def on_mouse_down(pos):
    global mouse_pos
    mouse_pos = pos

    if game_state == STATE_MENU:
        for button in buttons:
            button.click()
        return
    elif game_state in (STATE_GAME_OVER, STATE_WIN):
        for button in end_buttons:
            button.click()
        return
    elif game_state == STATE_PLAYING:
        player.dest = [pos[0] - 48, pos[1] - 48]
