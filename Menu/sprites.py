import pygame
import configuracion as cfg

#Creamos funcion para cargar sprites

def load(name):
    path = f"./assets/{name}.png"
    img = pygame.image.load(path) #No convertir a alpha() acá ya que en juego.py se cargan los sprites antes de definir la pantalla
    return pygame.transform.scale(img, (cfg.TILE, cfg.TILE))

MAGO = load("MAGO")
CERO = load("CERO")
RAIZNEGATIVA = load("RAIZNEGATIVA")
PIGARTO = load("PIGARTO")
ESPADA = load("ESPADA")
ESCUDO = load("ESCUDO")
ANILLO = load("ANILLO")
CORAZON = load("CORAZON")
