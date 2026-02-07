TILE_SIZE = 32
WIDTH = 30 * TILE_SIZE   # 960
HEIGHT = 20 * TILE_SIZE  # 640

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_WIN = "win"

TILE_TYPES = {
    1: "wall",
    0: "ground",
    "R": "relic",
    "B": "bush",
    "E": "enemy",
    "P": "player",
    "D": "door",
}
