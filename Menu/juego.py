import pygame, sys
import random
import configuracion as cfg
import colisiones as colision 
import criaturas as cr         
import items as item           
from sprites import MAGO, CERO, RAIZNEGATIVA, PIGARTO, ESPADA, ESCUDO, ANILLO, CORAZON, WALL, FLOOR


def jugar(SCREEN):
    # Muestra la pantalla de juego, detiene la música del menú e inicia la música de juego.
    
    # 1. Detiene la música actual (la del menú)
    pygame.mixer.music.stop()
    
    # 2. Carga y reproduce la música del juego en loop
    try:
        pygame.mixer.music.load(cfg.RUTA_MUSICA_JUEGO) 
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL) 
    except pygame.error as e:
        print(f"Error al cargar la música del juego: {e}")
    def dibujar_hud(screen, player_pts, player_hp, player_item):
        # CONFIGURACIÓN DEL MARCO 
        hud_x = 40           # posicion del hud en eje x
        hud_y = 40            #posicion del hud en eje y
        hud_w = 320          # ancho del hud
        hud_h = 260          # alto del hud
    
        # Se crea una superficie especial para el HUD con transparencia.
        # Esto permite tener un recuadro semitransparente encima del juego
        hud_surface = pygame.Surface((hud_w, hud_h), pygame.SRCALPHA)
        hud_surface.fill((25, 30, 80, 160))  # Color oscuro + transparencia (160)
    
        #Se dibuja un borde dorado alrededor del HUD
        pygame.draw.rect(hud_surface, (255, 210, 60),  # Color dorado
                         (0, 0, hud_w, hud_h),   # Tamaño del rectángulo
                         5,                   # Grosor del borde
                         border_radius=18)     #Bordes redondeados
    
        # Finalmente se coloca el HUD completo en la pantalla principal.
        screen.blit(hud_surface, (hud_x, hud_y))
    
        
        
        
        #SECCIÓN: PUNTAJE
        fuente = cfg.get_letra(22)   #Fuente para el texto
        txt_pts = fuente.render(f"PUNTAJE: {player_pts}", True, (255, 255, 120))   # Texto en color amarillo suave
        screen.blit(txt_pts, (hud_x + 30, hud_y + 20))  # Se dibuja dentro del HUD
    
        
        
        
        # SECCIÓN: VIDA 
        fuente_vida = cfg.get_letra(22)
        txt_vida = fuente_vida.render("VIDA:", True, (255, 255, 255))
        screen.blit(txt_vida, (hud_x + 30, hud_y + 90))
    
        CORAZON_HUD = pygame.transform.scale(CORAZON, (28, 28)) # Escalamos el corazón para que encaje con el tamaño del HUD 
        # Dibujamos un corazón por cada punto de vida
        for i in range(player_hp):
            screen.blit(CORAZON_HUD, (hud_x + 150 + i*32, hud_y + 88)) # Cada corazón se dibuja un poco más a la derecha
    
        # SECCIÓN: ITEM
        fuente_item = cfg.get_letra(22)  
        txt_item = fuente_item.render("ITEM:", True, (255, 255, 255))
        screen.blit(txt_item, (hud_x + 30, hud_y + 160))
    
        # Selección del sprite del ítem
        if player_item == item.sword.name:
            sprite = ESPADA
        elif player_item == item.shield.name:
            sprite = ESCUDO
        elif player_item == item.ring.name:
            sprite = ANILLO
        else:
            sprite = None # Si no tiene ítem, no hay imagen que mostrar
    
        if sprite:
            ITEM_HUD = pygame.transform.scale(sprite, (40, 40)) # Tamaño ideal para el HUD
            screen.blit(ITEM_HUD, (hud_x + 160, hud_y + 160))
        else:
             # Si NO hay un ítem equipado, se escribe la palabra "NINGUNO"
            txt_none = fuente_item.render("NINGUNO", True, (160, 160, 160))
            screen.blit(txt_none, (hud_x + 160, hud_y + 160))
    

    FPS = 60
    
    FILAS = len(colision.maze)
    COLUMNAS = len(colision.maze[0])
    
    COLOR_WALL = (30,30,30)
    COLOR_FLOOR = (253, 254, 253)
    COLOR_PLAYER = (0,120,255)
    COLOR_CERO = (0, 0, 255)
    COLOR_PIGARTO = (0, 255, 0)
    COLOR_RAIZ = (255, 0, 0)
    COLOR_SWORD = (255, 255, 0)
    COLOR_SHIELD = (255, 165, 0)
    COLOR_RING = (0, 0, 0)
    COLOR_HEART = (255, 100, 100)
    
    screen = SCREEN # Usar la variable pasada como argumento
    clock = pygame.time.Clock()
    
    #Definiciones del jugador
    player_y = cr.player.positions_y
    player_x = cr.player.positions_x
    player_hp = cr.player.hp
    
    # Variables para efecto de flotacion en mago
    float_offset = 0
    float_direction = 1
    
    #Resto de definiciones del jugador
    player_item=""
    inmunidad=0
    player_pts=cr.player.pts
    temporizador=0
    
    # Pigarto: Resetea el índice de posición en su camino y su existencia.
    cr.pigarto.pos = 0 
    cr.pigarto.exist = 1 # Asumimos que debe empezar vivo
    
    # Cero: Resetea su existencia y posición (si fueron modificados al morir).
    cr.cero.exist = 1 
    
    # Raíz Negativa: Resetea su existencia
    cr.raiznegativa.exist = 1 

    
    #Spawnear Item
    #Espada
    cont_aux_1=random.randint(0, 5)
    print("espada",  cont_aux_1)
    sword_place_y=item.sword.places_y[ cont_aux_1]
    sword_place_x=item.sword.places_x[ cont_aux_1]
    
    #Escudo
    cont_aux_1=random.randint(0, 5)
    while item.shield.places_x==sword_place_x and item.shield.places_y==sword_place_y:
        cont_aux_1=random.randint(0, 5)
    print("escudo",  cont_aux_1)
    shield_place_y=item.shield.places_y[cont_aux_1]
    shield_place_x=item.shield.places_x[cont_aux_1]
    
    #Anillo
    cont_aux_1=random.randint(0, 5)
    print("anillo", cont_aux_1)
    while item.ring.places_x==sword_place_x and item.ring.places_y==sword_place_y and item.ring.places_x==shield_place_x and item.ring.places_y==shield_place_y:
        cont_aux_1=random.randint(0, 5)
    ring_place_y=item.shield.places_y[cont_aux_1]
    ring_place_x=item.shield.places_x[cont_aux_1]
    
    def can_move(r, c):
        return 0 <= r < FILAS and 0 <= c < COLUMNAS and colision.maze[r][c] >= 1
    
    def eventos(): #Etiquetas para la matriz
        nonlocal player_y
        nonlocal player_x
        nonlocal pos_x, pos_y  
        nonlocal dir_x, dir_y  
        
        if colision.maze[player_y][player_x] == 2: #Teletransportación Matemagica 1
            if player_y == 14 and player_x == 0:
                player_y = 13
                player_x = 18
                # Sincroniza posiciones en píxeles y resetea dirección
                pos_x = player_x * cfg.TILE
                pos_y = player_y * cfg.TILE
                print("Matemagicamente Teletransportado")

                
            elif player_y == 13 and player_x == 19:  
                player_y = 14
                player_x = 1
                pos_x = player_x * cfg.TILE
                pos_y = player_y * cfg.TILE
                print("Matemagicamente Teletransportado")

                
        if colision.maze[player_y][player_x] == 3: #Teletransportación Matemagica 2
            if player_y == 0 and player_x == 9:
                player_y = 26
                player_x = 10
                pos_x = player_x * cfg.TILE
                pos_y = player_y * cfg.TILE
                print("Matemagicamente Teletransportado")
                        
                      
            elif player_y == 27 and player_x == 10:  
                player_y = 1
                player_x = 9
                pos_x = player_x * cfg.TILE
                pos_y = player_y * cfg.TILE
                print("Matemagicamente Teletransportado")
     
    
    #MOVIMIENTO DEL ENEMIGO
    # ---------------------------
    # CERO
    # ---------------------------
    cero_y = cr.cero.positions_y
    cero_x = cr.cero.positions_x
    cero_exist=cr.cero.exist
    cero_cooldown = 0
    cero_ratio=cr.cero.movement_ratio
    
    # ---------------------------
    # Pigarto
    # ---------------------------
    pigarto_y = cr.pigarto.positions_y
    pigarto_x = cr.pigarto.positions_x
    pigarto_cooldown = 0
    pigarto_exist=cr.pigarto.exist
    pigarto_ratio=cr.pigarto.movement_ratio
    # ---------------------------
    # Raíz Negativa
    # ---------------------------
    raiznegativa_y = cr.raiznegativa.positions_y
    raiznegativa_x = cr.raiznegativa.positions_x
    raiznegativa_ratio=cr.raiznegativa.movement_ratio
    raiznegativa_cooldown = 0
    raiznegativa_exist=cr.raiznegativa.exist

    def mover_enemigo(f, c, f_obj, c_obj):
        """Mueve al enemigo acercándose al jugador"""

        # Vertical
        if f_obj < f and can_move(f - 1, c):
            f -= 1
        elif f_obj > f and can_move(f + 1, c):
            f += 1

        # Horizontal
        elif c_obj < c and can_move(f, c - 1):
            c -= 1
        elif c_obj > c and can_move(f, c + 1):
            c += 1

        return f, c
 
    
    move_cooldown = True   # evita que avance varias casillas al dejar presionada una tecla
    
    # ============================
    #  MOVIMIENTO DEL JUGADOR 
    # ============================

    # Dirección actual del jugador
    dir_x = 0
    dir_y = 0

    # Dirección deseada por el jugador
    deseada_x = 0   
    deseada_y = 0

    # Posición en pixeles
    pos_x = player_x * cfg.TILE   #cfg.tile es el tamaño de una casilla en pixeles
    pos_y = player_y * cfg.TILE

    speed = 2  # velocidad (pixeles por frame)

    running = True
    
    def reiniciar_juego():
        #nonlocal le dice a Python que no son variables locales de reiniciar_juego() si no que
        #se refiere a las variables definidas en la función superior, jugar()
        #Esto permite que el reinicio se aplique al estado global del juego 
        nonlocal player_y, player_x, player_hp, player_item, inmunidad, temporizador
        nonlocal cero_y, cero_x, cero_exist, cero_cooldown, cero_ratio  
        nonlocal pigarto_y, pigarto_x, pigarto_cooldown, pigarto_exist, pigarto_ratio
        nonlocal raiznegativa_y, raiznegativa_x, raiznegativa_ratio, raiznegativa_cooldown, raiznegativa_exist  
        nonlocal sword_place_y, sword_place_x, shield_place_y, shield_place_x, ring_place_y, ring_place_x
        nonlocal float_offset, float_direction, move_cooldown, dir_x, dir_y
    
        # Reinicio del jugador (excepto player_pts, que se mantiene)
        player_y = cr.player.positions_y
        player_x = cr.player.positions_x
        player_hp = cr.player.hp
        player_item = ""
        inmunidad = 0
        temporizador = 0  # Reinicia el temporizador para el nuevo "nivel"
    
        # Reinicio de enemigos
        cr.pigarto.pos = 0
        cr.pigarto.exist = 1
        cr.cero.exist = 1
        cr.raiznegativa.exist = 1
    
        # Reinicio de variables locales de existencia
        cero_exist = cr.cero.exist
        pigarto_exist = cr.pigarto.exist 
        raiznegativa_exist = cr.raiznegativa.exist
    
        # Variables de movimiento de enemigos
        cero_y = cr.cero.positions_y
        cero_x = cr.cero.positions_x
        cero_cooldown = 0
        cero_ratio = cr.cero.movement_ratio
    
        pigarto_y = cr.pigarto.positions_y
        pigarto_x = cr.pigarto.positions_x
        pigarto_cooldown = 0
        pigarto_ratio = cr.pigarto.movement_ratio
    
        raiznegativa_y = cr.raiznegativa.positions_y
        raiznegativa_x = cr.raiznegativa.positions_x
        raiznegativa_ratio = cr.raiznegativa.movement_ratio
        raiznegativa_cooldown = 0
    
        # Reinicio de spawneo de items (aleatorio)
        cont_aux_1 = random.randint(0, 5)
        sword_place_y = item.sword.places_y[cont_aux_1]
        sword_place_x = item.sword.places_x[cont_aux_1]
    
        cont_aux_1 = random.randint(0, 5)
        # Asegura que el escudo no spawnee donde la espada
        while item.shield.places_x[cont_aux_1] == sword_place_x and item.shield.places_y[cont_aux_1] == sword_place_y:
            cont_aux_1 = random.randint(0, 5)
        shield_place_y = item.shield.places_y[cont_aux_1]
        shield_place_x = item.shield.places_x[cont_aux_1]
    
        cont_aux_1 = random.randint(0, 5)
        # Asegura que el anillo no spawnee donde la espada ni el escudo
        while (item.ring.places_x[cont_aux_1] == sword_place_x and item.ring.places_y[cont_aux_1] == sword_place_y) or \
              (item.ring.places_x[cont_aux_1] == shield_place_x and item.ring.places_y[cont_aux_1] == shield_place_y):
            cont_aux_1 = random.randint(0, 5)
        ring_place_y = item.ring.places_y[cont_aux_1]
        ring_place_x = item.ring.places_x[cont_aux_1]
    
        # Reinicio de otras variables
        float_offset = 0
        float_direction = 1
        move_cooldown = True
        dir_x = 0
        dir_y = 0
        move_timer = 0
        
    reiniciar_juego()  # Inicialización inicial

    running = True
    mostrando_mensaje_victoria = False  # Nueva variable para controlar el mensaje
    mensaje_temporizador = 0  # Temporizador para el mensaje (en frames)
    
    while running:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Guardar dirección DESEADA siempre
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    deseada_x = 0
                    deseada_y = -1

                if event.key in (pygame.K_s, pygame.K_DOWN):
                    deseada_x = 0
                    deseada_y = 1

                if event.key in (pygame.K_a, pygame.K_LEFT):
                    deseada_x = -1
                    deseada_y = 0

                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    deseada_x = 1
                    deseada_y = 0

   
        # Convierte la posición de píxeles a casilla
   
        tile_x = round(pos_x / cfg.TILE)
        tile_y = round(pos_y / cfg.TILE)

        # Calcula si esta el jugador esta centrado
        alineado_x = (pos_x % cfg.TILE) == 0   # Si el resto es 0 esta alineado
        alineado_y = (pos_y % cfg.TILE) == 0

        if alineado_x and alineado_y:
            next_tx = tile_x + deseada_x
            next_ty = tile_y + deseada_y

            if can_move(next_ty, next_tx): 
                dir_x = deseada_x
                dir_y = deseada_y

            # Verificar la dirección actual
            next_tx = tile_x + dir_x
            next_ty = tile_y + dir_y

            if not can_move(next_ty, next_tx):
                dir_x = 0
                dir_y = 0

        # Mover en pixeles
        # Actualiza la posición en píxeles
        pos_x += dir_x * speed  
        pos_y += dir_y * speed

        # Actualiza la posición en casillas
        player_x = round(pos_x / cfg.TILE) # round es para elegir la posicion mas cercana a la actual
        player_y = round(pos_y / cfg.TILE)

        eventos()

                
        # ---------------------------
        # MOVER ENEMIGO
        # ---------------------------
        #Cero
        ahora = pygame.time.get_ticks()
        if ahora - cero_cooldown >= cero_ratio:
            cero_y, cero_x = mover_enemigo(cero_y, cero_x, player_y, player_x)
            cero_cooldown = ahora

        #Pigarto
        if ahora - pigarto_cooldown >= pigarto_ratio:
            if cr.pigarto.pos<106:
                cr.pigarto.pos = cr.pigarto.pos+1
                pigarto_cooldown=ahora
            if cr.pigarto.pos>=106:
                cr.pigarto.pos=0
                pigarto_cooldown=ahora
                
        #Raíz negativa
        if ahora - raiznegativa_cooldown >= raiznegativa_ratio:
            raiznegativa_y, raiznegativa_x = mover_enemigo(raiznegativa_y, raiznegativa_x, player_y, player_x)
            raiznegativa_cooldown = ahora
            #ESTOCADA INTEGRADA EN  MAIN
            if raiznegativa_x==player_x:
                raiznegativa_ratio=cr.raiznegativa.movement_ratio-150
            elif raiznegativa_y==player_y:
                raiznegativa_ratio=cr.raiznegativa.movement_ratio-150
            else:
                raiznegativa_ratio=cr.raiznegativa.movement_ratio
        # ---------------------------
        # COLISIÓN (Lógica de DERROTA)
        # ---------------------------
        #Con CERO
        if cero_y == player_y and cero_x == player_x and cero_exist==1:
            if player_item==item.shield.name:
                player_item=""
                inmunidad=0
                cero_x=cr.cero.positions_x
                cero_y=cr.cero.positions_y
            elif player_item==item.sword.name:
                player_pts+=cr.cero.pts
                COLOR_CERO=COLOR_FLOOR
                player_item=""
                cero_exist=0
                if pigarto_exist==1 and raiznegativa_exist==0:
                    COLOR_SWORD=(255, 255, 0)
                    sword_place_y=cr.cero.positions_y
                    sword_place_x=cr.cero.positions_y
            elif inmunidad!=1 and player_hp-cr.cero.damage>0:
                player_x=cr.player.positions_x #El matemago muere instantaneamente si no se cambia de lugar
                player_y=cr.player.positions_y #Ideal siguiente paso es poenr frames de invlunerabilidad, por mientras esto funciona.
                player_hp-=cr.cero.damage
            elif inmunidad!=1 and player_hp-cr.cero.damage<=0:
                print("💀 cero")
                pygame.mixer.music.stop() 
                if player_pts > 0:
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return True # Indica que debe ir al menú principal
                else:
                    return False # Indica que debe ir a bajo_puntaje
            
        #Con Pigarto
        if pigarto_y[cr.pigarto.pos] == player_y and pigarto_x[cr.pigarto.pos] == player_x and pigarto_exist==1:
            if player_item==item.shield.name:
                cr.pigarto.pos=0
                inmunidad=0
                player_item=""
            elif player_item==item.sword.name:
                # Comportamiento único: Pigarto recibe daño normal a menos que sea el último
                if cero_exist==1 or raiznegativa_exist==1: 
                    cr.pigarto.hp=cr.pigarto.hp-item.sword.damage
                if cero_exist==0 and raiznegativa_exist==0 and pigarto_exist==1: #Comando cuando sólo queda pigarto
                    pigarto_exist=0
                    pigarto_ratio=9999999
                    COLOR_PIGARTO=COLOR_FLOOR
                    player_pts+=cr.pigarto.pts
                player_item=""
                
                cr.pigarto.pos=0
                if cr.pigarto.hp<=0:
                    player_pts+=cr.pigarto.pts
                    pigarto_exist=0
                    pigarto_x=0
                    pigarto_y=0
                    pigarto_ratio=9999999
                    COLOR_PIGARTO=COLOR_WALL
            elif player_item==item.ring.name:
                player_pts+=cr.pigarto.pts
                COLOR_PIGARTO=COLOR_FLOOR
                player_item=""
                pigarto_exist=0
            elif inmunidad!=1 and player_hp-cr.pigarto.damage>0:
                player_x=cr.player.positions_x #El matemago muere instantaneamente si no se cambia de lugar
                player_y=cr.player.positions_y #Ideal siguiente paso es poenr frames de invlunerabilidad, por mientras esto funciona.
                player_hp-=cr.pigarto.damage
            elif inmunidad!=1 and player_hp-cr.pigarto.damage<=0:
                print("💀 pigarto")
                pygame.mixer.music.stop() 
                if player_pts > 0:
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return True # Indica que debe ir al menú principal
                else:
                    return False # Indica que debe ir a bajo_puntaje
            
        #Con Raiz negativa
        if raiznegativa_y == player_y and raiznegativa_x == player_x and raiznegativa_exist==1:
            if player_item==item.shield.name:
                player_pts+=cr.raiznegativa.pts
                COLOR_RAIZ=COLOR_FLOOR
                player_item=""
                raiznegativa_exist=0
                inmunidad=0
                raiznegativa_x=0
                raiznegativa_y=0
                raiznegativa_ratio=9999999
                if pigarto_exist==1 and cero_exist==0:
                    COLOR_SWORD=(255, 255, 0)
                    sword_place_y=cr.cero.positions_y
                    sword_place_x=cr.cero.positions_y
            elif player_item==item.sword.name:
                cr.raiznegativa.hp-=item.sword.damage
                player_item=""
                raiznegativa_x=cr.raiznegativa.positions_x
                raiznegativa_y=cr.raiznegativa.positions_y
                if cr.raiznegativa.hp<=0:
                    player_pts+=cr.raiznegativa.pts
                    raiznegativa_exist=0
                    raiznegativa_x=0
                    raiznegativa_y=0
                    raiznegativa_ratio=9999999
                    COLOR_RAIZ=COLOR_FLOOR
            elif inmunidad!=1 and player_hp-cr.raiznegativa.damage>0:
                player_x=cr.player.positions_x #El matemago muere instantaneamente si no se cambia de lugar
                player_y=cr.player.positions_y #Ideal siguiente paso es poenr frames de invlunerabilidad, por mientras esto funciona.
                player_hp-=cr.raiznegativa.damage
            elif inmunidad!=1 and player_hp-cr.raiznegativa.damage<=0:
                print("💀 raiz")
                pygame.mixer.music.stop() 
                if player_pts > 0:
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return True # Indica que debe ir al menú principal
                else:
                    return False # Indica que debe ir a bajo_puntaje
        
        #COLISIÓN CON ITEMS
        #Espada
        if sword_place_x==player_x and sword_place_y==player_y:
            player_item=item.sword.name
            sword_place_x=0
            sword_place_y=1
            player_pts+=item.sword.pts
            
        #Escudo
        if shield_place_x==player_x and shield_place_y==player_y:
            player_item=item.shield.name
            inmunidad=1
            shield_place_x=0
            shield_place_y=2
            player_pts+=item.shield.pts
            
        if ring_place_x==player_x and ring_place_y==player_y:
            player_item=item.ring.name
            ring_place_x=0
            ring_place_y=3
            player_pts+=item.ring.pts
            
        # DIBUJO DE todo LO QUE SE VE EN PANTALLA
    
        #Mapa
        # Recorremos cada fila (r) y cada columna (c) del laberinto.
        for r in range(FILAS):
            # Convertimos la posición en la matriz a coordenadas reales de pantalla
            for c in range(COLUMNAS):
                x = c * cfg.TILE + cfg.offset_x
                y = r * cfg.TILE + cfg.offset_y
                # Si la celda vale 0 → es una pared.
                if colision.maze[r][c] == 0:
                    screen.blit(WALL, (x, y))      # DIBUJAR PARED
                else:
                    screen.blit(FLOOR, (x, y))     # DIBUJAR SUELO
          
       #   DIBUJAMOS SPRITES
       
       # ENEMIGOS 
       # Solo se dibuja si está vivo (existencia = 1).
       # Cero
        if cero_exist == 1:
            screen.blit(
                CERO,
                (
                    cero_x * cfg.TILE + cfg.offset_x,
                    cero_y * cfg.TILE + cfg.offset_y
                )
            )
        
        # Pigarto
        # Pigarto se mueve siguiendo una lista de posiciones predefinidas.
        # cr.pigarto.pos indica el índice actual de su posición.
        if pigarto_exist == 1:
            screen.blit(
                PIGARTO,
                (
                    pigarto_x[cr.pigarto.pos] * cfg.TILE + cfg.offset_x,
                    pigarto_y[cr.pigarto.pos] * cfg.TILE + cfg.offset_y
                )
            )
        
        # Raíz Negativa
        # Igual que Cero: se dibuja si sigue vivo.
        if raiznegativa_exist == 1:
            screen.blit(
                RAIZNEGATIVA,
                (
                    raiznegativa_x * cfg.TILE + cfg.offset_x,
                    raiznegativa_y * cfg.TILE + cfg.offset_y
                )
            )
        
        #ITEMS
        #Cada ítem se dibuja en su posición correspondiente del mapa.
        
        # Espada
        screen.blit(
            ESPADA,
            (
                sword_place_x * cfg.TILE + cfg.offset_x,
                sword_place_y * cfg.TILE + cfg.offset_y
            )
        )
        
        # Escudo
        screen.blit(
            ESCUDO,
            (
                shield_place_x * cfg.TILE + cfg.offset_x,
                shield_place_y * cfg.TILE + cfg.offset_y
            )
        )
        
        # Anillo
        screen.blit(
            ANILLO,
            (
                ring_place_x * cfg.TILE + cfg.offset_x,
                ring_place_y * cfg.TILE + cfg.offset_y
            )
        )
        
        # EFECTO DE FLOTACIÓN DEL MAGO
       
       
       
       # Modifica el desplazamiento vertical del mago para que suba y baje suavemente.
        float_offset += float_direction * 0.2
        # Si el mago sube demasiado, empieza a bajar.
        if float_offset > 2:
            float_direction = -1
        # Si baja demasiado, empieza a subir.
        elif float_offset < -2:
            float_direction = 1
        # Se dibuja aplicando el efecto de flotación (sumado a la posición Y real)
        screen.blit(
            MAGO,
            (
                player_x * cfg.TILE + cfg.offset_x,
                player_y * cfg.TILE + cfg.offset_y + float_offset
            )
        )
        
        
        temporizador+=1
        
        # Lógica de VICTORIA
        if pigarto_exist==0 and cero_exist==0 and raiznegativa_exist==0:
            print("Puntaje sin bonus por tiempo:", player_pts)
            print("Segundos", temporizador/60)
            if temporizador/60<=12:
                player_pts+=2000
                print("TIEMPO INHUMANO") 
            elif temporizador/60<=15:
                player_pts+=1000
            elif temporizador/60<=20:
                player_pts+=500
            elif temporizador/60<=40:
                player_pts+=250
            elif temporizador/60<=60:
                player_pts+=100
            elif temporizador/60>60:
                player_pts+=0
                                
            print("Puntaje total:", player_pts)
            mostrando_mensaje_victoria = True
            mensaje_temporizador = 180  # 3 segundos a 60 FPS (60 * 3)
            reiniciar_juego()
       
        # Manejo del mensaje de victoria
        if mostrando_mensaje_victoria:
            mensaje_temporizador -= 1
            if mensaje_temporizador <= 0:
                reiniciar_juego()  # Ahora sí resetea después del mensaje
                mostrando_mensaje_victoria = False
            else:
                # Dibuja el mensaje de victoria (fondo negro y texto)
                overlay = pygame.Surface((cfg.ANCHO_PANTALLA, cfg.ALTO_PANTALLA), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 255))  # Fondo negro 
                screen.blit(overlay, (0, 0))
                
                fuente_titulo = cfg.get_letra(60)
                fuente_sub = cfg.get_letra(30)
                texto_titulo = fuente_titulo.render("¡NIVEL COMPLETADO!", True, (255, 255, 0))  # Amarillo
                texto_puntaje = fuente_sub.render(f"PUNTAJE ACUMULADO: {player_pts}", True, (255, 255, 255))  # Blanco
                
                screen.blit(texto_titulo, texto_titulo.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 50)))
                screen.blit(texto_puntaje, texto_puntaje.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y + 50)))
    
        dibujar_hud(screen, player_pts, player_hp, player_item)
        pygame.display.flip()

    # Si sale del bucle 'while running' por QUIT o ESCAPE, regresa al menú
    return True # Indica que debe ir al menú principal