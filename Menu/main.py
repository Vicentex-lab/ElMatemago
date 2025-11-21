import pygame, sys
import json, os
from button import Button # Importa la clase Button para manejar botones interactivos
import colisiones as colision


pygame.init() # Inicializa todos los módulos necesarios de Pygame

SCREEN = pygame.display.set_mode((1280, 720)) # Define el tamaño de la ventana
pygame.display.set_caption("EL MATEMAGO") # Establece el título de la ventana

# Carga la imagen de fondo
BG = pygame.image.load("assets/Background.png")

# Inicializa el módulo de mezcla de sonido
pygame.mixer.init()
# Define la ruta de la música para el menú. Debe ser una cadena de texto (string).
RUTA_MUSICA_MENU = "./assets/DDO-Music-Tavern-2.mp3" 

# Define la ruta del archivo JSON para guardar los puntajes
RUTA_PUNTAJES = "puntajes.json"

# --- FUNCIONES DE UTILIDAD ---

def get_letra(size): 
    #Carga y devuelve la fuente 'font.ttf' en el tamaño especificado.
    return pygame.font.Font("assets/prstart.ttf", size)

# --- FUNCIONES DE PUNTAJES ---

def cargar_mejores_puntajes():
    """Carga todos los puntajes del archivo JSON, los ordena y devuelve el top 3."""
    if not os.path.exists(RUTA_PUNTAJES):
        # Si el archivo no existe, no hay puntajes para mostrar
        return []

    try:
        with open(RUTA_PUNTAJES, "r") as archivo:
            puntajes = json.load(archivo)
            # Ordena los puntajes de forma descendente (reverse=True) usando el valor de 'puntaje' como clave de ordenamiento
            puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)
            return puntajes_ordenados[:3] # Devuelve solo los 3 mejores
    except (json.JSONDecodeError, FileNotFoundError):
        # Maneja errores si el archivo está vacío, corrupto o si la ruta es incorrecta
        return []

# --- PANTALLA JUGAR ---

def jugar():
    #Muestra la pantalla de juego, detiene la música del menú e inicia la música de juego.
    RUTA_MUSICA_JUEGO = "assets/Pacmanwaka.wav"
    
    # 1. Detiene la música actual (la del menú)
    pygame.mixer.music.stop()
    
    # 2. Carga y reproduce la música del juego en loop
    """try:
        pygame.mixer.music.load(RUTA_MUSICA_JUEGO)
        pygame.mixer.music.play(-1) # -1 significa loop infinito
        pygame.mixer.music.set_volume(0.1)
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
                nonlocal player_f
                nonlocal player_c
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

# --- PANTALLA MARCADORES ---

def marcadores():
    #Muestra el top 3 de puntajes en una pantalla dedicada.
    top_scores = cargar_mejores_puntajes()
    
    x_pos = 640
    y_start = 220
    line_spacing = 70 # Espaciado vertical entre cada marcador

    while True:
        POS_MOUSE_MARCADORES = pygame.mouse.get_pos()
        SCREEN.fill("#333333") # Fondo oscuro

        # Renderiza el título de la pantalla
        TEXTO_TITULO = get_letra(60).render("MEJORES PUNTAJES", True, "#FFD700") # Dorado
        RECT_TITULO = TEXTO_TITULO.get_rect(center=(640, 80))
        SCREEN.blit(TEXTO_TITULO, RECT_TITULO)
        
        # Muestra los puntajes cargados
        if top_scores:
            for i, score_data in enumerate(top_scores):
                nombre = score_data.get("nombre", "N/A")
                puntaje = score_data.get("puntaje", 0)
                
                # Construye el texto: i+1 da la posición (1, 2, 3)
                score_text = f"{i+1}. {nombre} - {puntaje}"
                
                # Renderiza el texto
                TEXTO_SCORE = get_letra(40).render(score_text, True, "White")
                
                # Calcula la posición y lo dibuja
                RECT_SCORE = TEXTO_SCORE.get_rect(center=(x_pos, y_start + i * line_spacing))
                SCREEN.blit(TEXTO_SCORE, RECT_SCORE)
        else:
            # Mensaje si no hay puntajes
            TEXTO_SIN_SCORES = get_letra(30).render("Aún no hay puntajes registrados.", True, "White")
            RECT_SIN_SCORES = TEXTO_SIN_SCORES.get_rect(center=(x_pos, y_start))
            SCREEN.blit(TEXTO_SIN_SCORES, RECT_SIN_SCORES)
        
        # Botón para volver al menú principal
        VOLVER_MARCADORES = Button(image=None, pos=(640, y_start + len(top_scores) * line_spacing + 100), 
                            text_input="VOLVER", font=get_letra(75), base_color="White", hovering_color="Red")
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
        TEXTO_MANUAL = get_letra(45).render("Acá va el manual.", True, "Black")
        RECT_MANUAL = TEXTO_MANUAL.get_rect(center=(640, 260))
        SCREEN.blit(TEXTO_MANUAL, RECT_MANUAL)
        
        # Botón de regreso
        VOLVER_MANUAL = Button(image=None, pos=(640, 460), 
                            text_input="VOLVER", font=get_letra(75), base_color="Black", hovering_color="Red")
        VOLVER_MANUAL.changeColor(POS_MOUSE_MANUAL)
        VOLVER_MANUAL.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VOLVER_MANUAL.checkForInput(POS_MOUSE_MANUAL):
                    # No detenemos la música si es la del menú
                    menu_principal()
        
        pygame.display.update()
   

# --- PANTALLA OPCIONES ---

def opciones():
    #Muestra la pantalla de opciones.
    while True:
        POS_MOUSE_OPCIONES = pygame.mouse.get_pos()
        SCREEN.fill("white")
        
        TEXTO_OPCIONES = get_letra(35).render("Acá van las opciones (si es que))", True, "Black")
        RECT_OPCIONES = TEXTO_OPCIONES.get_rect(center=(640, 260))
        SCREEN.blit(TEXTO_OPCIONES, RECT_OPCIONES)
        
        # Botón de regreso
        VOLVER_OPCIONES = Button(image=None, pos=(640, 460), 
                            text_input="VOLVER", font=get_letra(75), base_color="Black", hovering_color="Green")
        VOLVER_OPCIONES.changeColor(POS_MOUSE_OPCIONES)
        VOLVER_OPCIONES.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VOLVER_OPCIONES.checkForInput(POS_MOUSE_OPCIONES):
                    menu_principal()
        pygame.display.update()

# --- BUCLE PRINCIPAL DEL MENÚ ---

def menu_principal():
    """Muestra el menú principal y maneja la navegación y la música de fondo."""
    
    # Lógica de la música: Solo carga y reproduce la música del menú si no hay nada sonando
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(RUTA_MUSICA_MENU)
        pygame.mixer.music.play(-1) # Reproducción en loop
        pygame.mixer.music.set_volume(0.5) # Volumen bajo
    
    while True:
        
        SCREEN.blit(BG, (0, 0)) # Dibuja el fondo
        POS_MOUSE_MENU = pygame.mouse.get_pos() # Obtiene la posición del mouse
        
        # Título del juego
        TEXTO_MENU = get_letra(85).render("EL MATEMAGO", True, "#b68f40") 
        RECT_MENU = TEXTO_MENU.get_rect(center=(640, 80))
        SCREEN.blit(TEXTO_MENU, RECT_MENU)
        
        # Definición de los botones
        BOTON_JUGAR = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 190), 
                            text_input="JUGAR", font=get_letra(60), base_color="#d7fcd4", hovering_color="White")
        BOTON_MARCADORES = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 290), 
                            text_input="MARCADORES", font=get_letra(55), base_color="#d7fcd4", hovering_color="White")
        BOTON_MANUAL = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 390), 
                            text_input="MANUAL", font=get_letra(55), base_color="#d7fcd4", hovering_color="White")
        BOTON_OPCIONES = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 490), 
                            text_input="OPCIONES", font=get_letra(60), base_color="#d7fcd4", hovering_color="White")
        BOTON_SALIR = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 590), 
                            text_input="SALIR", font=get_letra(60), base_color="#d7fcd4", hovering_color="White")

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