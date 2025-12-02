import pygame, sys
import random
import configuracion as cfg
import colisiones as colision 
import criaturas as cr         
import items as item           
from sprites import MAGO, CERO, RAIZNEGATIVA, PIGARTO, ESPADA, ESCUDO, ANILLO, CORAZON


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

    def mostrar_puntaje(player_pts):
        fuente = cfg.get_letra(30)  
        texto = fuente.render(f"PUNTAJE: {player_pts}", True, (255, 255, 0)) 
        SCREEN.blit(texto, (50,50)) # Usar SCREEN que es argumento

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
    
    #Rest de definiciones del jugador
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
            if colision.maze[player_y][player_x] == 2: #Teletransportación Matemagica 1
                        if player_y==14 and player_x==0:
                            player_y=13
                            player_x=18
                            print("Matemagicamente Teletransportado")
                            
                        if player_y==13 and player_x==19:
                            player_y=14
                            player_x=1
                            print("Matemagicamente Teletransportado")
                            
            if colision.maze[player_y][player_x] == 3: #Teletransportación Matemagica 2
                        if player_y==0 and player_x==9:
                            player_y=26
                            player_x=10
                            print("Matemagicamente Teletransportado")
                            
                        if player_y==27 and player_x==10:
                            player_y=1
                            player_x=9
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

    dir_x = 0    # La dirección en donde se mueve le personaje en x
    dir_y = 0    # En y

    move_timer = 0     # acomula tiempo
    move_delay = 120   # velocidad del personaje 

    running = True
    while running:
        tiempof = clock.tick(FPS)  # tiempof es el tiempo en ms desde el ultimo frame
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- AÑADIR MANEJO DE ESCAPE EN JUEGO ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    running = False # Detiene el bucle para salir o ir a Game Over

                if event.key in (pygame.K_w, pygame.K_UP):
                    if can_move(player_y - 1, player_x):
                        dir_x = 0
                        dir_y = -1

                if event.key in (pygame.K_s, pygame.K_DOWN):
                    if can_move(player_y + 1, player_x):
                        dir_x = 0
                        dir_y = 1

                if event.key in (pygame.K_a, pygame.K_LEFT):
                    if can_move(player_y, player_x - 1):
                        dir_x = -1
                        dir_y = 0

                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    if can_move(player_y, player_x + 1):
                        dir_x = 1
                        dir_y = 0

        #  Movimiento con velocidad
        
        move_timer += tiempof  # se suma el tiempo que paso

        if move_timer >= move_delay:  # cuando pasa cierto tiempo se mueve una casilla
            move_timer = 0

            new_x = player_x + dir_x  # calcula la siguiente casilla hacia donde va el jugador
            new_y = player_y + dir_y  # eje: vas arriba dir_y = -1, new_y = player_y -1

            if can_move(new_y, new_x):  # comprueba si no hay pared para moverte
                player_x = new_x        # si hay pared no te mueves a esa direccion pero tampoco te detienes
                player_y = new_y        # la dir_x e y no cambia 
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
                
        #Raiz negativa
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
                    print("espada: cero")
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
                if cero_exist==1 or raiznegativa_exist==1: #Comando normal
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
                    print("espada: cero")
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
            
        # DIBUJO
    
        #Mapa
        for r in range(FILAS):
            for c in range(COLUMNAS):
                rect = pygame.Rect(c*cfg.TILE + cfg.offset_x, r*cfg.TILE + cfg.offset_y, cfg.TILE, cfg.TILE)
                color = COLOR_FLOOR if colision.maze[r][c] >= 1 else COLOR_WALL
                pygame.draw.rect(screen, color, rect)
                
        #HUD DE CORAZONES 
        for i in range(player_hp):
            screen.blit(
                CORAZON,
                (
                    19 * cfg.TILE + cfg.offset_x,
                    (1 + i) * cfg.TILE + cfg.offset_y
                )
            )
          
       #   DIBUJAMOS SPRITES
       
       # ENEMIGOS 
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
        if pigarto_exist == 1:
            screen.blit(
                PIGARTO,
                (
                    pigarto_x[cr.pigarto.pos] * cfg.TILE + cfg.offset_x,
                    pigarto_y[cr.pigarto.pos] * cfg.TILE + cfg.offset_y
                )
            )
        
        # Raíz Negativa
        if raiznegativa_exist == 1:
            screen.blit(
                RAIZNEGATIVA,
                (
                    raiznegativa_x * cfg.TILE + cfg.offset_x,
                    raiznegativa_y * cfg.TILE + cfg.offset_y
                )
            )
        
        # --- ITEMS ---
        
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
        
        # EFECTO DE FLOTACIÓN
        float_offset += float_direction * 0.2
        
        if float_offset > 2:
            float_direction = -1
        elif float_offset < -2:
            float_direction = 1
        # DIBUJO DEL MAGO CON EFECTO DE FLOTACION
        screen.blit(
            MAGO,
            (
                player_x * cfg.TILE + cfg.offset_x,
                player_y * cfg.TILE + cfg.offset_y + float_offset
            )
        )
        
        
        
        screen.blit(
            MAGO,
            (
                player_x * cfg.TILE + cfg.offset_x,
                player_y * cfg.TILE + cfg.offset_y
            )
        )
        
       
       
        
        temporizador+=1
        
        # Lógica de VICTORIA
        if pigarto_exist==0 and cero_exist==0 and raiznegativa_exist==0:
            running = False
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
                                
            pygame.mixer.music.stop() 
            # Llama a guardar puntaje con el orden corregido (screen, player_pts)
            cfg.guardar_nuevo_puntaje(SCREEN, player_pts) 
            print("Puntaje total:", player_pts)
            return True # Indica que debe ir al menú principal
    
        
        mostrar_puntaje(player_pts)
        pygame.display.flip()

    # Si sale del bucle 'while running' por QUIT o ESCAPE, regresa al menú
    return True # Indica que debe ir al menú principal