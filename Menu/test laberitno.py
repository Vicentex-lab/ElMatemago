import pygame
import sys
import colisiones as colision  # tu matriz maze

# CONFIG
TILE = 32
FPS = 60

pygame.init()
FILAS = len(colision.maze)
COLUMNAS = len(colision.maze[0])
screen = pygame.display.set_mode((COLUMNAS*TILE, FILAS*TILE))
clock = pygame.time.Clock()

COLOR_WALL = (30,30,30)
COLOR_FLOOR = (240,240,240)
COLOR_PLAYER = (0,120,255)

# POSICIÓN INICIAL
player_x = 10
player_y = 23

# DIRECCIÓN ACTUAL
dir_x = 0
dir_y = 0

def can_move(y, x):
    return 0 <= y < FILAS and 0 <= x < COLUMNAS and colision.maze[y][x] >= 1

def eventos():
    global player_x, player_y
    # Teletransportación 1
    if colision.maze[player_y][player_x] == 2:
        if player_y == 14 and player_x == 0:
            player_y, player_x = 13, 18
        elif player_y == 13 and player_x == 19:
            player_y, player_x = 14, 1

    # Teletransportación 2
    if colision.maze[player_y][player_x] == 3:
        if player_y == 0 and player_x == 9:
            player_y, player_x = 26, 10
        elif player_y == 27 and player_x == 10:
            player_y, player_x = 1, 9

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # NUEVA DIRECCIÓN SOLO CUANDO PULSAS TECLA
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:   # arriba
                dir_x, dir_y = 0, -1
            if event.key == pygame.K_s:   # abajo
                dir_x, dir_y = 0, 1
            if event.key == pygame.K_a:   # izquierda
                dir_x, dir_y = -1, 0
            if event.key == pygame.K_d:   # derecha
                dir_x, dir_y = 1, 0

    # MOVIMIENTO CONSTANTE 
    next_x = player_x + dir_x
    next_y = player_y + dir_y

    if can_move(next_y, next_x):
        player_x = next_x
        player_y = next_y
        eventos()  

    #DIBUJO 
    for y in range(FILAS):
        for x in range(COLUMNAS):
            rect = pygame.Rect(x*TILE, y*TILE, TILE, TILE)
            color = COLOR_FLOOR if colision.maze[y][x] >= 1 else COLOR_WALL
            pygame.draw.rect(screen, color, rect)

    pygame.draw.rect(
        screen,
        COLOR_PLAYER,
        (player_x*TILE + 4, player_y*TILE + 4, TILE-8, TILE-8)
    )

    pygame.display.flip()

pygame.quit()
sys.exit()