import pygame, sys
import os 
from button import Button
import colisiones as colision
import criaturas as cr
import items as item
import random
import configuracion as cfg
# Inicializa Pygame
pygame.init() 
pygame.mixer.init()  # Inicializa el módulo de mezcla de sonido


# Define la pantalla en modo Fullscreen
SCREEN = pygame.display.set_mode((cfg.ANCHO_PANTALLA, cfg.ALTO_PANTALLA), pygame.FULLSCREEN)

#Importamos sprites luego definir pantalla Fullscreen
from sprites import MAGO, CERO, RAIZNEGATIVA, PIGARTO, ESPADA, ESCUDO, ANILLO
pygame.display.set_caption("EL MATEMAGO")


# --- FUNCIÓN DE UTILIDAD PARA SALIDA RÁPIDA (ESCAPE / QUIT) ---
def manejar_salida_menu(event):
    """Maneja eventos de salida directa del juego (QUIT o ESCAPE) en pantallas de menú."""
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

def low_score_message():
    """Muestra un mensaje indicando que el puntaje es demasiado bajo para guardar y vuelve al menú."""
    
    # Detiene cualquier música que quede sonando
    pygame.mixer.music.stop() 
    
    # 1. Crear un reloj local y definir FPS 
    clock = pygame.time.Clock() 
    FPS = 60
    
    start_time = pygame.time.get_ticks()
    display_time = 3000 # Mostrar por 3 segundos
    
    while pygame.time.get_ticks() - start_time < display_time:
        
        # 2. Limitar la velocidad del bucle
        clock.tick(FPS) 
        
        # Manejo de eventos para permitir salir con QUIT/ESCAPE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Permitir salir antes de tiempo presionando ESCAPE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return menu_principal() 
        
        # DIBUJO DEL MENSAJE 
        SCREEN.fill("#111111") # Fondo oscuro

        # Título
        TEXTO_TITULO = cfg.get_letra(60).render("¡FIN DEL JUEGO!", True, "#FF0000") 
        RECT_TITULO = TEXTO_TITULO.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 50))
        SCREEN.blit(TEXTO_TITULO, RECT_TITULO)
        
        TEXTO_SUB = cfg.get_letra(20).render("TU PUNTAJE ES 0. NECESITAS MÁS DE 0 PUNTOS PARA PODER GUARDARLO.", True, "#FFFFFF")
        RECT_SUB = TEXTO_SUB.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y + 50))
        SCREEN.blit(TEXTO_SUB, RECT_SUB)
        
        pygame.display.update() 
        
    return menu_principal() # Vuelve al menú principal después de 3 segundos
    
# --- PANTALLA JUGAR ----- #

def jugar():
    # Muestra la pantalla de juego, detiene la música del menú e inicia la música de juego.
    
    # 1. Detiene la música actual (la del menú)
    pygame.mixer.music.stop()
    
    # 2. Carga y reproduce la música del juego en loop
    try:
        pygame.mixer.music.load(cfg.RUTA_MUSICA_JUEGO) 
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL) 
    except pygame.error as e:
        print(f"Error al cargar la música del juego: {e}")

    def mostrar_puntaje(player_pts):
        fuente = cfg.get_letra(30)  
        texto = fuente.render(f"PUNTAJE: {player_pts}", True, (255, 255, 0)) 
        SCREEN.blit(texto, (50,50)) # Usar SCREEN global

    FPS = 60
    
    FILAS = len(colision.maze)
    COLUMNAS = len(colision.maze[0])
    
    COLOR_WALL = (30,30,30)
    COLOR_FLOOR = (253, 254, 253)
    COLOR_PLAYER = (0,120,255)
    COLOR_CERO = (0, 0, 255)
    COLOR_PIGARTO = (0, 255, 0)
    COLOR_RAIZ = (255, 0, 0)
    COLOR_SWORD = (255, 255, 0)
    COLOR_SHIELD = (255, 165, 0)
    COLOR_RING = (0, 0, 0)
    COLOR_HEART = (255, 100, 100)
    
    screen = SCREEN # Usar la variable global SCREEN
    clock = pygame.time.Clock()
    
    #Definiciones del jugador
    player_y = cr.player.positions_y
    player_x = cr.player.positions_x
    player_hp = cr.player.hp
    player_item=""
    inmunidad=0
    player_pts=cr.player.pts
    temporizador=0
    
    # Pigarto: Resetea el índice de posición en su camino y su existencia.
    cr.pigarto.pos = 0 
    cr.pigarto.exist = 1 # Asumimos que debe empezar vivo
    
    # Cero: Resetea su existencia y posición (si fueron modificados al morir).
    cr.cero.exist = 1 
    
    # Raíz Negativa: Resetea su existencia
    cr.raiznegativa.exist = 1 

    
    #Spawnear Item
    #Espada
    cont_aux_1=random.randint(0, 5)
    print("espada",  cont_aux_1)
    sword_place_y=item.sword.places_y[ cont_aux_1]
    sword_place_x=item.sword.places_x[ cont_aux_1]
    
    #Escudo
    cont_aux_1=random.randint(0, 5)
    while item.shield.places_x==sword_place_x and item.shield.places_y==sword_place_y:
        cont_aux_1=random.randint(0, 5)
    print("escudo",  cont_aux_1)
    shield_place_y=item.shield.places_y[cont_aux_1]
    shield_place_x=item.shield.places_x[cont_aux_1]
    
    #Anillo
    cont_aux_1=random.randint(0, 5)
    print("anillo", cont_aux_1)
    while item.ring.places_x==sword_place_x and item.ring.places_y==sword_place_y and item.ring.places_x==shield_place_x and item.ring.places_y==shield_place_y:
        cont_aux_1=random.randint(0, 5)
    ring_place_y=item.shield.places_y[cont_aux_1]
    ring_place_x=item.shield.places_x[cont_aux_1]
    
    def can_move(r, c):
        return 0 <= r < FILAS and 0 <= c < COLUMNAS and colision.maze[r][c] >= 1
    
    def eventos(): #Etiquetas para la matriz
            nonlocal player_y
            nonlocal player_x
            if colision.maze[player_y][player_x] == 2: #Teletransportación Matemagica 1
                        if player_y==14 and player_x==0:
                            player_y=13
                            player_x=18
                            print("Matemagicamente Teletransportado")
                            
                        if player_y==13 and player_x==19:
                            player_y=14
                            player_x=1
                            print("Matemagicamente Teletransportado")
                            
            if colision.maze[player_y][player_x] == 3: #Teletransportación Matemagica 2
                        if player_y==0 and player_x==9:
                            player_y=26
                            player_x=10
                            print("Matemagicamente Teletransportado")
                            
                        if player_y==27 and player_x==10:
                            player_y=1
                            player_x=9
                            print("Matemagicamente Teletransportado")
    
    #MOVIMIENTO DEL ENEMIGO
    # ---------------------------
    # CERO
    # ---------------------------
    cero_y = cr.cero.positions_y
    cero_x = cr.cero.positions_x
    cero_exist=cr.cero.exist
    cero_cooldown = 0
    cero_ratio=cr.cero.movement_ratio
    
    # ---------------------------
    # Pigarto
    # ---------------------------
    pigarto_y = cr.pigarto.positions_y
    pigarto_x = cr.pigarto.positions_x
    pigarto_cooldown = 0
    pigarto_exist=cr.pigarto.exist
    pigarto_ratio=cr.pigarto.movement_ratio
    # ---------------------------
    # Raíz Negativa
    # ---------------------------
    raiznegativa_y = cr.raiznegativa.positions_y
    raiznegativa_x = cr.raiznegativa.positions_x
    raiznegativa_ratio=cr.raiznegativa.movement_ratio
    raiznegativa_cooldown = 0
    raiznegativa_exist=cr.raiznegativa.exist

    def mover_enemigo(f, c, f_obj, c_obj):
        """Mueve al enemigo acercándose al jugador"""

        # Vertical
        if f_obj < f and can_move(f - 1, c):
            f -= 1
        elif f_obj > f and can_move(f + 1, c):
            f += 1

        # Horizontal
        elif c_obj < c and can_move(f, c - 1):
            c -= 1
        elif c_obj > c and can_move(f, c + 1):
            c += 1

        return f, c
 
    
    move_cooldown = True   # evita que avance varias casillas al dejar presionada una tecla
    
    # ============================
    #  MOVIMIENTO DEL JUGADOR 
    # ============================


    # Dirección actual del jugador
    dir_x = 0
    dir_y = 0

    # Dirección deseada (la que el jugador quiere)
    desired_x = 0
    desired_y = 0

    # Posición en pixeles
    pos_x = player_x * cfg.TILE
    pos_y = player_y * cfg.TILE

    speed = 4  # velocidad (pixeles por frame)

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Guardar dirección DESEADA siempre
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    desired_x = 0
                    desired_y = -1

                if event.key in (pygame.K_s, pygame.K_DOWN):
                    desired_x = 0
                    desired_y = 1

                if event.key in (pygame.K_a, pygame.K_LEFT):
                    desired_x = -1
                    desired_y = 0

                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    desired_x = 1
                    desired_y = 0

        # -------------------------------
        # A) Intentar girar si la casilla lo permite
        # -------------------------------
        tile_x = round(pos_x / cfg.TILE)
        tile_y = round(pos_y / cfg.TILE)

        # ¿Está exactamente centrado en una casilla?
        aligned_x = (pos_x % cfg.TILE) == 0
        aligned_y = (pos_y % cfg.TILE) == 0

        if aligned_x and aligned_y:
            # Intentar aplicar la dirección deseada
            next_tx = tile_x + desired_x
            next_ty = tile_y + desired_y

            if can_move(next_ty, next_tx):
                dir_x = desired_x
                dir_y = desired_y

            # Verificar la dirección actual
            next_tx = tile_x + dir_x
            next_ty = tile_y + dir_y

            if not can_move(next_ty, next_tx):
                dir_x = 0
                dir_y = 0

        # -------------------------------
        # B) Mover en pixeles
        # -------------------------------
        pos_x += dir_x * speed
        pos_y += dir_y * speed

        # Actualizar posición en casillas
        player_x = round(pos_x / cfg.TILE)
        player_y = round(pos_y / cfg.TILE)

        eventos()

                
        # ---------------------------
        # MOVER ENEMIGO
        # ---------------------------
        #Cero
        ahora = pygame.time.get_ticks()
        if ahora - cero_cooldown >= cero_ratio:
            cero_y, cero_x = mover_enemigo(cero_y, cero_x, player_y, player_x)
            cero_cooldown = ahora

        #Pigarto
        if ahora - pigarto_cooldown >= pigarto_ratio:
            if cr.pigarto.pos<106:
                cr.pigarto.pos = cr.pigarto.pos+1
                pigarto_cooldown=ahora
            if cr.pigarto.pos>=106:
                cr.pigarto.pos=0
                pigarto_cooldown=ahora
                
        #Raiz negativa
        if ahora - raiznegativa_cooldown >= raiznegativa_ratio:
            raiznegativa_y, raiznegativa_x = mover_enemigo(raiznegativa_y, raiznegativa_x, player_y, player_x)
            raiznegativa_cooldown = ahora
            #ESTOCADA INTEGRADA EN  MAIN
            if raiznegativa_x==player_x:
                raiznegativa_ratio=cr.raiznegativa.movement_ratio-150
            elif raiznegativa_y==player_y:
                raiznegativa_ratio=cr.raiznegativa.movement_ratio-150
            else:
                raiznegativa_ratio=cr.raiznegativa.movement_ratio
        # ---------------------------
        # COLISIÓN (Lógica de DERROTA)
        # ---------------------------
        #Con CERO
        if cero_y == player_y and cero_x == player_x and cero_exist==1:
            if player_item==item.shield.name:
                player_item=""
                inmunidad=0
                cero_x=cr.cero.positions_x
                cero_y=cr.cero.positions_y
            elif player_item==item.sword.name:
                player_pts+=cr.cero.pts
                COLOR_CERO=COLOR_FLOOR
                player_item=""
                cero_exist=0
                if pigarto_exist==1 and raiznegativa_exist==0:
                    print("espada: cero")
                    COLOR_SWORD=(255, 255, 0)
                    sword_place_y=cr.cero.positions_y
                    sword_place_x=cr.cero.positions_y
            elif inmunidad!=1 and player_hp-cr.cero.damage>0:
                player_x=cr.player.positions_x #El matemago muere instantaneamente si no se cambia de lugar
                player_y=cr.player.positions_y #Ideal siguiente paso es poenr frames de invlunerabilidad, por mientras esto funciona.
                player_hp-=cr.cero.damage
            elif inmunidad!=1 and player_hp-cr.cero.damage<=0:
                print("💀 cero")
                pygame.mixer.music.stop() 
                if player_pts > 0:
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return menu_principal() 
                else:
                    return low_score_message() # Puntaje 0, mensaje y retorno al menú

        #Con Pigarto
        if pigarto_y[cr.pigarto.pos] == player_y and pigarto_x[cr.pigarto.pos] == player_x and pigarto_exist==1:
            if player_item==item.shield.name:
                cr.pigarto.pos=0
                inmunidad=0
                player_item=""
            elif player_item==item.sword.name:
                if cero_exist==1 or raiznegativa_exist==1: #Comando normal
                    cr.pigarto.hp=cr.pigarto.hp-item.sword.damage
                if cero_exist==0 and raiznegativa_exist==0 and pigarto_exist==1: #Comando cuando sólo queda pigarto
                    pigarto_exist=0
                    pigarto_ratio=9999999
                    COLOR_PIGARTO=COLOR_FLOOR
                    player_pts+=cr.pigarto.pts
                player_item=""
                
                cr.pigarto.pos=0
                if cr.pigarto.hp<=0:
                    player_pts+=cr.pigarto.pts
                    pigarto_exist=0
                    pigarto_x=0
                    pigarto_y=0
                    pigarto_ratio=9999999
                    COLOR_PIGARTO=COLOR_WALL
            elif player_item==item.ring.name:
                player_pts+=cr.pigarto.pts
                COLOR_PIGARTO=COLOR_FLOOR
                player_item=""
                pigarto_exist=0
            elif inmunidad!=1 and player_hp-cr.pigarto.damage>0:
                player_x=cr.player.positions_x #El matemago muere instantaneamente si no se cambia de lugar
                player_y=cr.player.positions_y #Ideal siguiente paso es poenr frames de invlunerabilidad, por mientras esto funciona.
                player_hp-=cr.pigarto.damage
            elif inmunidad!=1 and player_hp-cr.pigarto.damage<=0:
                print("💀 pigarto")
                pygame.mixer.music.stop() 
                if player_pts > 0:
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return menu_principal() 
                else:
                    return low_score_message() # Puntaje 0, mensaje y retorno al menú
            
        #Con Raiz negativa
        if raiznegativa_y == player_y and raiznegativa_x == player_x and raiznegativa_exist==1:
            if player_item==item.shield.name:
                player_pts+=cr.raiznegativa.pts
                COLOR_RAIZ=COLOR_FLOOR
                player_item=""
                raiznegativa_exist=0
                inmunidad=0
                raiznegativa_x=0
                raiznegativa_y=0
                raiznegativa_ratio=9999999
                if pigarto_exist==1 and cero_exist==0:
                    print("espada: cero")
                    COLOR_SWORD=(255, 255, 0)
                    sword_place_y=cr.cero.positions_y
                    sword_place_x=cr.cero.positions_y
            elif player_item==item.sword.name:
                cr.raiznegativa.hp-=item.sword.damage
                player_item=""
                raiznegativa_x=cr.raiznegativa.positions_x
                raiznegativa_y=cr.raiznegativa.positions_y
                if cr.raiznegativa.hp<=0:
                    player_pts+=cr.raiznegativa.pts
                    raiznegativa_exist=0
                    raiznegativa_x=0
                    raiznegativa_y=0
                    raiznegativa_ratio=9999999
                    COLOR_RAIZ=COLOR_FLOOR
            elif inmunidad!=1 and player_hp-cr.raiznegativa.damage>0:
                player_x=cr.player.positions_x #El matemago muere instantaneamente si no se cambia de lugar
                player_y=cr.player.positions_y #Ideal siguiente paso es poenr frames de invlunerabilidad, por mientras esto funciona.
                player_hp-=cr.raiznegativa.damage
            elif inmunidad!=1 and player_hp-cr.raiznegativa.damage<=0:
                print("💀 raiz")
                pygame.mixer.music.stop() 
                if player_pts > 0:
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return menu_principal() 
                else:
                    return low_score_message() # Puntaje 0, mensaje y retorno al menú
        
        #COLISIÓN CON ITEMS
        #Espada
        if sword_place_x==player_x and sword_place_y==player_y:
            player_item=item.sword.name
            sword_place_x=0
            sword_place_y=1
            player_pts+=item.sword.pts
            
        #Escudo
        if shield_place_x==player_x and shield_place_y==player_y:
            player_item=item.shield.name
            inmunidad=1
            shield_place_x=0
            shield_place_y=2
            player_pts+=item.shield.pts
            
        if ring_place_x==player_x and ring_place_y==player_y:
            player_item=item.ring.name
            ring_place_x=0
            ring_place_y=3
            player_pts+=item.ring.pts
            
        # DIBUJO
    
        #Mapa
        for r in range(FILAS):
            for c in range(COLUMNAS):
                rect = pygame.Rect(c*cfg.TILE + cfg.offset_x, r*cfg.TILE + cfg.offset_y, cfg.TILE, cfg.TILE)
                color = COLOR_FLOOR if colision.maze[r][c] >= 1 else COLOR_WALL
                pygame.draw.rect(screen, color, rect)
                
        #HUD provisoria
        if player_hp==1:
            pygame.draw.rect(
                screen, COLOR_HEART,
                (19*cfg.TILE + 6 + cfg.offset_x, 1*cfg.TILE + 6 + cfg.offset_y, cfg.TILE-12, cfg.TILE-12)
            )
        if player_hp>1:
            pygame.draw.rect(
                screen, COLOR_HEART,
                (19*cfg.TILE + 6 + cfg.offset_x, 2*cfg.TILE + 6 + cfg.offset_y, cfg.TILE-12, cfg.TILE-12)
            )
        if player_hp>2:
            pygame.draw.rect(
                screen, COLOR_HEART,
                (19*cfg.TILE + 6 + cfg.offset_x, 3*cfg.TILE + 6 + cfg.offset_y, cfg.TILE-12, cfg.TILE-12)
            )
                
       #   DIBUJAMOS SPRITES
       
       # --- ENEMIGOS ---     
       # Cero
        if cero_exist == 1:
            screen.blit(
                CERO,
                (
                    cero_x * cfg.TILE + cfg.offset_x,
                    cero_y * cfg.TILE + cfg.offset_y
                )
            )
        
        # Pigarto
        if pigarto_exist == 1:
            screen.blit(
                PIGARTO,
                (
                    pigarto_x[cr.pigarto.pos] * cfg.TILE + cfg.offset_x,
                    pigarto_y[cr.pigarto.pos] * cfg.TILE + cfg.offset_y
                )
            )
        
        # Raíz Negativa
        if raiznegativa_exist == 1:
            screen.blit(
                RAIZNEGATIVA,
                (
                    raiznegativa_x * cfg.TILE + cfg.offset_x,
                    raiznegativa_y * cfg.TILE + cfg.offset_y
                )
            )
        
        # --- ITEMS ---
        
        # Espada
        screen.blit(
            ESPADA,
            (
                sword_place_x * cfg.TILE + cfg.offset_x,
                sword_place_y * cfg.TILE + cfg.offset_y
            )
        )
        
        # Escudo
        screen.blit(
            ESCUDO,
            (
                shield_place_x * cfg.TILE + cfg.offset_x,
                shield_place_y * cfg.TILE + cfg.offset_y
            )
        )
        
        # Anillo
        screen.blit(
            ANILLO,
            (
                ring_place_x * cfg.TILE + cfg.offset_x,
                ring_place_y * cfg.TILE + cfg.offset_y
            )
        )
        
        # --- JUGADOR ---
        
        screen.blit(
            MAGO,
            (
                player_x * cfg.TILE + cfg.offset_x,
                player_y * cfg.TILE + cfg.offset_y
            )
        )
        
       
       
        
        temporizador+=1
        
        # Lógica de VICTORIA
        if pigarto_exist==0 and cero_exist==0 and raiznegativa_exist==0:
            running = False
            print("Puntaje sin bonus por tiempo:", player_pts)
            print("Segundos", temporizador/60)
            if temporizador/60<=12:
                player_pts+=2000
                print("TIEMPO INHUMANO") 
            elif temporizador/60<=15:
                player_pts+=1000
            elif temporizador/60<=20:
                player_pts+=500
            elif temporizador/60<=40:
                player_pts+=250
            elif temporizador/60<=60:
                player_pts+=100
            elif temporizador/60>60:
                player_pts+=0
                                
            pygame.mixer.music.stop() 
            # Llama a guardar puntaje con el orden corregido (screen, player_pts)
            cfg.guardar_nuevo_puntaje(SCREEN, player_pts) 
            print("Puntaje total:", player_pts)
            return menu_principal() # Regresa al menú principal
    
        
        mostrar_puntaje(player_pts)
        pygame.display.flip()

    # Si sale del bucle 'while running' por QUIT o ESCAPE, regresa al menú
    return menu_principal()


# --- PANTALLA MARCADORES (CORREGIDA LA SALIDA) ---

def marcadores():
    top_scores = cfg.cargar_mejores_puntajes()
    
    x_pos = cfg.CENTRO_X
    y_start = cfg.CENTRO_Y - 140
    line_spacing = 70

    while True:
        POS_MOUSE_MARCADORES = pygame.mouse.get_pos()
        SCREEN.fill("#333333") 

        TEXTO_TITULO = cfg.get_letra(60).render("MEJORES PUNTAJES", True, "#FFD700") 
        RECT_TITULO = TEXTO_TITULO.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 280))
        SCREEN.blit(TEXTO_TITULO, RECT_TITULO)
        
        if top_scores:
            for i, score_data in enumerate(top_scores):
                # Usamos .get() para seguridad
                nombre = score_data.get("nombre", "N/A")
                puntaje = score_data.get("player_pts", 0)
                
                score_text = f"{i+1}. {nombre} - {puntaje}"
                
                TEXTO_SCORE = cfg.get_letra(40).render(score_text, True, "White")
                
                RECT_SCORE = TEXTO_SCORE.get_rect(center=(x_pos, y_start + i * line_spacing))
                SCREEN.blit(TEXTO_SCORE, RECT_SCORE)
        else:
            TEXTO_SIN_SCORES = cfg.get_letra(30).render("Aún no hay puntajes registrados.", True, "White")
            RECT_SIN_SCORES = TEXTO_SIN_SCORES.get_rect(center=(x_pos, y_start))
            SCREEN.blit(TEXTO_SIN_SCORES, RECT_SIN_SCORES)
        
        VOLVER_MARCADORES = Button(image=pygame.image.load("./assets/Options Rect.png"), pos=(cfg.CENTRO_X, y_start + len(top_scores) * line_spacing + 100), 
                            text_input="VOLVER", font=cfg.get_letra(75), base_color="White", hovering_color="Red")
        VOLVER_MARCADORES.changeColor(POS_MOUSE_MARCADORES)
        VOLVER_MARCADORES.update(SCREEN)

        for event in pygame.event.get():
            manejar_salida_menu(event) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VOLVER_MARCADORES.checkForInput(POS_MOUSE_MARCADORES):
                    return menu_principal() # Usar return para volver

        pygame.display.update()

# --- PANTALLA MANUAL (CORREGIDA LA SALIDA) ---

def manual():
    print("ENTRANDO A LA PANTALLA DE MANUAL")
    while True:
        POS_MOUSE_MANUAL = pygame.mouse.get_pos()
        SCREEN.fill("gray")
        # Título del manual
        TEXTO_MANUAL = cfg.get_letra(45).render("MANUAL EL MATEMAGO.", True, "Black")
        RECT_MANUAL = TEXTO_MANUAL.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 100))
        SCREEN.blit(TEXTO_MANUAL, RECT_MANUAL)
        #BOTÓN PARA ABRIR EL PDF
        BOTON_PDF = Button(
            # imagen del botón
            image=pygame.image.load("./assets/Options Rect.png"),
            # posición central
            pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 0),
            # texto dentro del botón
            text_input="ABRIR PDF",
            font=cfg.get_letra(55),
            base_color="Black",
            hovering_color="Blue"
        )
        BOTON_PDF.changeColor(POS_MOUSE_MANUAL)
        BOTON_PDF.update(SCREEN)

        VOLVER_MANUAL = Button(image=pygame.image.load("./assets/Options Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 150), 
                            text_input="VOLVER", font=cfg.get_letra(75), base_color="Black", hovering_color="Red")
        VOLVER_MANUAL.changeColor(POS_MOUSE_MANUAL)
        VOLVER_MANUAL.update(SCREEN)

        for event in pygame.event.get():
            manejar_salida_menu(event) 
            # Detectar clic del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Abrir pdf
                if BOTON_PDF.checkForInput(POS_MOUSE_MANUAL):
                    # Ruta del archivo PDF dentro de la carpeta assets
                    ruta_pdf = os.path.join("assets", "Manual de Matemago.pdf")
                    print("ABRIENDO PDF:", ruta_pdf)
                    # En Windows: abre el PDF con el programa predeterminado (Adobe, E
                    try:
                        os.startfile(ruta_pdf)  
                    except:
                        # En Mac o Linux: usa el comando "open" para abrir el archivo
                        os.system(f"open {ruta_pdf}")
                        

                if VOLVER_MANUAL.checkForInput(POS_MOUSE_MANUAL):
                    return menu_principal() # Usar return para volver
        
        pygame.display.update()

# --- PANTALLA OPCIONES (CORREGIDA LA SALIDA) ---

def opciones():
    # Variable de control: indica si el usuario está arrastrando el slider
    mouse_held = False
    while True:
         # Posición actual del mouse
        POS = pygame.mouse.get_pos()
        SCREEN.fill("white")
        TEXTO_OP = cfg.get_letra(70).render("OPCIONES", True, "Black")
        SCREEN.blit(TEXTO_OP, TEXTO_OP.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 260)))
        
        # Texto que muestra el volumen actual en porcentaje

        TEXTO_VOL = cfg.get_letra(40).render(f"VOLUMEN: {int(cfg.VOLUMEN_GLOBAL*100)}%", True, "Black")
        SCREEN.blit(TEXTO_VOL, TEXTO_VOL.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 180)))
        
        # --- SLIDER (asume variables cfg.* definidas) ---
        
        #Dibujar la barra del slider (rectángulo gris), configuracion declarada en configuracion.py
        pygame.draw.rect(SCREEN, "gray", (cfg.SLIDER_X, cfg.SLIDER_Y, cfg.SLIDER_WIDTH, cfg.SLIDER_HEIGHT))
        # Dibujar la bolita del slider (círculo negro)
        pygame.draw.circle(SCREEN, "black", (cfg.SLIDER_HANDLE_X, cfg.SLIDER_Y + cfg.SLIDER_HEIGHT//2), cfg.HANDLE_RADIUS)

        VOLVER = Button(
            image=pygame.image.load("./assets/Play Rect.png"),
            pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 150),
            text_input="VOLVER",
            font=cfg.get_letra(60),
            base_color="black",
            hovering_color="red"
        )
        VOLVER.changeColor(POS)
        VOLVER.update(SCREEN)

        # EVENTOS
        for event in pygame.event.get():
            manejar_salida_menu(event) 
            # Cuando el usuario hace clic con el mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Detecta si el clic ocurrió sobre la bolita del slider
                #Revisa si la posición horizontal del mouse está dentro del área de la bolita del slider.
                #centro menos el radio
                if (cfg.SLIDER_HANDLE_X - cfg.HANDLE_RADIUS <= POS[0] <= cfg.SLIDER_HANDLE_X + cfg.HANDLE_RADIUS
                    and cfg.SLIDER_Y - 10 <= POS[1] <= cfg.SLIDER_Y + 30):
                     # El usuario está agarrando el slider -> activar arrastre
                    mouse_held = True
                if VOLVER.checkForInput(POS):
                    return menu_principal() # Usar return para volver
                 # Cuando el usuario suelta el clic -> dejar de arrastrar
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False
        #Configuracion mientras se arrastra
        
        # Mover la bolita con el mouse pero sin salirse de la barra
        if mouse_held:
            cfg.SLIDER_HANDLE_X = max(cfg.SLIDER_X, min(POS[0], cfg.SLIDER_X + cfg.SLIDER_WIDTH))
             # Convertir la posición de la bolita en un valor entre 0.0 y 1.0
            cfg.VOLUMEN_GLOBAL = (cfg.SLIDER_HANDLE_X - cfg.SLIDER_X) / cfg.SLIDER_WIDTH
         # Aplicar el volumen actualizado a la música
        pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL)
        # Actualizar la pantalla
        pygame.display.update()

# --- BUCLE PRINCIPAL DEL MENÚ (CORREGIDA LA SALIDA) ---

def menu_principal():
    
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(cfg.RUTA_MUSICA_MENU)
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL)
        
    SCREEN.fill((0, 0, 0))
    pygame.display.update()
    
    while True:
        
        SCREEN.fill((0, 0, 0)) 
        POS_MOUSE_MENU = pygame.mouse.get_pos()
        
        # Título del juego
        TEXTO_MENU = cfg.get_letra(85).render("EL MATEMAGO", True, "#b68f40") 
        RECT_MENU = TEXTO_MENU.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 260))
        SCREEN.blit(TEXTO_MENU, RECT_MENU)
        
        # Definición de los botones
        BOTON_JUGAR = Button(image=pygame.image.load("./assets/Play Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y - 150), 
                            text_input="JUGAR", font=cfg.get_letra(60), base_color="#d7fcd4", hovering_color="White")
        BOTON_MARCADORES = Button(image=pygame.image.load("./assets/Options Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y - 50), 
                            text_input="MARCADORES", font=cfg.get_letra(55), base_color="#d7fcd4", hovering_color="White")
        BOTON_MANUAL = Button(image=pygame.image.load("./assets/Play Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 50), 
                            text_input="MANUAL", font=cfg.get_letra(55), base_color="#d7fcd4", hovering_color="White")
        BOTON_OPCIONES = Button(image=pygame.image.load("./assets/Options Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 150), 
                            text_input="OPCIONES", font=cfg.get_letra(60), base_color="#d7fcd4", hovering_color="White")
        BOTON_SALIR = Button(image=pygame.image.load("./assets/Play Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 250), 
                            text_input="SALIR", font=cfg.get_letra(60), base_color="#d7fcd4", hovering_color="Red")
        
        for button in [BOTON_JUGAR, BOTON_MARCADORES, BOTON_MANUAL, BOTON_OPCIONES, BOTON_SALIR]:
            button.changeColor(POS_MOUSE_MENU)
            button.update(SCREEN)
        
        # Manejo de eventos
        for event in pygame.event.get():
            manejar_salida_menu(event) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOTON_JUGAR.checkForInput(POS_MOUSE_MENU):
                    jugar()
                if BOTON_MARCADORES.checkForInput(POS_MOUSE_MENU):
                    marcadores()
                if BOTON_MANUAL.checkForInput(POS_MOUSE_MENU):
                    manual()
                if BOTON_OPCIONES.checkForInput(POS_MOUSE_MENU):
                    opciones()
                if BOTON_SALIR.checkForInput(POS_MOUSE_MENU):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
 

menu_principal()