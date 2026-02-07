from game.constants import WIDTH, HEIGHT
from game.world import Game

TITLE = "Temple Escape"
game = Game()

def draw():
    game.draw(screen)

def update(dt):
    game.update(dt, screen, music, sounds)

def on_mouse_move(pos):
    game.on_mouse_move(pos)

def on_mouse_down(pos):
    game.on_mouse_down(pos, music, sounds)
