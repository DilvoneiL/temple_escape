import math
from pygame import Rect
from game.constants import TILE_SIZE

class Button:
    def __init__(self, text, pos, callback):
        self.text = text
        self.rect = Rect(pos[0], pos[1], 220, 50)
        self.callback = callback
        self.hover = False

    def draw(self, screen):
        color = "darkgreen" if self.hover else "green"
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(self.text, center=self.rect.center, fontsize=32, color="white")

    def update_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)

    def click(self):
        if self.hover:
            self.callback()


class Relic:
    def __init__(self, pos):
        self.pos = pos
        self.collected = False
        self.image = "relic"

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.pos)

    def check_collision(self, player_rect, sounds, sfx_on):
        if (not self.collected) and player_rect.colliderect(Rect(self.pos[0], self.pos[1], 32, 32)):
            self.collected = True
            if sfx_on:
                try:
                    sounds.pickup.play()
                except:
                    pass
            return True
        return False


class ExitDoor:
    def __init__(self, pos):
        self.pos = pos
        self.image_closed = "door"
        self.image_open = "door_open"
        self.opened = False
        self.rect = Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        screen.blit(self.image_open if self.opened else self.image_closed, self.pos)

    def check_collision(self, player_rect):
        if self.opened and player_rect.colliderect(Rect(self.pos[0], self.pos[1], 48, 64)):
            return True
        return False


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

        if self.state != previous_state:
            self.frame_index = 0

        self.frame_timer += self.anim_speed
        current_anim = self.images.get(f"{self.state}_{self.direction}", [])
        if current_anim and self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(current_anim)

    def draw(self, screen):
        key = f"{self.state}_{self.direction}"
        current_anim = self.images.get(key, [])
        if not current_anim:
            return
        image = current_anim[self.frame_index]
        if self.hidden:
            screen.surface.set_alpha(100)
            screen.blit(image, self.pos)
            screen.surface.set_alpha(255)
        else:
            screen.blit(image, self.pos)

    def get_rect(self):
        return Rect(self.pos[0] + 38, self.pos[1] + 38, 18, 18)


class Enemy:
    def __init__(self, point_a, point_b, vertical=False):
        self.pos = list(point_a)
        self.point_a = list(point_a)
        self.point_b = list(point_b)
        self.vertical = vertical
        self.speed = 1.5
        self.direction = 1
        self.state = "walk"
        self.mode = "patrol"
        self.frame_index = 0
        self.frame_timer = 0
        self.anim_speed = 0.15
        self.images = {
            "idle_down": [f"orc_idle_{i:02}" for i in range(5)],
            "walk_down": [f"orc_walk_{i:02}" for i in range(7)],
        }

    def get_rect(self, pos=None):
        if pos is None:
            pos = self.pos
        return Rect(pos[0] + 38, pos[1] + 38, 20, 20)

    def update(self, dt, player_pos, walls, bushes, player_hidden=False):
        previous_state = self.state

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
                self.direction *= -1
                test_pos[axis] = self.pos[axis] + (-step)
                if not will_collide(test_pos):
                    self.pos[axis] = test_pos[axis]
                    self.state = "walk"
                else:
                    self.state = "idle"
            else:
                self.pos[axis] = test_pos[axis]
                self.state = "walk"

            dist_to_player = math.hypot(player_pos[0] - self.pos[0], player_pos[1] - self.pos[1])
            if dist_to_player < 150 and not player_hidden:
                self.mode = "hunt"

        if self.state != previous_state:
            self.frame_index = 0

        self.frame_timer += dt
        current_anim = self.images.get("walk_down", [])
        if current_anim and self.frame_timer >= self.anim_speed:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(current_anim)

    def draw(self, screen):
        anim_key = f"{self.state}_down"
        current_anim = self.images.get(anim_key, [])
        if current_anim:
            screen.blit(current_anim[self.frame_index], self.pos)


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

    def draw(self, screen):
        # mantém como você fez: desenhando no ret ajustado
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Bush:
    def __init__(self, pos):
        self.pos = pos
        self.image = "bush"
        self.rect = Rect(pos[0] + 4, pos[1] + 4, 24, 24)

    def draw(self, screen):
        screen.blit(self.image, self.pos)
