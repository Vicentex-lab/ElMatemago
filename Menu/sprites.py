import pygame
import configuracion as cfg

#Creamos funcion para cargar sprites

def load(name):
    # Construye la ruta del archivo en carpeta assets, asumiendo formato PNG.
    
    path = f"./assets/{name}.png"
     #Trabajamos con pygame.image que es un modulo de pygame para trabajar con imagenes
     #Funcionamiento .load()
     #Abre el archivo de imagen que está guardado en tu disco.
     #Lee su contenido, como un PNG, JPG, etc.
     #Lo convierte internamente en un objeto Surface de Pygame que sirve como lienzo en pygame, para trabajar con imagenes y operarlas, escalarlas,dibujar,rotar,etc
    img = pygame.image.load(path) 
    # Escala la imagen para que ocupe exactamente un tile del laberinto.
    #pygame.transform es un modulo y .scale() es un metodo de este que sirve para redimensionar surfaces
    #Recibe 2 parametros, img y se transforma a 32x32 de ancho/alto
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
