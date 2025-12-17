import pygame, sys
import os 
from button import Button
import colisiones as colision
import criaturas as cr
import items as item
import random
import configuracion as cfg
from juego import jugar as iniciar_juego # Importa la función principal del juego desde 'juego.py'

# Inicializa todos los módulos necesarios de Pygame
pygame.init() 
pygame.mixer.init()  # Inicializa el módulo de mezcla de sonido (necesario para la música y efectos).
cfg.cargar_sfx() #Cargar los efectos de sonido

#Cargar preferencias del usuario
cfg.cargar_preferencias()

# Define la pantalla en modo Fullscreen utilizando las dimensiones obtenidas en 'configuracion.py'.
SCREEN = pygame.display.set_mode((cfg.ANCHO_PANTALLA, cfg.ALTO_PANTALLA), pygame.FULLSCREEN)

#  CARGA Y CONFIGURACIÓN DE ASSETS (SPRITES) 


#Importamos sprites luego de definir la pantalla (SCREEN)
from sprites import CERO, RAIZNEGATIVA, PIGARTO, ESPADA, ESCUDO, ANILLO, CORAZON
pygame.display.set_caption("EL MATEMAGO") #Establece el título de la ventana

#Utilizamos .convert_alpha() una vez definida SCREEN
# Optimiza las imágenes cargadas para un dibujo más rápido en la pantalla y mantiene la transparencia de las imágenes.
#Forma general de optimizacion
CERO = CERO.convert_alpha()
RAIZNEGATIVA = RAIZNEGATIVA.convert_alpha()
PIGARTO = PIGARTO.convert_alpha()
ESPADA = ESPADA.convert_alpha()
ESCUDO = ESCUDO.convert_alpha()
ANILLO = ANILLO.convert_alpha()
CORAZON = CORAZON.convert_alpha()

#Cargamos imagen de fondo para el menú
fondo_menu = pygame.image.load("./assets/fondo_pantallas.png").convert() #metodo .convert convierte la imagen al mismo formato de color de pantalla
                                                                        #otra forma de optimizar y mas eficiencia
# Escala el fondo para que ocupe todo el tamaño de la pantalla. tenemos escala actual y la transformamos a (ancho, altura pantalla)
fondo_menu = pygame.transform.scale(fondo_menu, SCREEN.get_size())

            
# FUNCIÓN DE UTILIDAD PARA SALIDA RÁPIDA (ESCAPE / QUIT)
def manejar_salida_menu(event):
    """
     Maneja eventos de salida directa del juego (QUIT o ESCAPE) en pantallas de menú.
     
     Args:
         event (pygame.event.Event): El objeto evento de Pygame (necesita event par determinar el tipo de evento que se le pasa a la función y ver qué acción tomar)
     """
    if event.type == pygame.QUIT:
        # El usuario hace clic en el botón de cerrar de la ventana.
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            # El usuario presiona la tecla ESC.
            pygame.quit()
            sys.exit()

# PANTALLA DE PUNTAJE BAJO (bajo_puntaje) 
def bajo_puntaje():
    """
       Muestra un mensaje de advertencia de 3 segundos si el puntaje final es 0. 
       Impide guardar puntajes de cero.
    """
    
    # Detiene cualquier música que quede sonando y reproducir sfx de Game Over
    pygame.mixer.music.stop() 
    
    cfg.play_sfx("game_over")
    
    # 1. Crea un reloj local y define FPS 
    clock = pygame.time.Clock() 
    FPS = 60
    
    # Inicia un temporizador para controlar cuánto tiempo se muestra la pantalla.
    tiempo_inicio = pygame.time.get_ticks() #Devuelve los milisegundos que han transcurrido desde que se inicia el programa. Tiempo inicio se iguala a pygame.time.get_ticks() en ese preciso instante
    tiempo_mostrar = 3000 # Mostrar por 3 segundos
    
    while pygame.time.get_ticks() - tiempo_inicio < tiempo_mostrar: #Se muestra mientras la diferencia entre el tiempo en que se inicia el programa y tiempo_inicio sea mayor a 3 segundos (el tiempo en que se inició el programa aumenta a cada momento)
        
        # 2. Limitar la velocidad del bucle a 60 cuadros por segundo
        clock.tick(FPS) 
        
        # Manejo de eventos para permitir salir con QUIT/ESCAPE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manejar_salida_menu(event) # Utiliza la función de utilidad para QUIT/ESCAPE.
            # Permitir salir antes de tiempo presionando ESCAPE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return menu_principal() #Vuelve al menú principal
        
        # DIBUJO DEL MENSAJE 
        SCREEN.fill("#111111") # Fondo oscuro

        # Renderiza el texto del título y el mensaje de advertencia, usando fuentes de cfg.
        TEXTO_TITULO = cfg.get_letra(60).render("¡FIN DEL JUEGO!", True, "#FF0000") 
        RECT_TITULO = TEXTO_TITULO.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 50))
        SCREEN.blit(TEXTO_TITULO, RECT_TITULO)
        
        #Subtitulos
        TEXTO_SUB = cfg.get_letra(20).render(f"TU PUNTAJE ES MUY BAJO. NECESITAS MÁS PUNTOS PARA ENTRAR EN EL TOP.", True, "#FFFFFF")
        RECT_SUB = TEXTO_SUB.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y + 50))
        SCREEN.blit(TEXTO_SUB, RECT_SUB)
        
        # Actualiza toda la pantalla para mostrar los cambios.
        pygame.display.update() 
        
    return menu_principal() # Vuelve al menú principal después de 3 segundos
    

# PANTALLA MARCADORES 

def marcadores():
    """
        Muestra la lista de los mejores puntajes cargados desde el archivo JSON.
    """
    
    # Llama a la función de utilidad para cargar y ordenar el Top 3.
    top_puntaje = cfg.cargar_mejores_puntajes()
    
    # Variables de posicionamiento para centrar los puntajes.
    x_pos = cfg.CENTRO_X
    y_start = cfg.CENTRO_Y - 140
    line_spacing = 70

    while True:
        POS_MOUSE_MARCADORES = pygame.mouse.get_pos()
        SCREEN.blit(fondo_menu, (0, 0)) 
        5
        # Título de la pantalla.
        TEXTO_TITULO = cfg.get_letra(50).render("MARCADORES", True, "#f2c572")
        RECT_TITULO = TEXTO_TITULO.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 330))
        SCREEN.blit(TEXTO_TITULO, RECT_TITULO)
        
        if top_puntaje:
            # Si hay puntajes guardados, itera sobre la lista.
            for i, datos_puntaje in enumerate(top_puntaje):
                # Extrae nombre y puntaje (con valores por defecto por seguridad).
                nombre = datos_puntaje.get("nombre", "N/A") #Si falta la clave nombre en algún registro, .get se encarga de asignar un valor por defecto (N/A) y que no se cierre el programa
                puntaje = datos_puntaje.get("player_pts", 0)
                
                # Formatea la línea: [Ranking]. [Nombre] - [Puntaje]
                text_puntaje = f"{i+1}. {nombre} - {puntaje}"
                
                # Posiciona cada puntaje hacia abajo usando el índice (i) y el espaciado.
                TEXTO_SCORE = cfg.get_letra(40).render(text_puntaje, True, "White")
                
                RECT_SCORE = TEXTO_SCORE.get_rect(center=(x_pos, y_start + i * line_spacing))
                SCREEN.blit(TEXTO_SCORE, RECT_SCORE)
        else:
            # Si la lista está vacía, muestra un mensaje por defecto.
            TEXTO_SIN_SCORES = cfg.get_letra(30).render("AÚN NO HAY PUNTAJES REGISTRADOS.", True, "White")
            RECT_SIN_SCORES = TEXTO_SIN_SCORES.get_rect(center=(x_pos, y_start))
            SCREEN.blit(TEXTO_SIN_SCORES, RECT_SIN_SCORES)
        
        # Botón para volver al menú principal.
        VOLVER_MARCADORES = Button(image=pygame.image.load("./assets/Options Rect.png"), pos=(cfg.CENTRO_X, y_start + len(top_puntaje) * line_spacing + 100), 
                            text_input="VOLVER", font=cfg.get_letra(50), base_color="#e2f3ff", hovering_color="#fff7d1")
        VOLVER_MARCADORES.changeColor(POS_MOUSE_MARCADORES)
        VOLVER_MARCADORES.update(SCREEN)

        # Manejo de eventos.
        for event in pygame.event.get():
            manejar_salida_menu(event) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VOLVER_MARCADORES.checkForInput(POS_MOUSE_MARCADORES):
                    return menu_principal() # Usar return para volver al menú principal

        pygame.display.update()

# PANTALLA MANUAL 

def manual():
    """
       Muestra la pantalla del manual y proporciona un botón para abrir el PDF.
    """
    print("ENTRANDO A LA PANTALLA DE MANUAL")
    while True:
        POS_MOUSE_MANUAL = pygame.mouse.get_pos()
        SCREEN.blit(fondo_menu, (0, 0))
        
        # Título del manual
        TEXTO_MANUAL = cfg.get_letra(50).render("MANUAL", True, "#f2c572")
        RECT_MANUAL = TEXTO_MANUAL.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 330))
        SCREEN.blit(TEXTO_MANUAL, RECT_MANUAL)
        
        #BOTÓN PARA ABRIR EL PDF
        BOTON_PDF = Button(
            # imagen del botón
            image=pygame.image.load("./assets/Options Rect.png"),
            # posición central
            pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 0),
            # texto dentro del botón
            text_input="ABRIR PDF",
            font=cfg.get_letra(50),
            base_color="#e2f3ff",
            hovering_color="#fff7d1"
        )
        BOTON_PDF.changeColor(POS_MOUSE_MANUAL)
        BOTON_PDF.update(SCREEN)

        # Botón para volver.
        VOLVER_MANUAL = Button(image=pygame.image.load("./assets/Options Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 150), 
                            text_input="VOLVER", font=cfg.get_letra(50), base_color="#e2f3ff", hovering_color="#fff7d1")
        VOLVER_MANUAL.changeColor(POS_MOUSE_MANUAL)
        VOLVER_MANUAL.update(SCREEN)

        # Manejo de eventos.
        for event in pygame.event.get():
            manejar_salida_menu(event) 
            # Detectar clic del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Abrir pdf
                if BOTON_PDF.checkForInput(POS_MOUSE_MANUAL):
                    #Libreria os permite trabajar con sistema operativo/Archivos
                    
                    #trabajamos con modulo os y metodo .path es para manejar rutas archivos y .join une correctamente partes ruta\,/
                    ruta_pdf = os.path.join("assets", "Manual de Matemago.pdf") 
                    
                    # Ahora se Intenta abrir el archivo 
                    # Se usa try/except porque si no estamos en Windows, estamos en Linux o MacOS
                    # En Windows: abre el PDF con el programa predeterminado.
                    #startfile() viene de modulo os y es especifico para abrir archivos en windows
                    try:
                        os.startfile(ruta_pdf)  
                    except:
                        # En Mac o Linux: usa el comando "open" para abrir el archivo
                        os.system(f"open {ruta_pdf}")
                        
                    
                if VOLVER_MANUAL.checkForInput(POS_MOUSE_MANUAL):
                    return menu_principal() # Usar return para volver
        
        pygame.display.update()

# PANTALLA OPCIONES 

def opciones():
    """
       Muestra la pantalla de opciones, permitiendo al usuario ajustar el volumen 
       mediante un control deslizante (slider).
    """
    
    # Colores de fondo para la dificultad seleccionada
    COLOR_BASE = "#e2f3ff" #Opción inactiva
    COLOR_HOVER = "#f1ca04" #Color al colocar el mouse encima
    COLOR_SELECCION = "#1eff00" # Color para la opción activa
    
    # Carga la imagen originales
    QUIT_RECT_ORIGINAL = pygame.image.load("./assets/Quit Rect.png").convert_alpha()
    
    #Escala para botones más pequeños (ej. dificultad)
    ANCHO_PEQUEÑO = 250
    ALTO_PEQUEÑO = 55
    
    # Escalar la imagen de botón para dificultad
    RECT_PEQUEÑO = pygame.transform.scale(QUIT_RECT_ORIGINAL, (ANCHO_PEQUEÑO, ALTO_PEQUEÑO))
    
    # Variable de control: indica si el usuario está arrastrando el slider, de base es False y se hara True cuando se presione
    mouse_held = False
    while True:

        # Posición actual del mouse (x,y)
        POS = pygame.mouse.get_pos()
        # Dibujamos el fondo del menú de opciones.
        SCREEN.blit(fondo_menu, (0, 0))
        
        # Renderizamos el texto "OPCIONES" con una fuente grande (50 px)
        # #.render convierte string en surface, True es para bordes suaves no pixelados
        TEXTO_OP = cfg.get_letra(50).render("OPCIONES", True, "#f2c572")
        # y lo centramos en una posición superior de la pantalla.
        # con surface ya creada con texto "Volumen" creamos rectangulo para envolverlo
        #center coloca en centro cordenadas de centro pantalla (centro_x y centro_y -330 para que este arriba)
        SCREEN.blit(TEXTO_OP, TEXTO_OP.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 330)))
        
        # DIBUJOS VOLUMEN
        
        # Texto que dice "Volumen" a la izquierda del slider 
        #.render convierte string en surface para trabajarla, True es antialiasing para bordes suaves texto
        TEXTO_VOL = cfg.get_letra(35).render(f"VOLUMEN:", True, "White")
        
        #Dibujamos texto volumen (surface) y el rectangulo que lo envuelve, centramos ambos en su posicion
        SCREEN.blit(TEXTO_VOL, TEXTO_VOL.get_rect(center=(cfg.SLIDER_X-180, cfg.SLIDER_Y)))
        
        # Texto que muestra el volumen actual en porcentaje a la derecha del slider (usando VOLUMEN_GLOBAL de .cfg)
        #.render convierte string en surface para trabajarla, True es antialiasing para bordes suaves texto
        TEXTO_VOLPORCENTAJE = cfg.get_letra(35).render(f"{int(cfg.VOLUMEN_GLOBAL*100)}%", True, "White")
        
        #Dibujamos texto volumen (surface) y el rectangulo que lo envuelve, centramos ambos en su posicion
        SCREEN.blit(TEXTO_VOLPORCENTAJE, TEXTO_VOLPORCENTAJE.get_rect(center=(cfg.SLIDER_X+600, cfg.SLIDER_Y)))
        
        # DIBUJOS DIFICULTAD
        
        TEXTO_DIFICULTAD = cfg.get_letra(35).render(f"DIFICULTAD:", True, "White")
  
        SCREEN.blit(TEXTO_DIFICULTAD, TEXTO_DIFICULTAD.get_rect(center=(cfg.CENTRO_X-400, cfg.CENTRO_Y - 100)))
        
        # 1. BOTÓN NORMAL
        color_normal = COLOR_SELECCION if cfg.DIFICULTAD_GLOBAL == "NORMAL" else COLOR_BASE
        BOTON_NORMAL = Button(
            image=RECT_PEQUEÑO,
            pos=(cfg.CENTRO_X-50, cfg.CENTRO_Y - 100),
            text_input="NORMAL",
            font=cfg.get_letra(30),
            base_color=color_normal, 
            hovering_color=COLOR_HOVER
        )
        
        # 2. BOTÓN DIFÍCIL
        color_dificil = COLOR_SELECCION if cfg.DIFICULTAD_GLOBAL == "DIFICIL" else COLOR_BASE
        BOTON_DIFICIL = Button(
            image=RECT_PEQUEÑO,
            pos=(cfg.CENTRO_X+250, cfg.CENTRO_Y - 100),
            text_input="DIFICIL",
            font=cfg.get_letra(30),
            base_color=color_dificil, 
            hovering_color=COLOR_HOVER
        )

        # Actualizar y dibujar botones de dificultad
        BOTON_NORMAL.changeColor(POS)
        BOTON_NORMAL.update(SCREEN)
        BOTON_DIFICIL.changeColor(POS)
        BOTON_DIFICIL.update(SCREEN)
        
        
        # DIBUJOS MUSICA
        
        TEXTO_MUSICA = cfg.get_letra(35).render(f"MUSICA:", True, "White")
  
        SCREEN.blit(TEXTO_MUSICA, TEXTO_MUSICA.get_rect(center=(cfg.CENTRO_X-430, cfg.CENTRO_Y)))
        
        # 1. BOTÓN SI MÚSICA
        color_si_musica = COLOR_SELECCION if cfg.MUSICA_ACTIVADA else COLOR_BASE
        BOTON_SI_MUS = Button(
            image=RECT_PEQUEÑO,
            pos=(cfg.CENTRO_X-50, cfg.CENTRO_Y),
            text_input="SI",
            font=cfg.get_letra(30),
            base_color=color_si_musica, 
            hovering_color=COLOR_HOVER
        )
        
        # 2. BOTÓN NO MÚSICA
        color_no_musica = COLOR_SELECCION if not cfg.MUSICA_ACTIVADA else COLOR_BASE
        BOTON_NO_MUS = Button(
            image=RECT_PEQUEÑO,
            pos=(cfg.CENTRO_X+250, cfg.CENTRO_Y),
            text_input="NO",
            font=cfg.get_letra(30),
            base_color=color_no_musica, 
            hovering_color=COLOR_HOVER
        )

        # Actualizar y dibujar botones de dificultad
        BOTON_SI_MUS.changeColor(POS)
        BOTON_SI_MUS.update(SCREEN)
        BOTON_NO_MUS.changeColor(POS)
        BOTON_NO_MUS.update(SCREEN)
        
        
        # DIBUJOS SFX (EFECTOS DE SONIDO)
        
        TEXTO_SFX = cfg.get_letra(35).render(f"SFX:", True, "White")
        
        SCREEN.blit(TEXTO_SFX, TEXTO_SFX.get_rect(center=(cfg.CENTRO_X-430, cfg.CENTRO_Y+100)))
        
        # 1. BOTÓN SI SFX
        color_si_sfx = COLOR_SELECCION if cfg.SFX_ACTIVADOS else COLOR_BASE
        BOTON_SI_SFX = Button(
            image=RECT_PEQUEÑO,
            pos=(cfg.CENTRO_X-50, cfg.CENTRO_Y+100),
            text_input="SI",
            font=cfg.get_letra(30),
            base_color=color_si_sfx, 
            hovering_color=COLOR_HOVER
        )
        
        # 2. BOTÓN NO SFX
        color_no_sfx = COLOR_SELECCION if not cfg.SFX_ACTIVADOS else COLOR_BASE
        BOTON_NO_SFX = Button(
            image=RECT_PEQUEÑO,
            pos=(cfg.CENTRO_X+250, cfg.CENTRO_Y+100),
            text_input="NO",
            font=cfg.get_letra(30),
            base_color=color_no_sfx, 
            hovering_color=COLOR_HOVER
        )
        
        # Actualizar y dibujar botones de dificultad
        BOTON_SI_SFX.changeColor(POS)
        BOTON_SI_SFX.update(SCREEN)
        BOTON_NO_SFX.changeColor(POS)
        BOTON_NO_SFX.update(SCREEN)
        
        # DIBUJO DEL SLIDER 
        
        # Dibuja la barra de la línea del slider (rectángulo) con las dimensiones de cfg.
        pygame.draw.rect(SCREEN, "#e2f3ff", (cfg.SLIDER_X, cfg.SLIDER_Y, cfg.SLIDER_WIDTH, cfg.SLIDER_HEIGHT))
        
        # Dibujar la bolita del slider (círculo negro)
        pygame.draw.circle(SCREEN, "#f2c572", (cfg.SLIDER_HANDLE_X, cfg.SLIDER_Y + cfg.SLIDER_HEIGHT//2), cfg.HANDLE_RADIUS)

        # Botón para volver.
        VOLVER = Button(
            image=pygame.image.load("./assets/Play Rect.png"),
            pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 350),
            text_input="VOLVER",
            font=cfg.get_letra(50),
            base_color="#e2f3ff",
            hovering_color="#fff7d1"
        )
        VOLVER.changeColor(POS)
        VOLVER.update(SCREEN)

        # EVENTOS
        for event in pygame.event.get():
            manejar_salida_menu(event) 
            # Cuando el usuario hace clic con el mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Detecta si el clic ocurrió sobre la bolita del slider
                # Revisa si la posición horizontal del mouse está dentro del área de la bolita del slider.
                # centro menos el radio
                if (cfg.SLIDER_HANDLE_X - cfg.HANDLE_RADIUS <= POS[0] <= cfg.SLIDER_HANDLE_X + cfg.HANDLE_RADIUS
                    and cfg.SLIDER_Y - 10 <= POS[1] <= cfg.SLIDER_Y + 30):
                     # El usuario está agarrando el slider -> activar arrastre
                    mouse_held = True
    
                # Detección para botones de Música
                if BOTON_SI_MUS.checkForInput(POS):
                    if not cfg.MUSICA_ACTIVADA:
                        # 1. Cambiar la bandera de activación
                        cfg.MUSICA_ACTIVADA = True
                        
                        # 2. Reproducir la música inmediatamente:
                        # Se detiene cualquier cosa que esté sonando (si hay)
                        pygame.mixer.music.stop() 
                        
                        # Cargar y reproducir la música del menú
                        pygame.mixer.music.load(cfg.RUTA_MUSICA_MENU)
                        pygame.mixer.music.play(-1) # Reproducir en loop
                        pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL) # Aplicar el volumen actual
                        
                if BOTON_NO_MUS.checkForInput(POS):
                    if cfg.MUSICA_ACTIVADA:
                        cfg.MUSICA_ACTIVADA = False
                        pygame.mixer.music.stop() # Detener la música inmediatamente
                        cfg.guardar_preferencias()
                    
                #Cambia la variable a normal cuando se presioona el botón    
                if BOTON_NORMAL.checkForInput(POS):
                    cfg.DIFICULTAD_GLOBAL = "NORMAL"  
                    
                #Cambia la variable a difícil cuando se presiona el botón    
                if BOTON_DIFICIL.checkForInput(POS):
                    cfg.DIFICULTAD_GLOBAL = "DIFICIL"  
                    
                #Activa SFX cuando se presiona el botón
                if BOTON_SI_SFX.checkForInput(POS):
                    if not cfg.SFX_ACTIVADOS:
                        cfg.SFX_ACTIVADOS = True
                        cfg.guardar_preferencias()
                
                #Desactiva SFX cuando se presiona el botón
                if BOTON_NO_SFX.checkForInput(POS):
                    if cfg.SFX_ACTIVADOS:
                        cfg.SFX_ACTIVADOS = False
                        cfg.guardar_preferencias()
                    
                if VOLVER.checkForInput(POS):
                    cfg.guardar_preferencias() #Guarda las preferencias indicadas por el usuario
                    return menu_principal() # Usar return para volver al menú principal
            
            # Cuando el usuario suelta el clic -> dejar de arrastrar
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False
       
        #Configuracion mientras se arrastra
        
        # Mover la bolita con el mouse pero sin salirse de la barra, ej  Si el mouse está más a la derecha del límite, el mango se queda en el borde.
        if mouse_held:
            #resumen min() y max ()
            #min determina valor mas pequeño entre (a y b)
            #max determina valor mas grande entre (a y b)
            
            
            cfg.SLIDER_HANDLE_X = max(cfg.SLIDER_X, min(POS[0], cfg.SLIDER_X + cfg.SLIDER_WIDTH))
             # Convertir la posición de la bolita en un valor entre 0.0 y 1.0
            cfg.VOLUMEN_GLOBAL = (cfg.SLIDER_HANDLE_X - cfg.SLIDER_X) / cfg.SLIDER_WIDTH
         # Aplicar el volumen actualizado a la música
        pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL)
        # Actualizar la pantalla para mostrar el slider en su nueva posición.
        pygame.display.update()

# BUCLE PRINCIPAL DEL MENÚ 

def menu_principal():
    
    """
       Función principal que dibuja el menú, maneja los botones de navegación 
       y gestiona la música de fondo.
    """
    
    # 1. Gestión de música de inicio:
    # Si no hay música sonando y la música está activada, carga y reproduce la música del menú en loop (-1).
    if cfg.MUSICA_ACTIVADA:
            pygame.mixer.music.load(cfg.RUTA_MUSICA_MENU)
            pygame.mixer.music.play(-1) 
            pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL)
    else:
        # Si la música no debe estar activada, nos aseguramos de que esté detenida
        pygame.mixer.music.stop()
        
    SCREEN.fill((0, 0, 0))
    pygame.display.update()
    
    
    #Bucle infinito del menú principal.
    while True:
        
        # 2. Gestión de música durante el bucle
        # Se asegura de que la música de fondo se reinicie si se detiene por alguna razón y está activada
        if cfg.MUSICA_ACTIVADA:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(cfg.RUTA_MUSICA_MENU)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL)
        else:        
            # Si el usuario la desactivó, la detenemos si por alguna razón inició.
            pygame.mixer.music.stop()
            
        # 3. Dibujo del fondo y del título
        SCREEN.fill((0, 0, 0)) 
        POS_MOUSE_MENU = pygame.mouse.get_pos()
        SCREEN.blit(fondo_menu, (0, 0))
        
        
        # Título del juego
        TEXTO_MENU = cfg.get_letra(65).render("EL MATEMAGO", True, "#f2c572") 
        RECT_MENU = TEXTO_MENU.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 330))
        SCREEN.blit(TEXTO_MENU, RECT_MENU)
        
        # 4. Definición de los botones
        # Cada botón requiere una imagen, posición central, texto, fuente, y colores.

        BOTON_JUGAR = Button(image=pygame.image.load("./assets/Play Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y - 180), 
                            text_input="JUGAR", font=cfg.get_letra(50), base_color="#e2f3ff", hovering_color="#fff7d1")
        BOTON_MARCADORES = Button(image=pygame.image.load("./assets/Options Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y - 60), 
                            text_input="MARCADORES", font=cfg.get_letra(50), base_color="#e2f3ff", hovering_color="#fff7d1")
        BOTON_MANUAL = Button(image=pygame.image.load("./assets/Play Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 60), 
                            text_input="MANUAL", font=cfg.get_letra(50), base_color="#e2f3ff", hovering_color="#fff7d1")
        BOTON_OPCIONES = Button(image=pygame.image.load("./assets/Options Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 180), 
                            text_input="OPCIONES", font=cfg.get_letra(50), base_color="#e2f3ff", hovering_color="#fff7d1")
        BOTON_SALIR = Button(image=pygame.image.load("./assets/Play Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 300), 
                            text_input="SALIR", font=cfg.get_letra(50), base_color="#e2f3ff", hovering_color="#fff7d1")
        
        
        # 5. Dibujo de botones:
        for button in [BOTON_JUGAR, BOTON_MARCADORES, BOTON_MANUAL, BOTON_OPCIONES, BOTON_SALIR]:
            button.changeColor(POS_MOUSE_MENU) # Actualiza el color si el mouse está encima.
            button.update(SCREEN) # Dibuja el botón en la pantalla.
        
        # 6. Manejo de eventos
        for event in pygame.event.get():
            manejar_salida_menu(event) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if BOTON_JUGAR.checkForInput(POS_MOUSE_MENU):
                    # Llama a la función principal del juego.
                    resultado_juego = iniciar_juego(SCREEN)
                    # Si el juego devuelve False (puntaje cero), llama a bajo_puntaje().
                    if resultado_juego == False:
                        bajo_puntaje()
                    #Si devuelve True, la ejecución simplemente continúa con el menú
                    #(ya que menu_principal() está en un bucle infinito `while True:`)
                     
                    #Detener la música que esté sonando    
                    pygame.mixer.music.stop()
                    
                if BOTON_MARCADORES.checkForInput(POS_MOUSE_MENU):
                    marcadores() # Va a la pantalla de marcadores.
                    
                if BOTON_MANUAL.checkForInput(POS_MOUSE_MENU):
                    manual() # Va a la pantalla del manual.
                    
                if BOTON_OPCIONES.checkForInput(POS_MOUSE_MENU):
                    opciones() # Va a la pantalla de opciones.
                    
                if BOTON_SALIR.checkForInput(POS_MOUSE_MENU):
                    # Cierra Pygame y sale del sistema.
                    pygame.quit()
                    sys.exit()

        pygame.display.update() # Actualiza la pantalla para mostrar el menú.


 # La línea final llama a la función principal del menú, iniciando el bucle del juego.
menu_principal()