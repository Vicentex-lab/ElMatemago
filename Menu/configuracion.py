import pygame
import json
import os
import colisiones # Importa el módulo donde se define la matriz 'maze' (el mapa del laberinto)


# Inicializa Pygame para poder usar pygame.display.Info() y obtener la resolución.
# Es crucial inicializarlo aquí, ya que otros módulos de configuración (como la pantalla) dependen de esto.
pygame.init() 

# --- CONFIGURACIÓN DE PANTALLA ---
# Obtiene la información de la pantalla del sistema operativo.
INFO_PANTALLA = pygame.display.Info()
# Define el ancho de la pantalla usando la resolución actual.
ANCHO_PANTALLA = INFO_PANTALLA.current_w
# Define el alto de la pantalla usando la resolución actual.
ALTO_PANTALLA = INFO_PANTALLA.current_h

# Define el centro de la pantalla, que usaremos para centrar los elementos (menús, HUD, laberinto, etc)
CENTRO_X = ANCHO_PANTALLA // 2
CENTRO_Y = ALTO_PANTALLA // 2

# --- CONFIGURACIÓN DEL LABERINTO ---
TILE = 32  # Tamaño en píxeles de cada celda (o 'tile') del laberinto. Estándar para pixel art.

# Obtiene el número de filas del laberinto (dimensión vertical), definida en colisiones.py
# Esto se logra midiendo la longitud de la lista principal (que contiene todas las filas).
FILAS_LABERINTO = len(colisiones.maze)

# Obtiene el número de columnas del laberinto (dimensión horizontal).
# Se accede al primer elemento de la lista principal (colisiones.maze[0]),
# que es la primera fila, y se mide su longitud.
COLUMNAS_LABERINTO = len(colisiones.maze[0])

# --- CÁLCULO PARA CENTRAR EL LABERINTO EN PANTALLA COMPLETA ---
# Calcula el ancho total en píxeles del laberinto.
ANCHO_LABERINTO = COLUMNAS_LABERINTO * TILE
# Calcula el alto total en píxeles del laberinto.
ALTO_LABERINTO = FILAS_LABERINTO * TILE

# Centramos el laberinto usando el centro de la pantalla (cfg.CENTRO_X/Y)     
# offset_x: Distancia desde el borde izquierdo hasta donde debe empezar el laberinto.
# Se obtiene restando la mitad del ancho del laberinto al centro X de la pantalla.
offset_x = CENTRO_X - (ANCHO_LABERINTO // 2)
        
 # offset_y: Distancia desde el borde superior hasta donde debe empezar el laberinto.
# Se obtiene restando la mitad del alto del laberinto al centro Y de la pantalla.
offset_y = CENTRO_Y - (ALTO_LABERINTO // 2)

# --- VARIABLES GLOBALES DE JUEGO ---
VOLUMEN_GLOBAL = 0.5 # Nivel inicial de volumen (50%).
DIFICULTAD_GLOBAL = "NORMAL" # Puede ser "NORMAL" o "DIFICIL"
ARCHIVO_PREFERENCIAS = "Menu/preferencias.json" #Ruta archivo de preferencias del usuario
MUSICA_ACTIVADA = True # Si es True, la música se reproduce.
RUTA_MUSICA_MENU = "./assets/Matemago_Menu_Song.mp3" 
RUTA_MUSICA_JUEGO = "./assets/Matemago_Dungeon_Song.mp3"
RUTA_MUSICA_RECORD = "./assets/High_score.mp3"

SFX_ACTIVADOS = True # Controla si los efectos de sonido se reproducen
RUTA_SFX_ITEM = "./assets/sfx/Get_item.wav"
RUTA_SFX_ENEMY_DIE = "./assets/sfx/Enemy_die.wav"
RUTA_SFX_PLAYER_HURT = "./assets/sfx/Player_hurt.wav"
RUTA_SFX_GAME_OVER = "./assets/sfx/Game_over.wav"
SFX_LIBRARY = {} # Este diccionario global almacenará todos los objetos pygame.mixer.Sound cargados. Se inicializa vacío ({}) para que 'cargar_sfx()' pueda llenarlo al inicio del juego.

# Obtiene el directorio base del archivo actual (configuracion.py), útil para referencias relativas.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Construye la ruta completa al archivo JSON de puntajes de forma segura.
RUTA_PUNTAJES = os.path.join(BASE_DIR, "puntajes.json")

# --- CONFIGURACIÓN DEL SLIDER DE VOLUMEN ---
SLIDER_WIDTH = 500 # Anchura de la línea del slider
SLIDER_HEIGHT = 10 #Altura de la línea del slider (es una línea horizontal).

# Posición X calculada como central inicialmente 
#con esto centramos slider, restando la mitad del ancho a centro ventana
SLIDER_X = CENTRO_X - (SLIDER_WIDTH // 2)  
SLIDER_Y = CENTRO_Y - 190 # Posición Y fija, un poco arriba del centro.

# Posición inicial del manejador (círculo) del slider.
# Se calcula multiplicando el ancho total por el volumen actual (0.5),
# y sumando eso a la posición inicial X del slider.
SLIDER_HANDLE_X = SLIDER_X + int(SLIDER_WIDTH * VOLUMEN_GLOBAL)

#tamaño circulo
HANDLE_RADIUS = 15

# --- FUNCIONES DE UTILIDAD ---

def get_letra(size): 
    """
        Carga y devuelve un objeto de fuente (Font) de Pygame.
        
        Args:
            size (int): El tamaño de la fuente a cargar.
            
        Returns:
            pygame.font.Font: Un objeto de fuente de Pygame listo para renderizar texto.
        """
    return pygame.font.Font("./assets/prstart.ttf", size)

# Función de carga de SFX
def cargar_sfx():
    """
    Carga todos los efectos de sonido definidos en las rutas a SFX_LIBRARY.
    """
    
    # Declaración global: Indicamos que vamos a modificar la variable 'SFX_LIBRARY' que fue definida fuera de esta función.
    global SFX_LIBRARY
    
    # Definición de la lista de sonidos a cargar.
    # Usamos un diccionario para mapear una CLAVE de texto fácil de usar 
    # (ej. "item_pickup") a la RUTA de archivo real donde se encuentra el sonido.
    SFX_A_CARGAR = {
        "item_pickup": RUTA_SFX_ITEM,
        "enemy_die": RUTA_SFX_ENEMY_DIE,
        "player_hurt": RUTA_SFX_PLAYER_HURT,
        "game_over": RUTA_SFX_GAME_OVER
        # Añadir aquí más sonidos
    }
    
    # Bucle para recorrer el diccionario y cargar cada sonido.
    for key, path in SFX_A_CARGAR.items():
        # Bloque 'try/except' para manejar errores de carga (ej. archivo no encontrado).
        try:
            # Crea un objeto pygame.mixer.Sound con el archivo de la ruta (path).
            # Los objetos Sound se cargan completamente en la memoria para una reproducción instantánea y múltiple (pueden sonar varios a la vez).
            SFX_LIBRARY[key] = pygame.mixer.Sound(path)
        except pygame.error as e:
            # Si hay un error (ej. archivo faltante), se notifica al usuario
            print(f"Advertencia: No se pudo cargar el SFX '{key}'. Error: {e}")
            # Asignamos None al slot del diccionario para evitar un error de programa si intentamos usar un sonido que nunca se cargó.
            SFX_LIBRARY[key] = None 

# Función de reproducción de SFX
def play_sfx(key):
    """
    Reproduce el efecto de sonido asociado a 'key' si los SFX están activos y
    ajusta su volumen al valor global del usuario.
    
    Args:
        key (str): La clave del sonido a reproducir (ej. 'item_pickup').
    """
    
    # Declaración global: Accedemos a las variables de configuración definidas 
    # globalmente para leer el estado del volumen y la librería de sonidos.
    global MUSICA_ACTIVADA, VOLUMEN_GLOBAL, SFX_LIBRARY 
    
    # Comprobación de Activación de SFX
    # Si el usuario ha desactivado los SFX en las opciones, el resto de la función se salta, y el sonido no se reproduce.
    if SFX_ACTIVADOS: 
        
        # Verificación de Carga y Existencia
        # Comprueba que la 'key' exista en la librería Y que el objeto de sonido asociado no sea None (es decir, que se cargó correctamente antes).
        if key in SFX_LIBRARY and SFX_LIBRARY[key] is not None:
            
            # Recuperamos el objeto pygame.mixer.Sound para manipularlo.
            sound_object = SFX_LIBRARY[key]
            
            # Establecer el Volumen
            # Aplicamos el volumen global del usuario (ej. 0.5) al objeto de sonido,
            # asegurando que los SFX respeten las preferencias.
            sound_object.set_volume(VOLUMEN_GLOBAL) 
            
            # Reproducir el Sonido
            # Inicia la reproducción del SFX una sola vez. Como es un objeto Sound,
            # esta llamada no interrumpe la música del juego.
            sound_object.play()

def cargar_mejores_puntajes():
    """
        Carga todos los puntajes guardados, los ordena y devuelve solo el Top 3.
        
        Returns:
            list: Una lista de diccionarios con el formato [{'nombre': '...', 'player_pts': N}, ...]
                  Contiene los 3 mejores puntajes, o una lista vacía si falla o no hay archivo.
        """
        
    # 1. Verifica si el archivo de puntajes existe. Si no existe, devuelve una lista vacía.
    if not os.path.exists(RUTA_PUNTAJES):
        return []
    try:
         # 2. Abre el archivo en modo lectura ('r').
        with open(RUTA_PUNTAJES, "r") as archivo:
            # Carga el contenido JSON del archivo en la variable 'puntajes'.
            puntajes = json.load(archivo)
            
            # 3. Ordena la lista de diccionarios.
            #'key=lambda x: x["player_pts"]' indica que el criterio de ordenamiento --> (lambda es una función sin nombre que se define en una sola línea)
            # es el valor asociado a la clave "player_pts" en cada diccionario.
            # 'reverse=True' indica que el orden debe ser descendente (de mayor a menor).
            puntajes_ordenados = sorted(puntajes, key=lambda x: x["player_pts"], reverse=True)
            
            # 4. Devuelve los primeros 3 elementos de la lista ordenada (el Top 3).
            return puntajes_ordenados[:3] # Devuelve solo los 3 mejores (hace un slicing de la lista, inicia en 0 y se detiene antes del índice 3)
        
    # Maneja errores si el archivo existe pero el JSON está mal formado o hay un error de E/S (devuelve lista vacía).    
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
    
# Función para cargar la configuración al iniciar el juego
def cargar_preferencias():
    """
    Carga el volumen, la dificultad y el estado de la música desde el archivo JSON 
    si existe. Si el archivo no existe o está corrupto, se usan los valores por defecto 
    definidos en el módulo 'configuracion'.
    """    
    #Modifica las variables globales
    global VOLUMEN_GLOBAL, DIFICULTAD_GLOBAL, SLIDER_HANDLE_X, MUSICA_ACTIVADA, SFX_ACTIVADOS
    
    # Comprobación de existencia del archivo
    if os.path.exists(ARCHIVO_PREFERENCIAS):
        #Apertura del archivo
        # 'with open' asegura que el archivo se cerrará automáticamente al salir del bloque, incluso si ocurre un error.
        with open(ARCHIVO_PREFERENCIAS, 'r') as f:
            try:
                # json.load() lee el contenido del archivo .json (f) y lo convierte 
                # en un diccionario de Python (datos).
                datos = json.load(f)
                
                # Aplicar la configuración guardada
                
                # Cargar y aplicar el volumen
                # Se verifica si la clave 'volumen' existe y si su valor está dentro del rango 0.0 a 1.0.
                if 'volumen' in datos and 0.0 <= datos['volumen'] <= 1.0:
                    VOLUMEN_GLOBAL = datos['volumen'] # Asigna el valor guardado a la variable global.
                    
                    # Aplica el volumen inmediatamente al mezclador de Pygame,
                    # para que la música del menú suene con el volumen correcto si está activa.
                    pygame.mixer.music.set_volume(VOLUMEN_GLOBAL) 
                    
                    # Actualizar la posición del slider
                    SLIDER_HANDLE_X = SLIDER_X + (SLIDER_WIDTH * VOLUMEN_GLOBAL)
                
                # Cargar la dificultad
                # Se verifica si la clave 'dificultad' existe y si su valor es uno de los esperados.
                if 'dificultad' in datos and datos['dificultad'] in ["NORMAL", "DIFICIL"]:
                    DIFICULTAD_GLOBAL = datos['dificultad']
                    
                # Cargar el estado de la música
                # Se verifica si la clave 'musica_activada' existe y si su valor es un booleano (True/False).
                if 'musica_activada' in datos and isinstance(datos['musica_activada'], bool):
                    MUSICA_ACTIVADA = datos['musica_activada']
                    
                if 'sfx_activados' in datos and isinstance(datos['sfx_activados'], bool):
                    SFX_ACTIVADOS = datos['sfx_activados']
                     
                print("Configuración cargada exitosamente.")
                
            except json.JSONDecodeError:
                print(f"Error al leer el archivo {ARCHIVO_PREFERENCIAS}. Usando valores predeterminados.")
    else:
        print(f"Archivo {ARCHIVO_PREFERENCIAS} no encontrado. Usando valores predeterminados.")

    
# Función para guardar la configuración después de un cambio
def guardar_preferencias():
    """Guarda el volumen, dificultad y otras configuraciones en un archivo JSON."""
    
    #Trabaja con variables globales
    global VOLUMEN_GLOBAL, DIFICULTAD_GLOBAL, MUSICA_ACTIVADA
    
    # 1. Crear el diccionario con los datos actuales
    datos = {
        'volumen': VOLUMEN_GLOBAL,
        'dificultad': DIFICULTAD_GLOBAL,
        'musica_activada': MUSICA_ACTIVADA,
        'sfx_activados': SFX_ACTIVADOS,
    }
    
    # 2. Escribir el diccionario en el archivo JSON
    with open(ARCHIVO_PREFERENCIAS, 'w') as f:
        json.dump(datos, f, indent=4)
    
    print("Configuración guardada.")   
    
def obtener_nombre(screen, player_pts):
    """
        Maneja la lógica de la pantalla de Game Over y la entrada de texto del usuario.
        Permite al usuario ingresar su nombre para guardar su puntaje.
        
        Args:
            screen (pygame.Surface): La superficie de Pygame donde se dibujará la entrada de texto.
            player_pts (int): El puntaje que el jugador acaba de obtener.
            
        Returns:
            str: El nombre ingresado por el usuario (limpio de espacios en blanco al inicio/final).
        """
        
    # Inicialización de variables de estado para la entrada de texto
    nombre = '' # Cadena donde se acumula el nombre.
    textbox = True # Controla el bucle de entrada de texto.
    
    # Colores
    COLOR_TEXTO = (255, 255, 255) # Blanco
    COLOR_FONDO_CAJA = (50, 50, 50) # Gris oscuro para el fondo de la caja de texto
    COLOR_CURSOR = (255, 255, 0) # Amarillo para el título y el cursor
    
    # Rectángulo de la caja de texto: define su posición y tamaño.
    # Se utiliza un bloque try-except para asegurar que se utilicen CENTRO_X/Y.
    try:
        # Se centra la caja restando 300 (la mitad de 600) del CENTRO_X.
        INPUT_RECT = pygame.Rect(CENTRO_X-300 , CENTRO_Y+50, 600, 60)
    except NameError:
        # Fallback si CENTRO_X y CENTRO_Y no están definidos correctamente
        screen_width, screen_height = screen.get_size()
        CENTRO_X = screen_width // 2
        CENTRO_Y = screen_height // 2
        INPUT_RECT = pygame.Rect(CENTRO_X - 300, CENTRO_Y + 50, 600, 60)
    
    # Bucle principal: se ejecuta mientras el usuario no presione ENTER con un nombre válido.
    while textbox:
        # 1. PROCESAMIENTO DE EVENTOS
        for event in pygame.event.get():
            # Si el usuario intenta cerrar la ventana, se sale del juego.
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Al presionar ENTER, se valida el nombre:
                    # Debe tener al menos un carácter que no sea espacio en blanco (`nombre.strip() != ""`)
                    # Y todos sus caracteres deben ser letras (`nombre.replace(' ', '').isalpha()`). (Se reemplazan espacios por cadena vacía y verifica si el carácter añadido es una letra)
                    if nombre.strip() != "" and nombre.replace(' ', '').isalpha():
                        textbox = False # Nombre válido: sale del bucle
                    else:
                        print("❌ Nombre inválido. Solo letras y no vacío.")
                elif event.key == pygame.K_BACKSPACE:
                    # Elimina el último carácter de la cadena del nombre.
                    nombre = nombre[:-1] #Hace un slicing (en Python el -1 representa el último carácter de la lista/cadena)
                    #Por lo que al presionar la tecla de retroceso, el slicing toma la cadena desde el primer caracter y
                    #considera todo lo que está antes del último carácter
                else:
                    # Captura la tecla presionada (event.unicode)
                    key_name = event.unicode
                    # Permite solo letras y limita la longitud a 10 caracteres.
                    if key_name.isalpha() and len(nombre) < 10:
                        nombre += key_name.upper() # Añade el carácter en mayúscula.
        
        # ------------------------------------------------------------------
        # 2. DIBUJO EN PANTALLA
        # ------------------------------------------------------------------
        # Rellena la pantalla con negro para limpiar el frame anterior.
        screen.fill((0, 0, 0)) 
            
        # Renderizado de textos de Game Over y Puntaje
        
        # Usamos un try/except para get_letra por si no está definida
        try:
            # Título principal de la pantalla.
            texto_titulo = get_letra(60).render("¡FIN DEL JUEGO!", True, COLOR_CURSOR)
            # Muestra el puntaje obtenido.
            texto_score = get_letra(40).render(f"PUNTAJE: {player_pts}", True, COLOR_TEXTO)
            # Instrucción para el usuario.
            texto_prompt = get_letra(30).render("INGRESA TU NOMBRE (SOLO LETRAS):", True, COLOR_TEXTO)
        except NameError:
            # Fallback simple si la función de fuente no está disponible
            font = pygame.font.Font(None, 60)
            texto_titulo = font.render("¡FIN DEL JUEGO!", True, COLOR_CURSOR)
            texto_score = font.render(f"PUNTAJE: {player_pts}", True, COLOR_TEXTO)
            texto_prompt = font.render("INGRESA TU NOMBRE (SOLO LETRAS):", True, COLOR_TEXTO)

        # Posicionamiento de textos en la pantalla (centrados)
        screen.blit(texto_titulo, texto_titulo.get_rect(center=(CENTRO_X, CENTRO_Y - 150)))
        screen.blit(texto_score, texto_score.get_rect(center=(CENTRO_X, CENTRO_Y - 50)))
        screen.blit(texto_prompt, texto_prompt.get_rect(center=(CENTRO_X, CENTRO_Y + 10)))
            
        # Dibujar la caja de texto: fondo y borde
        pygame.draw.rect(screen, COLOR_FONDO_CAJA, INPUT_RECT) #Fondo
        pygame.draw.rect(screen, COLOR_TEXTO, INPUT_RECT, 2) # Borde
            
        # Renderizar el texto ingresado por el usuario
        # Usamos el mismo fallback de fuente
        try:
            texto_renderizado = get_letra(40).render(nombre, True, COLOR_TEXTO)
        except NameError:
            font_input = pygame.font.Font(None, 40)
            texto_renderizado = font_input.render(nombre, True, COLOR_TEXTO)

            
        # Ajustar posición del texto dentro de la caja
        # Se alinea a la izquierda (midleft) con un pequeño margen de 10 píxeles.
        text_rect = texto_renderizado.get_rect(midleft=(INPUT_RECT.x + 10, INPUT_RECT.centery))
        screen.blit(texto_renderizado, text_rect)
            
        # Dibujar el cursor (pequeña línea parpadeante)
        if pygame.time.get_ticks() % 1000 < 500:
            # Posición X del cursor: al final del texto si hay nombre, o al inicio si está vacío.
            cursor_pos = text_rect.right if nombre else INPUT_RECT.x + 10
            # Dibuja una línea vertical de 3 píxeles de grosor.
            pygame.draw.line(screen, COLOR_CURSOR, (cursor_pos, INPUT_RECT.y + 10), (cursor_pos, INPUT_RECT.bottom - 10), 3)

        # 3. ACTUALIZAR LA PANTALLA:  Muestra los cambios realizados.
        pygame.display.flip()
    
    # 4. RETORNO DE LA FUNCIÓN: SOLO CUANDO EL BUCLE WHILE FINALIZA (textbox = False)
    return nombre.strip() #.strip() elimina los espacios al final del texto

def guardar_nuevo_puntaje(screen, player_pts):
    """
       Función que gestiona el proceso completo de guardar un puntaje.
       1. Llama a la función de entrada de nombre.
       2. Carga todos los puntajes existentes.
       3. Añade el nuevo puntaje.
       4. Guarda la lista completa de vuelta en el archivo JSON.
       
       Args:
           screen (pygame.Surface): La superficie de la pantalla para la entrada de texto.
           player_pts (int): El puntaje obtenido.
    """
       
    # DETENER MÚSICA ANTERIOR Y CARGAR LA DE RÉCORD
    pygame.mixer.music.stop()
    if MUSICA_ACTIVADA:
        try:
            pygame.mixer.music.load(RUTA_MUSICA_RECORD)
            pygame.mixer.music.set_volume(VOLUMEN_GLOBAL)
            pygame.mixer.music.play(-1) # En bucle
        except pygame.error as e:
            print(f"Error cargando música de récord: {e}")   
    
    # 1. Solicita el nombre al usuario usando la ventana de Pygame.
    nombre = obtener_nombre(screen, player_pts)
            
    print(f"Guardando puntaje para: {nombre}")
    # ----------------------------------------
    
    todos_los_puntajes = []
    
    # 2. Carga los puntajes existentes.
    try:
        # Verifica si el archivo JSON existe.
        if os.path.exists(RUTA_PUNTAJES):
            #Se utiliza with ya que al terminar el bloque de código dentro de with Python automáticamente
            #llama al método archivo.close(), que de lo contrario habría que hacerlo manualmente y además garantiza
            #que siempre se cierre
            with open(RUTA_PUNTAJES, "r") as archivo:
                # Carga la lista completa de puntajes.
                todos_los_puntajes = json.load(archivo)
    except NameError:
        # Error si la ruta no está definida (debería estarlo globalmente).
        print("Error: RUTA_PUNTAJES no está definida. No se guardará el puntaje.")
        return
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        # Ignora errores en la lectura y simplemente usa la lista vacía 'todos_los_puntajes = []'.
        pass

    # 3. Añade el nuevo puntaje con el nombre y el puntaje obtenido.
    todos_los_puntajes.append({"nombre": nombre, "player_pts": player_pts})

    # 4. Guarda la lista actualizada de puntajes.
    try:
        # Abre el archivo en modo escritura ('w') y lo sobrescribe.
        with open(RUTA_PUNTAJES, "w") as archivo:
            # Escribe la lista completa de Python como una cadena JSON, usando 'indent=4' para formato legible (sangría de 4 espacios y salto de línea automático).
            json.dump(todos_los_puntajes, archivo, indent=4)
        print("Puntaje guardado exitosamente.")
    except IOError: # Cubre si es que hay otros problemas aparte de que el archivo no exista al momento de la escritura, IOError es un error de entrada y salida, evita que se cierre el programa
        print(f"Error al escribir en el archivo: {RUTA_PUNTAJES}")
        

def es_top_3(player_pts):
    """
    Verifica si un puntaje califica para entrar en el Top 3.
    Retorna True si califica, False de lo contrario.
    """
    todos_los_puntajes = []
    
    # 1. Intentar cargar los puntajes existentes
    if os.path.exists(RUTA_PUNTAJES):
        try:
            with open(RUTA_PUNTAJES, "r") as archivo:
                todos_los_puntajes = json.load(archivo)
        except (json.JSONDecodeError, IOError):
            todos_los_puntajes = []

    # 2. Si hay menos de 3, cualquier puntaje califica
    if len(todos_los_puntajes) < 3:
        return True

    # 3. Ordenar y comparar con el tercero
    todos_los_puntajes.sort(key=lambda x: x["player_pts"], reverse=True)
    tercer_mejor_puntaje = todos_los_puntajes[2]["player_pts"]
    
    return player_pts >= tercer_mejor_puntaje

