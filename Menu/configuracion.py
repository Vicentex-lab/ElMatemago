import pygame
import json
import os
import colisiones 


# Inicializa Pygame para poder usar pygame.display.Info()
pygame.init() 

# --- CONFIGURACIÓN DE PANTALLA ---
# Obtiene la resolución actual de la pantalla para usarla en el modo Fullscreen
INFO_PANTALLA = pygame.display.Info()
ANCHO_PANTALLA = INFO_PANTALLA.current_w
ALTO_PANTALLA = INFO_PANTALLA.current_h

# Define el centro de la pantalla, que usaremos para centrar los elementos
CENTRO_X = ANCHO_PANTALLA // 2
CENTRO_Y = ALTO_PANTALLA // 2

# --- CONFIGURACIÓN DEL LABERINTO ---
TILE = 32 # Tamaño de cada celda del laberinto
FILAS_LABERINTO = len(colisiones.maze)
COLUMNAS_LABERINTO = len(colisiones.maze[0])

# --- CÁLCULO PARA CENTRAR EL LABERINTO EN PANTALLA COMPLETA ---
ANCHO_LABERINTO = COLUMNAS_LABERINTO * TILE
ALTO_LABERINTO = FILAS_LABERINTO * TILE

# Centramos el laberinto usando el centro de la pantalla (cfg.CENTRO_X/Y)     
# offset_x: Distancia desde el borde izquierdo hasta donde debe empezar el laberinto.
# Se obtiene restando la mitad del ancho del laberinto al centro X de la pantalla.
offset_x = CENTRO_X - (ANCHO_LABERINTO // 2)
        
 # offset_y: Distancia desde el borde superior hasta donde debe empezar el laberinto.
# Se obtiene restando la mitad del alto del laberinto al centro Y de la pantalla.
offset_y = CENTRO_Y - (ALTO_LABERINTO // 2)

# --- VARIABLES GLOBALES DE JUEGO ---
VOLUMEN_GLOBAL = 0.5
RUTA_MUSICA_MENU = "./assets/Matemago_Menu_Song.mp3" 
RUTA_MUSICA_JUEGO = "./assets/Matemago_Dungeon_Song.mp3"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PUNTAJES = os.path.join(BASE_DIR, "puntajes.json")

# --- CONFIGURACIÓN DEL SLIDER DE VOLUMEN ---
SLIDER_WIDTH = 500
SLIDER_HEIGHT = 10
# Posición X calculada para centrar el SLIDER
SLIDER_X = CENTRO_X - (SLIDER_WIDTH // 2)  
SLIDER_Y = CENTRO_Y - 80 
SLIDER_HANDLE_X = SLIDER_X + int(SLIDER_WIDTH * VOLUMEN_GLOBAL)
HANDLE_RADIUS = 15

# --- FUNCIONES DE UTILIDAD ---

def get_letra(size): 
    """Carga y devuelve la fuente 'font.ttf' en el tamaño especificado."""
    return pygame.font.Font("./assets/prstart.ttf", size)

def cargar_mejores_puntajes():
    """Carga todos los puntajes del archivo JSON, los ordena y devuelve el top 3."""
    if not os.path.exists(RUTA_PUNTAJES):
        return []
    try:
        with open(RUTA_PUNTAJES, "r") as archivo:
            puntajes = json.load(archivo)
            # Ordena los puntajes de forma descendente (reverse=True)
            puntajes_ordenados = sorted(puntajes, key=lambda x: x["player_pts"], reverse=True)
            return puntajes_ordenados[:3] # Devuelve solo los 3 mejores
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
def obtener_nombre(screen, player_pts):
    # Inicialización de variables de entrada de texto
    nombre = ''
    textbox = True
    
    # Colores
    COLOR_TEXTO = (255, 255, 255) # Blanco
    COLOR_FONDO_CAJA = (50, 50, 50) # Gris oscuro
    COLOR_CURSOR = (255, 255, 0) # Amarillo
    
    # Rectángulo de la caja de texto
    try:
        INPUT_RECT = pygame.Rect(CENTRO_X-300 , CENTRO_Y+50, 600, 60)
    except NameError:
        # Fallback si CENTRO_X y CENTRO_Y no están definidos
        screen_width, screen_height = screen.get_size()
        CENTRO_X = screen_width // 2
        CENTRO_Y = screen_height // 2
        INPUT_RECT = pygame.Rect(CENTRO_X - 300, CENTRO_Y + 50, 600, 60)
    
    # Bucle principal de entrada de nombre
    while textbox:
        # 1. PROCESAMIENTO DE EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Validar al presionar ENTER
                    if nombre.strip() != "" and nombre.replace(' ', '').isalpha():
                        textbox = False # Salir del bucle while
                    else:
                        print("❌ Nombre inválido. Solo letras y no vacío.")
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    # Capturar la tecla y validar que sea una letra o espacio
                    key_name = event.unicode
                    if key_name.isalpha() and len(nombre) < 10:
                        nombre += key_name.upper()
        
        # ------------------------------------------------------------------
        # 2. DIBUJO EN PANTALLA: DEBE IR DENTRO DEL BUCLE WHILE
        # ------------------------------------------------------------------
        screen.fill((0, 0, 0)) # Fondo negro para la pantalla de game over/input
            
        # Título / Instrucciones
        # Usamos un try/except para get_letra por si no está definida
        try:
            texto_titulo = get_letra(60).render("¡FIN DEL JUEGO!", True, COLOR_CURSOR)
            texto_score = get_letra(40).render(f"PUNTAJE: {player_pts}", True, COLOR_TEXTO)
            texto_prompt = get_letra(30).render("INGRESA TU NOMBRE (SOLO LETRAS):", True, COLOR_TEXTO)
        except NameError:
            # Fallback simple si la función de fuente no está disponible
            font = pygame.font.Font(None, 60)
            texto_titulo = font.render("¡FIN DEL JUEGO!", True, COLOR_CURSOR)
            texto_score = font.render(f"PUNTAJE: {player_pts}", True, COLOR_TEXTO)
            texto_prompt = font.render("INGRESA TU NOMBRE (SOLO LETRAS):", True, COLOR_TEXTO)

        screen.blit(texto_titulo, texto_titulo.get_rect(center=(CENTRO_X, CENTRO_Y - 150)))
        screen.blit(texto_score, texto_score.get_rect(center=(CENTRO_X, CENTRO_Y - 50)))
        screen.blit(texto_prompt, texto_prompt.get_rect(center=(CENTRO_X, CENTRO_Y + 10)))
            
        # Dibujar la caja de texto
        pygame.draw.rect(screen, COLOR_FONDO_CAJA, INPUT_RECT)
        pygame.draw.rect(screen, COLOR_TEXTO, INPUT_RECT, 2) # Borde
            
        # Renderizar el texto ingresado
        # Usamos el mismo fallback de fuente
        try:
            texto_renderizado = get_letra(40).render(nombre, True, COLOR_TEXTO)
        except NameError:
            font_input = pygame.font.Font(None, 40)
            texto_renderizado = font_input.render(nombre, True, COLOR_TEXTO)

            
        # Ajustar posición del texto dentro de la caja
        text_rect = texto_renderizado.get_rect(midleft=(INPUT_RECT.x + 10, INPUT_RECT.centery))
        screen.blit(texto_renderizado, text_rect)
            
        # Dibujar el cursor (pequeña línea parpadeante)
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_pos = text_rect.right if nombre else INPUT_RECT.x + 10
            pygame.draw.line(screen, COLOR_CURSOR, (cursor_pos, INPUT_RECT.y + 10), (cursor_pos, INPUT_RECT.bottom - 10), 3)

        # 3. ACTUALIZAR LA PANTALLA
        pygame.display.flip()
    
    # 4. RETORNO DE LA FUNCIÓN: SOLO CUANDO EL BUCLE WHILE FINALIZA (textbox = False)
    return nombre.strip()

def guardar_nuevo_puntaje(screen, player_pts):
    """
    Solicita el nombre al usuario usando la ventana de Pygame,
    añade el nuevo puntaje a la lista general y la guarda.
    
    Args:
        player_pts (int): El puntaje obtenido por el jugador.
        screen (pygame.Surface): La superficie de la pantalla de Pygame (nueva dependencia).
    """
    
    # 1. Llama a la nueva función de entrada de texto en Pygame
    nombre = obtener_nombre(screen, player_pts)
            
    print(f"Guardando puntaje para: {nombre}")
    # ----------------------------------------
    
    todos_los_puntajes = []
    
    # Asumimos que RUTA_PUNTAJES está definida y apuntando a un archivo JSON
    try:
        if os.path.exists(RUTA_PUNTAJES):
            with open(RUTA_PUNTAJES, "r") as archivo:
                todos_los_puntajes = json.load(archivo)
    except NameError:
        # Manejo si RUTA_PUNTAJES no está definida
        print("Error: RUTA_PUNTAJES no está definida. No se guardará el puntaje.")
        return
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        pass

    # Usa player_pts que fue pasado a esta función.
    todos_los_puntajes.append({"nombre": nombre, "player_pts": player_pts})

    try:
        with open(RUTA_PUNTAJES, "w") as archivo:
            json.dump(todos_los_puntajes, archivo, indent=4)
        print("Puntaje guardado exitosamente.")
    except IOError:
        print(f"Error al escribir en el archivo: {RUTA_PUNTAJES}")

