#CLON PARA IMPORTAR BOTS
import pygame
import sys
import criaturas as cr
import colisiones as colision
import random

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
COLOR_ENEMY = (255,50,50)

enemigo_f = 13
enemigo_c = 10

enemy_cooldown = 0
enemy_wait = 250  # milisegundoss

RANGO_DESTRABE = 5   # Aumentar este número aumenta el rango de prueba

def mover_enemigo(r, c, player_r, player_c):

    # ---------- 1. mover normalmente hacia el jugador ----------
    direcciones_normales = []

    if player_r < r: direcciones_normales.append((r-1, c))     # arriba
    if player_r > r: direcciones_normales.append((r+1, c))     # abajo
    if player_c < c: direcciones_normales.append((r, c-1))     # izquierda
    if player_c > c: direcciones_normales.append((r, c+1))     # derecha

    for nr, nc in direcciones_normales:
        if can_move(nr, nc):
            return nr, nc

    # -----------------------------------------------------------
    # 2. Buscar destinos alternativos en un área amplia
    # -----------------------------------------------------------

    destinos = []
    for dy in range(-RANGO_DESTRABE, RANGO_DESTRABE+1):
        for dx in range(-RANGO_DESTRABE, RANGO_DESTRABE+1):
            tr = r + dy
            tc = c + dx
            if can_move(tr, tc):
                destinos.append((tr, tc))

    if not destinos:
        return r, c  # no hay nada útil alrededor

    # ordenar destinos por distancia al jugador (busca acercarse igual)
    destinos.sort(key=lambda d: abs(d[0]-player_r) + abs(d[1]-player_c))

    mejor_destino = destinos[0]

    # -----------------------------------------------------------
    # 3. Para ese destino, probar TODOS los movimientos posibles
    # -----------------------------------------------------------

    opciones = [
        (r-1, c),  # arriba
        (r+1, c),  # abajo
        (r, c-1),  # izquierda
        (r, c+1),  # derecha
    ]

    # ordenar las opciones según cuál se acerca más al destino alternativo
    opciones.sort(key=lambda pos: abs(pos[0]-mejor_destino[0]) + abs(pos[1]-mejor_destino[1]))

    # ahora probamos cada opción
    for nr, nc in opciones:
        if can_move(nr, nc):
            return nr, nc

    # si todas fallan, se queda quieto
    return r, c

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
            
    # ---------------------------
    # MOVER ENEMIGO
    # ---------------------------
    ahora = pygame.time.get_ticks()
    if ahora - enemy_cooldown >= enemy_wait:
        enemigo_f, enemigo_c = mover_enemigo(enemigo_f, enemigo_c, player_f, player_c)
        enemy_cooldown = ahora

    # ---------------------------
    # COLISIÓN
    # ---------------------------
    if enemigo_f == player_f and enemigo_c == player_c:
        print("Te dividieron por 0")
        running = False
            
    # DIBUJO

    for r in range(FILAS):
        for c in range(COLUMNAS):
            rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
            color = COLOR_FLOOR if colision.maze[r][c] >= 1 else COLOR_WALL
            pygame.draw.rect(screen, color, rect)

    # dibujar enemigo
    
    pygame.draw.rect(
        screen, COLOR_ENEMY
        (cr.pigarto.positions_x[0]*TILE+6, cr.pigarto.positions_y[0], TILE-12, TILE-12)
    )
    
    pygame.draw.rect(
        screen, COLOR_ENEMY,
        (enemigo_c*TILE + 6, enemigo_f*TILE + 6, TILE-12, TILE-12)
    )
    
    pygame.draw.rect(
        screen,
        COLOR_PLAYER,
        (player_c*TILE + 4, player_f*TILE + 4, TILE-8, TILE-8)
    )

    pygame.display.flip()

pygame.quit()
sys.exit()