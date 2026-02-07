from game.constants import TILE_SIZE

def build_map_grid():
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
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if x == x1 or x == x2 or y == y1 or y == y2:
                    MAP_GRID[y][x] = 1
                else:
                    MAP_GRID[y][x] = 0

    # -------------------------
    # 3 SALAS + CORREDORES
    # -------------------------
    add_room(2, 2, 10, 7)       # Sala 1 (top-left)
    add_room(19, 2, 27, 7)      # Sala 2 (top-right)
    add_room(11, 12, 18, 17)    # Sala 3 (bottom-middle)

    # Corredor horizontal central
    for x in range(1, 29):
        MAP_GRID[9][x] = 0

    # Corredor vertical até sala 3
    for y in range(9, 18):
        MAP_GRID[y][14] = 0

    # Aberturas para conectar as salas
    MAP_GRID[5][10] = 0
    MAP_GRID[6][10] = 0
    MAP_GRID[5][19] = 0
    MAP_GRID[5][20] = 0
    MAP_GRID[12][14] = 0
    MAP_GRID[12][15] = 0

    # -------------------------
    # ENTIDADES
    # -------------------------
    MAP_GRID[9][2] = "P"

    MAP_GRID[4][6] = "E"
    MAP_GRID[6][8] = "R"

    MAP_GRID[4][23] = "E"
    MAP_GRID[6][21] = "R"

    MAP_GRID[14][16] = "E"
    MAP_GRID[16][12] = "R"

    MAP_GRID[4][4] = "B"
    MAP_GRID[6][24] = "B"
    MAP_GRID[15][13] = "B"
    MAP_GRID[15][15] = "B"

    MAP_GRID[9][29] = "D"

    return MAP_GRID


def draw_ground(screen, map_grid):
    for y, row in enumerate(map_grid):
        for x, _ in enumerate(row):
            screen.blit("ground", (x * TILE_SIZE, y * TILE_SIZE))
