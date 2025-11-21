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

player_f = 23    # (fila donde quieres ponerlo)
player_c = 10 # (columna donde quieres ponerlo)

def can_move(r, c):
    return 0 <= r < FILAS and 0 <= c < COLUMNAS and colision.maze[r][c] >= 1

def eventos(): #Etiquetas para la matriz
        global player_f
        global player_c
        if colision.maze[player_f][player_c] == 2: #Teletransportación Matemagica 1
                    if player_f==14 and player_c==0:
                        player_f=13
                        player_c=18
                        print("Matemagicamente Teletransportado")
                        
                    if player_f==13 and player_c==19:
                        player_f=14
                        player_c=1
                        print("Matemagicamente Teletransportado")
                        
        if colision.maze[player_f][player_c] == 3: #Teletransportación Matemagica 2
                    if player_f==0 and player_c==9:
                        player_f=26
                        player_c=10
                        print("Matemagicamente Teletransportado")
                        
                    if player_f==27 and player_c==10:
                        player_f=1
                        player_c=9
                        print("Matemagicamente Teletransportado")

# MOVIMIENTO 

move_cooldown = True   # evita que avance varias casillas al dejar presionada una tecla

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # se detecta cada vez que presionas una tecla (solo una vez)
        if event.type == pygame.KEYDOWN:
            if not move_cooldown:
                if event.key == pygame.K_w and can_move(player_f - 1, player_c):
                    player_f -= 1
                    print("Fila:", player_f, "Columna:", player_c)
                    eventos()
                if event.key == pygame.K_s and can_move(player_f + 1, player_c):
                    player_f += 1
                    print("Fila:", player_f, "Columna:", player_c)
                    eventos()
                if event.key == pygame.K_a and can_move(player_f, player_c - 1):
                    player_c -= 1
                    print("Fila:", player_f, "Columna:", player_c)
                    eventos()
                if event.key == pygame.K_d and can_move(player_f, player_c + 1):
                    player_c += 1
                    print("Fila:", player_f, "Columna:", player_c)
                    eventos()

                move_cooldown = True

        if event.type == pygame.KEYUP:
            move_cooldown = False
    # DIBUJO

    for r in range(FILAS):
        for c in range(COLUMNAS):
            rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
            color = COLOR_FLOOR if colision.maze[r][c] >= 1 else COLOR_WALL
            pygame.draw.rect(screen, color, rect)

    
    
    pygame.draw.rect(
        screen,
        COLOR_PLAYER,
        (player_c*TILE + 4, player_f*TILE + 4, TILE-8, TILE-8)
    )

    pygame.display.flip()

pygame.quit()
sys.exit()