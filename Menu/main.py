import pygame, sys
import os 
from button import Button
import colisiones as colision
import criaturas as cr
import items as item
import random
import configuracion as cfg
from juego import jugar as iniciar_juego #del nuevo archivo juego.py

# Inicializa Pygame
pygame.init() 
pygame.mixer.init()  # Inicializa el módulo de mezcla de sonido

# Define la pantalla en modo Fullscreen
SCREEN = pygame.display.set_mode((cfg.ANCHO_PANTALLA, cfg.ALTO_PANTALLA), pygame.FULLSCREEN)

#Importamos sprites luego de definir pantalla Fullscreen
from sprites import MAGO, CERO, RAIZNEGATIVA, PIGARTO, ESPADA, ESCUDO, ANILLO

#Convertir sprites acá (una vez definida la pantalla)
MAGO = MAGO.convert_alpha()
CERO = CERO.convert_alpha()
RAIZNEGATIVA = RAIZNEGATIVA.convert_alpha()
PIGARTO = PIGARTO.convert_alpha()
ESPADA = ESPADA.convert_alpha()
ESCUDO = ESCUDO.convert_alpha()
ANILLO = ANILLO.convert_alpha()
pygame.display.set_caption("EL MATEMAGO")


#Cargamos fondo menu
fondo_menu = pygame.image.load("./assets/menu_editado.png").convert()
fondo_menu = pygame.transform.scale(fondo_menu, SCREEN.get_size())


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


def bajo_puntaje():
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
    

# --- PANTALLA MARCADORES ----

def marcadores():
    top_scores = cfg.cargar_mejores_puntajes()
    
    x_pos = cfg.CENTRO_X
    y_start = cfg.CENTRO_Y - 140
    line_spacing = 70

    while True:
        POS_MOUSE_MARCADORES = pygame.mouse.get_pos()
        SCREEN.blit(fondo_menu, (0, 0)) 

        TEXTO_TITULO = cfg.get_letra(50).render("MARCADORES", True, "#f2c572")
        RECT_TITULO = TEXTO_TITULO.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 330))
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
                            text_input="VOLVER", font=cfg.get_letra(50), base_color="#e2f3ff", hovering_color="#fff7d1")
        VOLVER_MARCADORES.changeColor(POS_MOUSE_MARCADORES)
        VOLVER_MARCADORES.update(SCREEN)

        for event in pygame.event.get():
            manejar_salida_menu(event) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VOLVER_MARCADORES.checkForInput(POS_MOUSE_MARCADORES):
                    return menu_principal() # Usar return para volver

        pygame.display.update()

# --- PANTALLA MANUAL  ---

def manual():
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

        VOLVER_MANUAL = Button(image=pygame.image.load("./assets/Options Rect.png"), pos=(cfg.CENTRO_X, cfg.CENTRO_Y + 150), 
                            text_input="VOLVER", font=cfg.get_letra(50), base_color="#e2f3ff", hovering_color="#fff7d1")
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

# --- PANTALLA OPCIONES ---

def opciones():
    # Variable de control: indica si el usuario está arrastrando el slider
    mouse_held = False
    while True:
         # Posición actual del mouse
        POS = pygame.mouse.get_pos()
        SCREEN.blit(fondo_menu, (0, 0))
        TEXTO_OP = cfg.get_letra(50).render("OPCIONES", True, "#f2c572")
        SCREEN.blit(TEXTO_OP, TEXTO_OP.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 330)))
        
        
        # Texto que muestra el volumen actual en porcentaje

        TEXTO_VOL = cfg.get_letra(40).render(f"VOLUMEN: {int(cfg.VOLUMEN_GLOBAL*100)}%", True, "White")
        SCREEN.blit(TEXTO_VOL, TEXTO_VOL.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 180)))
        
        # --- SLIDER (asume variables cfg.* definidas) ---
        
        #Dibujar la barra del slider (rectángulo gris), configuracion declarada en configuracion.py
        pygame.draw.rect(SCREEN, "#e2f3ff", (cfg.SLIDER_X, cfg.SLIDER_Y, cfg.SLIDER_WIDTH, cfg.SLIDER_HEIGHT))
        # Dibujar la bolita del slider (círculo negro)
        pygame.draw.circle(SCREEN, "#f2c572", (cfg.SLIDER_HANDLE_X, cfg.SLIDER_Y + cfg.SLIDER_HEIGHT//2), cfg.HANDLE_RADIUS)

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
    
    pygame.mixer.music.load(cfg.RUTA_MUSICA_MENU)
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL)
        
    SCREEN.fill((0, 0, 0))
    pygame.display.update()
    
    while True:
        
        #Volver a reproducir la música al retornar al menú
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        
        SCREEN.fill((0, 0, 0)) 
        POS_MOUSE_MENU = pygame.mouse.get_pos()
        SCREEN.blit(fondo_menu, (0, 0))
        
        
        # Título del juego
        TEXTO_MENU = cfg.get_letra(65).render("EL MATEMAGO", True, "#f2c572") 
        RECT_MENU = TEXTO_MENU.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 330))
        SCREEN.blit(TEXTO_MENU, RECT_MENU)
        
        # Definición de los botones
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
        
        for button in [BOTON_JUGAR, BOTON_MARCADORES, BOTON_MANUAL, BOTON_OPCIONES, BOTON_SALIR]:
            button.changeColor(POS_MOUSE_MENU)
            button.update(SCREEN)
        
        # Manejo de eventos
        for event in pygame.event.get():
            manejar_salida_menu(event) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOTON_JUGAR.checkForInput(POS_MOUSE_MENU):
                    resultado_juego = iniciar_juego(SCREEN)
                    if resultado_juego == False:
                        bajo_puntaje()
                        
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