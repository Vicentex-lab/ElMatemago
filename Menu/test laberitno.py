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

player_f = 23
player_c = 10

# Dirección de movimiento 
dir_f = 0
dir_c = 0

# Temporizador para controlar la velocidad del movimiento por casilla
move_timer = 0
<<<<<<< Updated upstream
move_delay = 120   # milisegundos por movimiento (se para más lento o más rápido)
=======
move_delay = 120   # milisegundos por movimiento 
>>>>>>> Stashed changes


# FUNCIONES
def can_move(r, c):
    return 0 <= r < FILAS and 0 <= c < COLUMNAS and colision.maze[r][c] >= 1


def eventos():  # teletransportes
    global player_f, player_c

    if colision.maze[player_f][player_c] == 2:  # Teletransportación Matemagica 1
        if player_f == 14 and player_c == 0:
            player_f = 13
            player_c = 18
            print("Matemagicamente Teletransportado")

        if player_f == 13 and player_c == 19:
            player_f = 14
            player_c = 1
            print("Matemagicamente Teletransportado")

    if colision.maze[player_f][player_c] == 3:  # Teletransportación Matemagica 2
        if player_f == 0 and player_c == 9:
            player_f = 26
            player_c = 10
            print("Matemagicamente Teletransportado")

        if player_f == 27 and player_c == 10:
            player_f = 1
            player_c = 9
            print("Matemagicamente Teletransportado")


# LOOP PRINCIPAL
running = True
while running:
<<<<<<< Updated upstream
    dt = clock.tick(FPS) 
=======
    dt = clock.tick(FPS)  # delta time para el timer
>>>>>>> Stashed changes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

<<<<<<< Updated upstream
        # SOLO establecemos dirección (como Pac-Man)
=======
>>>>>>> Stashed changes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                dir_f = -1
                dir_c = 0
            if event.key == pygame.K_s:
                dir_f = 1
                dir_c = 0
            if event.key == pygame.K_a:
                dir_f = 0
                dir_c = -1
            if event.key == pygame.K_d:
                dir_f = 0
                dir_c = 1

    # MOVIMIENTO CONSTANTE 
    move_timer += dt

    if move_timer >= move_delay:
        move_timer = 0

        new_f = player_f + dir_f
        new_c = player_c + dir_c

        if can_move(new_f, new_c):  # si no es pared, avanza
            player_f = new_f
            player_c = new_c
            print("Fila:", player_f, "Columna:", player_c)
            eventos()

<<<<<<< Updated upstream
  
    # DIBUJO DEL LABERINTO
   
=======
    # -------------------
    # DIBUJO DEL LABERINTO
    # -------------------
>>>>>>> Stashed changes
    for r in range(FILAS):
        for c in range(COLUMNAS):
            rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
            color = COLOR_FLOOR if colision.maze[r][c] >= 1 else COLOR_WALL
            pygame.draw.rect(screen, color, rect)

    # Jugador
    pygame.draw.rect(
        screen,
        COLOR_PLAYER,
        (player_c*TILE + 4, player_f*TILE + 4, TILE-8, TILE-8)
    )

    pygame.display.flip()


pygame.quit()
sys.exit()
