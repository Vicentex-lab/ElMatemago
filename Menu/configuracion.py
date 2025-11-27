import pygame
import json
import os
import colisiones 


# Inicializa Pygame para poder usar pygame.display.Info()
pygame.init() 

# --- CONFIGURACIÓN DE PANTALLA ---
# Obtiene la resolución actual de la pantalla para usarla en el modo Fullscreen
INFO_PANTALLA = pygame.display.Info()
ANCHO_PANTALLA = INFO_PANTALLA.current_w
ALTO_PANTALLA = INFO_PANTALLA.current_h

# Define el centro de la pantalla, que usaremos para centrar los elementos
CENTRO_X = ANCHO_PANTALLA // 2
CENTRO_Y = ALTO_PANTALLA // 2

# --- CONFIGURACIÓN DEL LABERINTO ---
TILE = 32 # Tamaño de cada celda del laberinto
FILAS_LABERINTO = len(colisiones.maze)
COLUMNAS_LABERINTO = len(colisiones.maze[0])

# --- CÁLCULO PARA CENTRAR EL LABERINTO EN PANTALLA COMPLETA ---
ANCHO_LABERINTO = COLUMNAS_LABERINTO * TILE
ALTO_LABERINTO = FILAS_LABERINTO * TILE

# Centramos el laberinto usando el centro de la pantalla (cfg.CENTRO_X/Y)     
# offset_x: Distancia desde el borde izquierdo hasta donde debe empezar el laberinto.
# Se obtiene restando la mitad del ancho del laberinto al centro X de la pantalla.
offset_x = CENTRO_X - (ANCHO_LABERINTO // 2)
        
 # offset_y: Distancia desde el borde superior hasta donde debe empezar el laberinto.
# Se obtiene restando la mitad del alto del laberinto al centro Y de la pantalla.
offset_y = CENTRO_Y - (ALTO_LABERINTO // 2)

# --- VARIABLES GLOBALES DE JUEGO ---
VOLUMEN_GLOBAL = 0.5
RUTA_MUSICA_MENU = "C:\\Users\\Kari\\Documents\\GitHub\\ElMatemago\\Menu\\assets\\Matemago_Menu_Song.mp3" 
RUTA_MUSICA_JUEGO = "C:\\Users\\Kari\\Documents\\GitHub\\ElMatemago\\Menu\\assets\\Matemago_Dungeon_Song.mp3"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PUNTAJES = os.path.join(BASE_DIR, "puntajes.json")

# --- CONFIGURACIÓN DEL SLIDER DE VOLUMEN ---
SLIDER_WIDTH = 500
SLIDER_HEIGHT = 10
# Posición X calculada para centrar el SLIDER
SLIDER_X = CENTRO_X - (SLIDER_WIDTH // 2)  
SLIDER_Y = CENTRO_Y - 80 
SLIDER_HANDLE_X = SLIDER_X + int(SLIDER_WIDTH * VOLUMEN_GLOBAL)
HANDLE_RADIUS = 15

# --- FUNCIONES DE UTILIDAD ---

def get_letra(size): 
    """Carga y devuelve la fuente 'font.ttf' en el tamaño especificado."""
    return pygame.font.Font("C:\\Users\\Kari\\Documents\\GitHub\\ElMatemago\\Menu\\assets\\prstart.ttf", size)

def cargar_mejores_puntajes():
    """Carga todos los puntajes del archivo JSON, los ordena y devuelve el top 3."""
    if not os.path.exists(RUTA_PUNTAJES):
        return []
    try:
        with open(RUTA_PUNTAJES, "r") as archivo:
            puntajes = json.load(archivo)
            # Ordena los puntajes de forma descendente (reverse=True)
            puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)
            return puntajes_ordenados[:3] # Devuelve solo los 3 mejores
    except (json.JSONDecodeError, FileNotFoundError):
        return []