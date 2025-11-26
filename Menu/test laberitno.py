import pygame
import sys
import colisiones as colision


# CONFIG
TILE = 32
FPS = 60

FILAS = len(colision.maze)
COLUMNAS = len(colision.maze[0])

pygame.init()
screen = pygame.display.set_mode((COLUMNAS*TILE, FILAS*TILE))
clock = pygame.time.Clock()

COLOR_WALL = (30,30,30)
COLOR_FLOOR = (240,240,240)
COLOR_PLAYER = (0,120,255)

player_y = cr.player.positions_y
player_x = cr.player.positions_x

# Dirección de movimiento 
dir_y = 0
dir_x = 0

# Temporizador para controlar la velocidad del movimiento por casilla
move_timer = 0
move_delay = 120   # milisegundos por movimiento (se para más lento o más rápido)


# FUNCIONES
def can_move(r, c):
    return 0 <= r < FILAS and 0 <= c < COLUMNAS and colision.maze[r][c] >= 1


def eventos():  # teletransportes
    global player_y, player_x

    if colision.maze[player_y][player_x] == 2:  # Teletransportación Matemagica 1
        if player_y == 14 and player_x == 0:
            player_y = 13
            player_x = 18
            print("Matemagicamente Teletransportado")

        if player_y == 13 and player_x == 19:
            player_y = 14
            player_x = 1
            print("Matemagicamente Teletransportado")

    if colision.maze[player_y][player_x] == 3:  # Teletransportación Matemagica 2
        if player_y == 0 and player_x == 9:
            player_y = 26
            player_x = 10
            print("Matemagicamente Teletransportado")

        if player_y == 27 and player_x == 10:
            player_y = 1
            player_x = 9
            print("Matemagicamente Teletransportado")


# LOOP PRINCIPAL
running = True
while running:
    dt = clock.tick(FPS) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # SOLO establecemos dirección 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                dir_y = -1
                dir_x = 0
            if event.key == pygame.K_s:
                dir_y = 1
                dir_x = 0
            if event.key == pygame.K_a:
                dir_y = 0
                dir_x = -1
            if event.key == pygame.K_d:
                dir_y = 0
                dir_x = 1

    # MOVIMIENTO CONSTANTE 
    move_timer += dt

    if move_timer >= move_delay:
        move_timer = 0

        new_y = player_y + dir_y
        new_x = player_x + dir_x

        if can_move(new_y, new_x):  # si no es pared, avanza
            player_y = new_y
            player_x = new_x
            print("Fila:", player_y, "Columna:", player_x)
            eventos()

  
    # DIBUJO DEL LABERINTO
   
    for r in range(FILAS):
        for c in range(COLUMNAS):
            rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
            color = COLOR_FLOOR if colision.maze[r][c] >= 1 else COLOR_WALL
            pygame.draw.rect(screen, color, rect)

    # Jugador
    pygame.draw.rect(
        screen,
        COLOR_PLAYER,
        (player_x*TILE + 4, player_y*TILE + 4, TILE-8, TILE-8)
    )

    pygame.display.flip()


pygame.quit()
sys.exit()
