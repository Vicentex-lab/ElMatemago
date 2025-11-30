import pygame
import configuracion as cfg

#Hacemos funcion para cargar sprites

def load(name):
    path = f"./assets/{name}.png"
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (cfg.TILE, cfg.TILE))

MAGO = load("MAGO")
CERO = load("CERO")
RAIZ = load("RAIZNEGATIVA")
PIGARTO = load("PIGARTO")
ESPADA = load("ESPADA")
ESCUDO = load("ESCUDO")
ANILLO = load("ANILLO")