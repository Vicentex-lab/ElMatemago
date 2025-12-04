import pygame
import configuracion as cfg

#Creamos funcion para cargar sprites

def load(name):
    # Esta función carga una imagen desde la carpeta "assets"
    # Construye la ruta del archivo, asumiendo formato PNG.
    # Luego la ajusta para que tenga el tamaño exacto de un cuadrito del juego.
    path = f"./assets/{name}.png"
     #Carga la imagen desde disco como superficie de Pygame.
    img = pygame.image.load(path) 
    # Escala la imagen para que ocupe exactamente un tile del laberinto.
    return pygame.transform.scale(img, (cfg.TILE, cfg.TILE))


#Sprites de jugador, enemigos, items, mapa, corazones,etc
MAGO = load("MAGO")
CERO = load("CERO")
RAIZNEGATIVA = load("RAIZNEGATIVA")
PIGARTO = load("PIGARTO")
ESPADA = load("ESPADA")
ESCUDO = load("ESCUDO")
ANILLO = load("ANILLO")
CORAZON = load("CORAZON")
WALL = load("WALL")
FLOOR = load("FLOOR")
