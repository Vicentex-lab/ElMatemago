import pygame
import configuracion as cfg

#Creamos funcion para cargar sprites

def load(name, recortar):
    # Construye la ruta del archivo en carpeta assets, asumiendo formato PNG.
    
    path = f"./assets/{name}.png"
     #Trabajamos con pygame.image que es un modulo de pygame para trabajar con imagenes
     #Funcionamiento .load()
     #Abre el archivo de imagen que está guardado en tu disco.
     #Lee su contenido, como un PNG, JPG, etc.
     #Lo convierte internamente en un objeto Surface de Pygame que sirve como lienzo en pygame, para trabajar con imagenes y operarlas, escalarlas,dibujar,rotar,etc
    img = pygame.image.load(path) 
    # Solo aplicamos el recorte si se pide explícitamente
    if recortar:
        rect_contenido = img.get_bounding_rect()
        img = img.subsurface(rect_contenido)
    # Escala la imagen para que ocupe exactamente un tile del laberinto.
    #pygame.transform es un modulo y .scale() es un metodo de este que sirve para redimensionar surfaces
    #Recibe 2 parametros, img y se transforma a 32x32 de ancho/alto
    return pygame.transform.scale(img, (cfg.TILE, cfg.TILE))


#Sprites de jugador
MAGO_1 = load("MAGO_1", recortar=False) # Derecha
MAGO_2 = load("MAGO_2", recortar=False) # Izquierda
MAGO_3 = load("MAGO_3", recortar=False) # Espalda
MAGO_4 = load("MAGO_4", recortar=False) # Frente

#Sprites secundarios para simular que mago camina
MAGO_1_B = load("MAGO_1_B", recortar=False) # Derecha
MAGO_2_B = load("MAGO_2_B", recortar=False) # Izquierda
MAGO_3_B = load("MAGO_3_B", recortar=False) # Espalda
MAGO_4_B = load("MAGO_4_B", recortar=False) # Frente
# 2. Las guardamos en LISTAS (Frame 0 y Frame 1)
ANIMACION_DERECHA = [MAGO_1, MAGO_1_B]
ANIMACION_IZQUIERDA = [MAGO_2, MAGO_2_B]
ANIMACION_ATRAS = [MAGO_3, MAGO_3_B]
ANIMACION_FRENTE = [MAGO_4, MAGO_4_B]

#ENEMIGOS
CERO = load("CERO", recortar=True)
RAIZNEGATIVA = load("RAIZNEGATIVA", recortar=True)
PIGARTO = load("PIGARTO", recortar=True)

#ITEMS
ESPADA = load("ESPADA", recortar=False)
ESCUDO = load("ESCUDO", recortar=True)
ANILLO = load("ANILLO", recortar=True)
CORAZON = load("CORAZON", recortar=True)
SPEED_BOOST = load("PW_SPEED_BOOST", recortar=True)
SLOW_TIME = load("pw_slow_time", recortar=True)

#ENTORNO
WALL = load("WALL", recortar=False)  # Paredes suelen llenar todo el cuadro, mejor False
FLOOR = load("FLOOR", recortar=False)
