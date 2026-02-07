from pygame import Rect
from game.constants import (
    TILE_SIZE, WIDTH, HEIGHT,
    STATE_MENU, STATE_PLAYING, STATE_GAME_OVER, STATE_WIN
)
from game.map_data import build_map_grid, draw_ground
from game.entities import Wall, Relic, Bush, Enemy, ExitDoor, Player
from game.ui import build_menu_buttons, build_end_buttons

class Game:
    def __init__(self):
        self.game_state = STATE_MENU

        self.music_on = True
        self.sfx_on = True

        self.mouse_pos = (0, 0)

        self.map_grid = build_map_grid()

        self.relics = []
        self.relics_collected = 0
        self.enemies = []
        self.walls = []
        self.bushes = []

        self.door = None
        self.player = None

        self.buttons = build_menu_buttons(
            self.start_game,
            self.toggle_audio,
            self.exit_game,
            self.music_on
        )

        self.end_buttons = build_end_buttons(self.play_again, self.back_to_menu, self.exit_game)

    # ----------------
    # MAP LOADING
    # ----------------
    def load_map(self):
        self.walls = []
        self.relics = []
        self.bushes = []
        self.enemies = []
        self.door = None
        self.player = None

        for y, row in enumerate(self.map_grid):
            for x, tile in enumerate(row):
                pos = (x * TILE_SIZE, y * TILE_SIZE)

                if tile == 1:
                    self.walls.append(Wall(pos, (TILE_SIZE, TILE_SIZE)))
                elif tile == "R":
                    self.relics.append(Relic(pos))
                elif tile == "B":
                    self.bushes.append(Bush(pos))
                elif tile == "E":
                    self.enemies.append(Enemy(pos, (pos[0] + TILE_SIZE * 3, pos[1])))
                elif tile == "D" and self.door is None:
                    self.door = ExitDoor(pos)
                elif tile == "P":
                    self.player = Player(pos)

        if self.player is None:
            self.player = Player((TILE_SIZE * 2, TILE_SIZE * 2))

        if self.door is None:
            self.door = ExitDoor((WIDTH - TILE_SIZE, HEIGHT // 2))

    # ----------------
    # STATE ACTIONS
    # ----------------
    def start_game(self):
        self.relics_collected = 0
        self.load_map()
        self.game_state = STATE_PLAYING

    def toggle_audio(self):
        self.music_on = not self.music_on
        
        self.buttons = build_menu_buttons(self.start_game, self.toggle_audio, self.exit_game, self.music_on)



    def exit_game(self):
        exit()

    def play_again(self):
        self.start_game()

    def back_to_menu(self):
        self.game_state = STATE_MENU

    # ----------------
    # DRAW / UPDATE
    # ----------------
    def draw(self, screen):
        screen.clear()

        if self.game_state == STATE_MENU:
            screen.draw.text("Temple Escape", center=(WIDTH // 2, 100), fontsize=48, color="white")
            for b in self.buttons:
                b.draw(screen)

        elif self.game_state == STATE_PLAYING:
            draw_ground(screen, self.map_grid)

            for r in self.relics:
                r.draw(screen)

            self.door.draw(screen)
            self.player.draw(screen)

            for e in self.enemies:
                e.draw(screen)

            for w in self.walls:
                w.draw(screen)

            for b in self.bushes:
                b.draw(screen)

            # HUD
            screen.draw.text(f"Relics: {self.relics_collected}/3", topleft=(10, 10), fontsize=24, color="white")
            if self.relics_collected == 3:
                screen.draw.text("All relics collected! Find the exit!", center=(WIDTH // 2, 20), fontsize=28, color="yellow")

        elif self.game_state == STATE_GAME_OVER:
            screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2), fontsize=64, color="red")
            for b in self.end_buttons:
                b.draw(screen)

        elif self.game_state == STATE_WIN:
            screen.draw.text("You Escaped!", center=(WIDTH // 2, HEIGHT // 2), fontsize=64, color="yellow")
            for b in self.end_buttons:
                b.draw(screen)

    def update(self, dt, screen, music, sounds):
        if self.game_state == STATE_MENU:
            for b in self.buttons:
                b.update_hover(self.mouse_pos)
            return

        if self.game_state in (STATE_GAME_OVER, STATE_WIN):
            for b in self.end_buttons:
                b.update_hover(self.mouse_pos)
            return

        if self.game_state != STATE_PLAYING:
            return

        # tocar/parar musica conforme toggle
        try:
            if self.music_on and (not music.is_playing("bgm")):
                music.play("bgm")
            if (not self.music_on) and music.is_playing("bgm"):
                music.stop()
        except:
            pass

        prev_pos = list(self.player.pos)
        self.player.update()
        player_rect = self.player.get_rect()

        # stealth
        was_hidden = self.player.hidden
        self.player.hidden = False
        for bush in self.bushes:
            if player_rect.colliderect(bush.rect):
                self.player.hidden = True
                break

        if self.player.hidden and not was_hidden and self.sfx_on:
            try:
                sounds.hide.play()
            except:
                pass

        # colisão com paredes
        for wall in self.walls:
            if player_rect.colliderect(wall.rect):
                self.player.pos = prev_pos
                self.player.dest = prev_pos
                player_rect = self.player.get_rect()
                break

        # door abre com 3
        if self.relics_collected == 3:
            self.door.opened = True

        # pegar relic
        for relic in self.relics:
            if relic.check_collision(player_rect, sounds, self.sfx_on):
                self.relics_collected += 1

        # inimigos
        for enemy in self.enemies:
            enemy.update(dt, self.player.pos, self.walls, self.bushes, player_hidden=self.player.hidden)
            if enemy.get_rect().colliderect(player_rect):
                self.game_state = STATE_GAME_OVER
                if self.sfx_on:
                    try:
                        sounds.hit.play()
                    except:
                        pass
                return

        # win
        if self.door.opened and self.door.check_collision(player_rect):
            if self.sfx_on:
                try:
                    sounds.door.play()
                except:
                    pass
            self.game_state = STATE_WIN

    # ----------------
    # INPUT
    # ----------------
    def on_mouse_move(self, pos):
        self.mouse_pos = pos

    def on_mouse_down(self, pos, music, sounds):
        self.mouse_pos = pos

        if self.game_state == STATE_MENU:
            for b in self.buttons:
                b.update_hover(pos)  # garante hover correto no clique
                b.click()
            return

        if self.game_state in (STATE_GAME_OVER, STATE_WIN):
            for b in self.end_buttons:
                b.update_hover(pos)
                b.click()
            return

        if self.game_state == STATE_PLAYING:
            self.player.dest = [pos[0] - 48, pos[1] - 48]

