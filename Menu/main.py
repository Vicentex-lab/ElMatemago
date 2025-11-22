import pygame, sys
import os # Necesario para la función manual()
# import json, os # Ya no son necesarios aquí si están en configuracion.py
from button import Button
import colisiones as colision
import criaturas as cr

# --- IMPORTACIÓN DE CONFIGURACIÓN ---
# Importa todo lo que necesitamos del nuevo archivo
import configuracion as cfg

# Inicializa Pygame
pygame.init() 
pygame.mixer.init() # Inicializa el módulo de mezcla de sonido

# Define la pantalla en modo Fullscreen usando las variables de configuracion.py
SCREEN = pygame.display.set_mode((cfg.ANCHO_PANTALLA, cfg.ALTO_PANTALLA), pygame.FULLSCREEN) 
pygame.display.set_caption("EL MATEMAGO") 

# Carga y escala la imagen de fondo para ajustarse a Fullscreen
BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (cfg.ANCHO_PANTALLA, cfg.ALTO_PANTALLA))

# --- PANTALLA JUGAR ---

def jugar():
    #Muestra la pantalla de juego, detiene la música del menú e inicia la música de juego.
    RUTA_MUSICA_JUEGO = "assets/Pacmanwaka.wav"
    
    # 1. Detiene la música actual (la del menú)
    pygame.mixer.music.stop()
    
    # 2. Carga y reproduce la música del juego en loop
    
    """try:
        pygame.mixer.music.load(cfg.RUTA_MUSICA_JUEGO) # Usar cfg.RUTA_MUSICA_JUEGO
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL) # Usar cfg.VOLUMEN_GLOBAL
    except pygame.error as e:
        print(f"Error al cargar la música del juego: {e}")"""
    
    while True:
        TILE = 32
        FPS = 60
        
        FILAS = len(colision.maze)
        COLUMNAS = len(colision.maze[0])
        screen = pygame.display.set_mode((COLUMNAS*TILE, FILAS*TILE))
        clock = pygame.time.Clock()
        
        COLOR_WALL = (30,30,30)
        COLOR_FLOOR = (240,240,240)
        COLOR_PLAYER = (0,120,255)
        COLOR_ENEMY = (255,50,50)
        
        screen = pygame.display.set_mode((COLUMNAS*TILE, FILAS*TILE))
        clock = pygame.time.Clock()
        
        player_y = cr.player.positions_y   # (Y donde quieres ponerlo)
        player_x = cr.player.positions_x   # (X donde quieres ponerlo)
        
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

        cero_cooldown = 0
        
        # ---------------------------
        # Pigarto
        # ---------------------------
        pigarto_y = cr.pigarto.positions_y
        pigarto_x = cr.pigarto.positions_x
        pigarto_cooldown = 0
        
        # ---------------------------
        # Raíz Negativa
        # ---------------------------
        raiznegativa_y = cr.raiznegativa.positions_y
        raiznegativa_x = cr.raiznegativa.positions_x
        raiznegativa_cooldown = 0

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

        
        # MOVIMIENTO DEL JUGADOR 
        
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
                        # ARRIBA (W o Flecha ↑)
                        if (event.key == pygame.K_w or event.key == pygame.K_UP) and can_move(player_y - 1, player_x):
                            player_y -= 1
                            print("Y", player_y, "X", player_x)
                            eventos()
                        # ABAJO (S o Flecha ↓)
                        if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and can_move(player_y + 1, player_x):
                            player_y += 1
                            print("Y", player_y, "X", player_x)
                            eventos()
                        # IZQUIERDA (A o Flecha ←)
                        if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and can_move(player_y, player_x - 1):
                            player_x -= 1
                            print("Y", player_y, "X", player_x)
                            eventos()
                        # DERECHA (D o Flecha →)
                        if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and can_move(player_y, player_x + 1):
                            player_x += 1
                            print("Y", player_y, "X", player_x)
                            eventos()
                        move_cooldown = True
        
                if event.type == pygame.KEYUP:
                    move_cooldown = False
                    
            # ---------------------------
            # MOVER ENEMIGO
            # ---------------------------
            #Cero
            ahora = pygame.time.get_ticks()
            if ahora - cero_cooldown >= cr.cero.movement_ratio:
                cero_y, cero_x = mover_enemigo(cero_y, cero_x, player_y, player_x)
                cero_cooldown = ahora

            #Pigarto
            if ahora - pigarto_cooldown >= cr.pigarto.movement_ratio:
                if cr.pigarto.pos<106:
                    cr.pigarto.pos = cr.pigarto.pos+1
                    pigarto_cooldown=ahora
                if cr.pigarto.pos>=106:
                    cr.pigarto.pos=0
                    pigarto_cooldown=ahora
                    
            #Raiz negativa
            if ahora - raiznegativa_cooldown >= cr.raiznegativa.movement_ratio:
                raiznegativa_y, raiznegativa_x = mover_enemigo(raiznegativa_y, raiznegativa_x, player_y, player_x)
                raiznegativa_cooldown = ahora
                #cr.raiznegativa.estocada() #No funciona
            # ---------------------------
            # COLISIÓN
            # ---------------------------
            
            #Con CERO
            if cero_y == player_y and cero_x == player_x:
                print("💀 Te atrapó el enemigo!")
                running = False

            #Con Pigarto
            if pigarto_y[cr.pigarto.pos] == player_y and pigarto_x[cr.pigarto.pos] == player_x:
                print("💀 Te atrapó el enemigo!")
                running = False
                
            #Con Raiz negativa
            if raiznegativa_y == player_y and raiznegativa_x == player_x:
                print("💀 Te atrapó el enemigo!")
                running = False
                
            # DIBUJO
        
            #Mapa
            for r in range(FILAS):
                for c in range(COLUMNAS):
                    rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
                    color = COLOR_FLOOR if colision.maze[r][c] >= 1 else COLOR_WALL
                    pygame.draw.rect(screen, color, rect)
                    
            #Enemigo
            #Cero
            pygame.draw.rect(
            screen, COLOR_ENEMY,
            (cero_x*TILE + 6, cero_y*TILE + 6, TILE-12, TILE-12)
            )

            #Pigarto
            pygame.draw.rect(
            screen, COLOR_ENEMY,
            (pigarto_x[cr.pigarto.pos]*TILE + 6, pigarto_y[cr.pigarto.pos]*TILE + 6, TILE-12, TILE-12)
            )
            
            #Raiz Negativa
            pygame.draw.rect(
                screen, (0, 255, 0),
                (raiznegativa_x*TILE + 6, raiznegativa_y*TILE + 6, TILE-12, TILE-12)
            )
        
            # Jugador
            pygame.draw.rect(
                screen,
                COLOR_PLAYER,
                (player_x*TILE + 4, player_y*TILE + 4, TILE-8, TILE-8)
            )
        
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

# --- PANTALLA MARCADORES ---

def marcadores():
    #Muestra el top 3 de puntajes en una pantalla dedicada.
    top_scores = cfg.cargar_mejores_puntajes()
    
    x_pos = cfg.CENTRO_X
    y_start = cfg.CENTRO_Y - 140 # Ajustar Y inicial para centrar la lista
    line_spacing = 70 # Espaciado vertical entre cada marcador

    while True:
        POS_MOUSE_MARCADORES = pygame.mouse.get_pos()
        SCREEN.fill("#333333") # Fondo oscuro

        # Renderiza el título de la pantalla
        TEXTO_TITULO = cfg.get_letra(60).render("MEJORES PUNTAJES", True, "#FFD700") # Dorado
        RECT_TITULO = TEXTO_TITULO.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 280))
        SCREEN.blit(TEXTO_TITULO, RECT_TITULO)
        
        # Muestra los puntajes cargados
        if top_scores:
            for i, score_data in enumerate(top_scores):
                nombre = score_data.get("nombre", "N/A")
                puntaje = score_data.get("puntaje", 0)
                
                # Construye el texto: i+1 da la posición (1, 2, 3)
                score_text = f"{i+1}. {nombre} - {puntaje}"
                
                # Renderiza el texto
                TEXTO_SCORE = cfg.get_letra(40).render(score_text, True, "White")
                
                # Calcula la posición y lo dibuja
                RECT_SCORE = TEXTO_SCORE.get_rect(center=(x_pos, y_start + i * line_spacing))
                SCREEN.blit(TEXTO_SCORE, RECT_SCORE)
        else:
            # Mensaje si no hay puntajes
            TEXTO_SIN_SCORES = cfg.get_letra(30).render("Aún no hay puntajes registrados.", True, "White")
            RECT_SIN_SCORES = TEXTO_SIN_SCORES.get_rect(center=(x_pos, y_start))
            SCREEN.blit(TEXTO_SIN_SCORES, RECT_SIN_SCORES)
        
        # Botón para volver al menú principal
        VOLVER_MARCADORES = Button(image=None, pos=(cfg.CENTRO_X, y_start + len(top_scores) * line_spacing + 100), 
                            text_input="VOLVER", font=cfg.get_letra(75), base_color="White", hovering_color="Red")
        VOLVER_MARCADORES.changeColor(POS_MOUSE_MARCADORES)
        VOLVER_MARCADORES.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VOLVER_MARCADORES.checkForInput(POS_MOUSE_MARCADORES):
                    menu_principal()
        
        pygame.display.update()

# --- PANTALLA MANUAL ---

def manual():
    #Muestra la pantalla del manual de juego.
    print("Entrando a la pantalla de MANUAL")
    while True:
        POS_MOUSE_MANUAL = pygame.mouse.get_pos()
        SCREEN.fill("gray")
        TEXTO_MANUAL = cfg.get_letra(45).render("Manual Matemagia.", True, "Black")
        RECT_MANUAL = TEXTO_MANUAL.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 100))
        SCREEN.blit(TEXTO_MANUAL, RECT_MANUAL)

        # --- Botón para abrir el PDF ---
        BOTON_PDF = Button(
            image=None,
            pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 0),
            text_input="ABRIR PDF",
            font=cfg.get_letra(55),
            base_color="Black",
            hovering_color="Blue"
        )
        BOTON_PDF.changeColor(POS_MOUSE_MANUAL)
        BOTON_PDF.update(SCREEN)

        # Botón de regreso
        VOLVER_MANUAL = Button(image=None, pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 150), 
                            text_input="VOLVER", font=cfg.get_letra(75), base_color="Black", hovering_color="Red")
        VOLVER_MANUAL.changeColor(POS_MOUSE_MANUAL)
        VOLVER_MANUAL.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                # --- Abrir PDF ---
                if BOTON_PDF.checkForInput(POS_MOUSE_MANUAL):
                    ruta_pdf = os.path.join("assets", "manual_matemagia.pdf")
                    print("Abriendo PDF:", ruta_pdf)
                    try:
                        os.startfile(ruta_pdf)  # WINDOWS
                    except:
                        print("No se pudo abrir el PDF.")

                if VOLVER_MANUAL.checkForInput(POS_MOUSE_MANUAL):
                    menu_principal()
        
        pygame.display.update()

# --- PANTALLA OPCIONES ---

def opciones():
    mouse_held = False  # Para arrastrar
    while True:
        POS = pygame.mouse.get_pos()
        SCREEN.fill("white")
        # Título
        TEXTO_OP = cfg.get_letra(70).render("OPCIONES", True, "Black")
        SCREEN.blit(TEXTO_OP, TEXTO_OP.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 260)))

        # Texto volumen
        TEXTO_VOL = cfg.get_letra(40).render(f"Volumen: {int(cfg.VOLUMEN_GLOBAL*100)}%", True, "Black")
        SCREEN.blit(TEXTO_VOL, TEXTO_VOL.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 180)))
        # --- SLIDER ---
        # Barra
        pygame.draw.rect(SCREEN, "gray", (cfg.SLIDER_X, cfg.SLIDER_Y, cfg.SLIDER_WIDTH, cfg.SLIDER_HEIGHT))

        # Handle
        pygame.draw.circle(SCREEN, "black", (cfg.SLIDER_HANDLE_X, cfg.SLIDER_Y + cfg.SLIDER_HEIGHT//2), cfg.HANDLE_RADIUS)

        # Botón volver
        VOLVER = Button(
            image=None,
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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Comenzar arrastre
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (cfg.SLIDER_HANDLE_X - cfg.HANDLE_RADIUS <= POS[0] <= cfg.SLIDER_HANDLE_X + cfg.HANDLE_RADIUS
                    and cfg.SLIDER_Y - 10 <= POS[1] <= cfg.SLIDER_Y + 30):
                    mouse_held = True

                if VOLVER.checkForInput(POS):
                    return menu_principal()

            # Terminar arrastre
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

        # Si se mantiene click, mover el handle
        if mouse_held:
            cfg.SLIDER_HANDLE_X = max(cfg.SLIDER_X, min(POS[0], cfg.SLIDER_X + cfg.SLIDER_WIDTH))
            cfg.VOLUMEN_GLOBAL = (cfg.SLIDER_HANDLE_X - cfg.SLIDER_X) / cfg.SLIDER_WIDTH
        pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL)
        pygame.display.update()

# --- BUCLE PRINCIPAL DEL MENÚ ---

def menu_principal():
    """Muestra el menú principal y maneja la navegación y la música de fondo."""
    
    # Lógica de la música: Solo carga y reproduce la música del menú si no hay nada sonando
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(cfg.RUTA_MUSICA_MENU)
        pygame.mixer.music.play(-1) # Reproducción en loop
        pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL) # Usar el volumen global
    
    while True:
        
        SCREEN.blit(BG, (0, 0)) # Dibuja el fondo
        POS_MOUSE_MENU = pygame.mouse.get_pos() # Obtiene la posición del mouse
        
        # Título del juego
        TEXTO_MENU = cfg.get_letra(85).render("EL MATEMAGO", True, "#b68f40") 
        RECT_MENU = TEXTO_MENU.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 260))
        SCREEN.blit(TEXTO_MENU, RECT_MENU)
        
        # Definición de los botones
        BOTON_JUGAR = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y - 150), 
                            text_input="JUGAR", font=cfg.get_letra(60), base_color="#d7fcd4", hovering_color="White")
        BOTON_MARCADORES = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y - 50), 
                            text_input="MARCADORES", font=cfg.get_letra(55), base_color="#d7fcd4", hovering_color="White")
        BOTON_MANUAL = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 50), 
                            text_input="MANUAL", font=cfg.get_letra(55), base_color="#d7fcd4", hovering_color="White")
        BOTON_OPCIONES = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 150), 
                            text_input="OPCIONES", font=cfg.get_letra(60), base_color="#d7fcd4", hovering_color="White")
        BOTON_SALIR = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 250), 
                            text_input="SALIR", font=cfg.get_letra(60), base_color="#d7fcd4", hovering_color="White")
        # Renderiza los botones y actualiza el color al pasar el mouse
        for button in [BOTON_JUGAR, BOTON_MARCADORES, BOTON_MANUAL, BOTON_OPCIONES, BOTON_SALIR]:
            button.changeColor(POS_MOUSE_MENU)
            button.update(SCREEN)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Lógica de click en cada botón, llamando a la función correspondiente
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

        pygame.display.update() # Actualiza toda la pantalla


menu_principal()