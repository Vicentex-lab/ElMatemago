import pygame, sys
import os 
from button import Button
import colisiones as colision
import criaturas as cr
import items as item
import random
import configuracion as cfg
from juego import jugar as iniciar_juego # Importa la función principal del juego desde 'juego.py'

# INICIALIZACIÓN DE PYGAME Y PANTALLA 

# Inicializa todos los módulos necesarios de Pygame
pygame.init() 
pygame.mixer.init()  # Inicializa el módulo de mezcla de sonido (necesario para la música y efectos).

# Define la pantalla en modo Fullscreen utilizando las dimensiones obtenidas en 'configuracion.py'.
SCREEN = pygame.display.set_mode((cfg.ANCHO_PANTALLA, cfg.ALTO_PANTALLA), pygame.FULLSCREEN)

#  CARGA Y CONFIGURACIÓN DE ASSETS (SPRITES) 


#Importamos sprites luego de definir la pantalla (SCREEN)
from sprites import MAGO, CERO, RAIZNEGATIVA, PIGARTO, ESPADA, ESCUDO, ANILLO, CORAZON
pygame.display.set_caption("EL MATEMAGO") #Establece el título de la ventana

#Utilizamos .convert_alpha() una vez definida SCREEN
# Optimiza las imágenes cargadas para un dibujo más rápido en la pantalla y mantiene la transparencia de las imágenes.
#Forma general de optimizacion
MAGO = MAGO.convert_alpha()
CERO = CERO.convert_alpha()
RAIZNEGATIVA = RAIZNEGATIVA.convert_alpha()
PIGARTO = PIGARTO.convert_alpha()
ESPADA = ESPADA.convert_alpha()
ESCUDO = ESCUDO.convert_alpha()
ANILLO = ANILLO.convert_alpha()
CORAZON = CORAZON.convert_alpha()

#Cargamos imagen de fondo para el menú
fondo_menu = pygame.image.load("./assets/menu_editado.png").convert() #metodo .convert convierte la imagen al mismo formato de color de pantall
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
    
    # Detiene cualquier música que quede sonando
    pygame.mixer.music.stop() 
    
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
        TEXTO_SUB = cfg.get_letra(20).render("TU PUNTAJE ES 0. NECESITAS MÁS DE 0 PUNTOS PARA PODER GUARDARLO.", True, "#FFFFFF")
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
    # Variable de control: indica si el usuario está arrastrando el slider, de base es False y se hara True cuando se presione
    mouse_held = False
    while True:
        """#
        VOLUMEN_GLOBAL = 0.5 # Nivel inicial de volumen (50%).
        --- CONFIGURACIÓN DEL SLIDER DE VOLUMEN ---
SLIDER_WIDTH = 500 # Anchura de la línea del slider
SLIDER_HEIGHT = 10 #Altura de la línea del slider (es una línea horizontal).

# Posición X calculada como central inicialmente 
#con esto centramos slider, restando la mitad del ancho a centro ventana
SLIDER_X = CENTRO_X - (SLIDER_WIDTH // 2)  
SLIDER_Y = CENTRO_Y - 80 # Posición Y fija, un poco arriba del centro.

# Posición inicial del manejador (círculo) del slider.
# Se calcula multiplicando el ancho total por el volumen actual (0.5),
# y sumando eso a la posición inicial X del slider.
SLIDER_HANDLE_X = SLIDER_X + int(SLIDER_WIDTH * VOLUMEN_GLOBAL)

#tamaño circulo
HANDLE_RADIUS = 15"""
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
        
        
        # Texto que muestra el volumen actual en porcentaje (usando VOLUMEN_GLOBAL de .cfg)
        #.render convierte string en surface para trabajarla, True es antialiasing para bordes suaves texto
        TEXTO_VOL = cfg.get_letra(40).render(f"VOLUMEN: {int(cfg.VOLUMEN_GLOBAL*100)}%", True, "White")
        
        #Dibujamos texto volumen (surface) y el rectangulo que lo envuelve, centramos ambos en su posicion
        SCREEN.blit(TEXTO_VOL, TEXTO_VOL.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 180)))
        
        # DIBUJO DEL SLIDER 
        
        # Dibuja la barra de la línea del slider (rectángulo) con las dimensiones de cfg.
        pygame.draw.rect(SCREEN, "#e2f3ff", (cfg.SLIDER_X, cfg.SLIDER_Y, cfg.SLIDER_WIDTH, cfg.SLIDER_HEIGHT))
        
        # Dibujar la bolita del slider (círculo negro)
        pygame.draw.circle(SCREEN, "#f2c572", (cfg.SLIDER_HANDLE_X, cfg.SLIDER_Y + cfg.SLIDER_HEIGHT//2), cfg.HANDLE_RADIUS)

        # Botón para volver.
        VOLVER = Button(
            image=pygame.image.load("./assets/Play Rect.png"),
            pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 150),
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
                if VOLVER.checkForInput(POS):
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
    # Si no hay música sonando, carga y reproduce la música del menú en loop (-1).
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(cfg.RUTA_MUSICA_MENU)
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL)
        
    SCREEN.fill((0, 0, 0))
    pygame.display.update()
    
    
    #Bucle infinito del menú principal.
    while True:
        
        # 2. Gestión de música durante el bucle
        # Se asegura de que la música de fondo se reinicie si se detiene por alguna razón.
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(cfg.RUTA_MUSICA_MENU)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL)
            
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