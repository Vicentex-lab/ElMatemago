import pygame
import configuracion as cfg

#Creamos funcion para cargar sprites

def load(name):
    path = f"./assets/{name}.png"
    # Solo cargar la imagen, no usar .convert() ni .convert_alpha() aquí (ya que estas requieren que la pantalla esté definida y juego.py carga los sprites antes de definir la pantalla).
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (cfg.TILE, cfg.TILE))

MAGO = load("MAGO")
CERO = load("CERO")
RAIZNEGATIVA = load("RAIZNEGATIVA")
PIGARTO = load("PIGARTO")
ESPADA = load("ESPADA")
ESCUDO = load("ESCUDO")
ANILLO = load("ANILLO")
