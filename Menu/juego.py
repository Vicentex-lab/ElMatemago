
import pygame, sys
import random
import configuracion as cfg
import colisiones as colision 
import criaturas as cr         
import items as item
import powerups as pw           
from sprites import CERO, RAIZNEGATIVA, PIGARTO, ESPADA, ESCUDO, ANILLO, CORAZON, WALL, FLOOR, SPEED_BOOST, SLOW_TIME, MULTIPLIER, DIVISOR

def jugar(SCREEN):
    # Muestra la pantalla de juego, detiene la música del menú e inicia la música de juego.
    
    # 1. Detiene la música actual (la del menú)
    pygame.mixer.music.stop()
    
    # 2. Carga y reproduce la música del juego en loop
    try:
        if cfg.MUSICA_ACTIVADA: #Solo reproducir si la música está activada
            pygame.mixer.music.load(cfg.RUTA_MUSICA_JUEGO)
            pygame.mixer.music.play(-1) # Reproducir en loop
            pygame.mixer.music.set_volume(cfg.VOLUMEN_GLOBAL)
    except pygame.error as e:
        print(f"Error al cargar la música del juego: {e}")
    
    def dibujar_hud(screen, player_pts, player_hp, player_item):
        # CONFIGURACIÓN DEL MARCO 
        hud_x = 40           # posicion del hud en eje x
        hud_y = 40            #posicion del hud en eje y
        hud_w = 320          # ancho del hud
        hud_h = 360         # alto del hud
    
        # Se crea una superficie especial para el HUD con transparencia.
        # Esto permite tener un recuadro semitransparente encima del juego
        #pygame.surface es modulo para construir lienzo para modificarlo
        #Recibe 2 parametros, el primero tupla (ancho,largo)
    
        hud_surface = pygame.Surface((hud_w, hud_h), pygame.SRCALPHA) 
        #pygame.SRCALPHA es para que la superficie que dibujamos permita transparencia por pixel y podamos dibujar encima
        #En este caso 160 es la transparencia
        #R,G,B, transparencia
        hud_surface.fill((25, 30, 80, 160))  # Se rellana superficie, con transparencia 25 y colores
        #Metodo .fill es para rellenar Surfaces con colores
    
        #Se dibuja un borde dorado alrededor del HUD
        pygame.draw.rect(hud_surface, (255, 210, 60),  # Color dorado en formato rgb
                         (0, 0, hud_w, hud_h),   # Tupla que define posicion y tamaño
                         5,                   # Grosor del borde, es tan bajo porque es una linea
                         border_radius=18)     #Bordes redondeados, suaviza esquinas
    
        # Finalmente se coloca el HUD completo en la pantalla principal.
        #.blit() "pega" una Surface sobre otra.
        #Se dibuja hud en coordenadas superiores izquierdas
        screen.blit(hud_surface, (hud_x, hud_y))
    
        #SECCIÓN: PUNTAJE
        fuente = cfg.get_letra(22)   #Funcion en cfg para retornar texto en pygame con tamaño 22
        # 1. Dibujamos la etiqueta "PUNTAJE:"
        txt_label_pts = fuente.render("PUNTAJE:", True, (255, 255, 120))   
        screen.blit(txt_label_pts, (hud_x + 30, hud_y + 20))
        # 2. Dibujamos el número (el valor del puntaje)
        txt_value_pts = fuente.render(str(player_pts), True, (255, 255, 120))
        screen.blit(txt_value_pts, (hud_x + 205, hud_y + 20))
    
        # SECCIÓN: VIDA 
        fuente_vida = cfg.get_letra(22)  #Funcion en cfg para retornar texto en pygame con tamaño 22
        #.render convierte string en surface, mostramos puntaje jugador, True es para bordes suaves no pixelados
        txt_vida = fuente_vida.render("VIDA:", True, (255, 255, 255))
        #.render convierte string en surface, mostramos puntaje jugador, True es para bordes suaves no pixelados
        screen.blit(txt_vida, (hud_x + 30, hud_y + 80))
        #nueva variable con corazon reescalado para que encaje con tamaño hud, escala 28x28
        CORAZON_HUD = pygame.transform.scale(CORAZON, (28, 28)) 
        # Dibujamos un corazón por cada punto de vida
        #Ciclo for para dibujar corazones, cada uno cambiara en "i * 32" pixeles a la derecha
        for i in range(player_hp):
            screen.blit(CORAZON_HUD, (hud_x + 160 + i*32, hud_y + 78)) 
    
        # SECCIÓN: ITEM
        fuente_item = cfg.get_letra(22)  #Funcion en cfg para retornar texto en pygame con tamaño 22
        txt_item = fuente_item.render("ITEM:", True, (255, 255, 255))
        #.render convierte string en surface, mostramos puntaje jugador, True es para bordes suaves no pixelados
        screen.blit(txt_item, (hud_x + 30, hud_y + 140)) # Se dibuja HUD creado en pantalla con su texto con sus coordenadas
    
        # Selección del sprite del ítem
        #Segun que item tenga jugador lo mostraremos en pantalla con su respectivo sprite
        if player_item == sword.name:
            sprite = ESPADA
        elif player_item == shield.name:
            sprite = ESCUDO
        elif player_item == ring.name:
            sprite = ANILLO
        else:
            sprite = None  # Si no tiene ítem, no hay imagen que mostrar
        # En caso que sprite != None 
        #Sprite tiene valor falso y se ejecutara else
        
        #Dibujaremos todo dentro de HUD
        if sprite:
            ITEM_HUD = pygame.transform.scale(sprite, (40, 40))  # Tamaño ideal de items para HUD
            #Dibujamos todo en pantalla con .blit()
            screen.blit(ITEM_HUD, (hud_x + 160, hud_y + 132))
        else:
            # Si NO hay un ítem equipado, se escribe la palabra "NINGUNO"
            txt_none = fuente_item.render("NINGUNO", True, (160, 160, 160)) 
            #.render convierte string en surface, mostramos puntaje jugador, True es para bordes suaves no pixelados
            screen.blit(txt_none, (hud_x + 160, hud_y + 140))
        
        
        
        
        # SECCION BUFFS
        #Lista para guardar TODOS los buffs activos
        lista_buffs_activos = []
        
        # Creamos y posicionamos el texto "BUFFS:" en el HUD
        fuente_buffs = cfg.get_letra(22)
        txt_buffs = fuente_buffs.render("BUFFS:", True, (255, 255, 255))
        screen.blit(txt_buffs, (hud_x + 30, hud_y + 200))

        #Verificamos cuál/cuales power-up están activo y asignamos sprites

        # -- Buff 1: Multiplicador --
        if multiplier.state:
            datos_buff = {
                "sprite": MULTIPLIER,
                "t_actual": multiplier.pos, #Tiempo restante (frames)
                "t_max": 60 * 15,  #Tiempo total 60FPS * 15 segundos= 900 frames totales, esto para calcular %
                "color": (50, 255, 50) # Verde
            }
            lista_buffs_activos.append(datos_buff) #Agregamos elemento con todas sus caracteristicas a lista
            
        # -- Buff 2: Divisor --
        if divisor.state:
            datos_buff = {
                "sprite": DIVISOR,
                "t_actual": divisor.pos, #Tiempo restante (frames)
                "t_max": 60 * 15,  #Tiempo total 60FPS * 15 segundos= 900 frames totales, esto para calcular %
                "color": (255, 50, 50) # Rojo
            }
            lista_buffs_activos.append(datos_buff)
            
        # -- Buff 3: Slow Time --
        if slow_time.pos != -1: 
            datos_buff = {
                "sprite": SLOW_TIME,
                "t_actual": slow_time.pos,  #Tiempo restante (frames)
                "t_max": 60 * 10,   #Tiempo total 60FPS * 10 segundos= 600 frames totales, esto para calcular %
                "color": (50, 100, 255) # Azul
            }
            lista_buffs_activos.append(datos_buff)
        # Si la lista tiene elementos, los dibujamos uno por uno
        if len(lista_buffs_activos) > 0:
            
            # 'i' es el índice (0, 1, 2...) y 'buff' es el diccionario de datos
            # Multiplicamos el índice por 50px para que no pongan uno encima del otro
            for i, buff in enumerate(lista_buffs_activos):
                
                # Calculamos la altura Y basada en el índice.
                # Cada buff estará 50 pixeles más abajo que el anterior.
                offset_y = i * 50 
                
                # Dibujar Icono
                ICONO = pygame.transform.scale(buff["sprite"], (40, 40))
                # Sumamos 'offset_y' a la altura base
                screen.blit(ICONO, (hud_x + 160, hud_y + 192 + offset_y))
                
                # Dibujar Barra del tiempo
                ancho_barra_max = 100
                alto_barra = 10
                pos_barra_x = hud_x + 210
                pos_barra_y = hud_y + 208 + offset_y # También bajamos la barra
                
                # Fondo barra
                pygame.draw.rect(screen, (50, 50, 50), (pos_barra_x, pos_barra_y, ancho_barra_max, alto_barra))
                
                # Porcentaje = Tiempo Restante / Tiempo Total
                porcentaje = buff["t_actual"] / max(buff["t_max"], 1)
                ancho_actual = int(ancho_barra_max * porcentaje)
                
                # Relleno barra
                pygame.draw.rect(screen, buff["color"], (pos_barra_x, pos_barra_y, ancho_actual, alto_barra))
                
                # Borde barra
                pygame.draw.rect(screen, (200, 200, 200), (pos_barra_x, pos_barra_y, ancho_barra_max, alto_barra), 1)
                
        else:
            # Si la lista está vacía mensaje "NINGUNO"
            txt_none_buff = fuente_buffs.render("NINGUNO", True, (160, 160, 160))
            screen.blit(txt_none_buff, (hud_x + 160, hud_y + 200))

    
    FILAS = len(colision.maze)
    COLUMNAS = len(colision.maze[0])
    
    screen = SCREEN # Usar la variable pasada como argumento
    clock = pygame.time.Clock()
    
    #Definiciones del jugador
    player_y = cr.player.positions_y
    player_x = cr.player.positions_x
    player_hp = cr.player.hp
    
    
    
    from sprites import ANIMACION_ATRAS,ANIMACION_DERECHA,ANIMACION_FRENTE,ANIMACION_IZQUIERDA
    # --- Animación del mago Mago izquierda derecha
    lista_actual = ANIMACION_FRENTE    # sprite actual del mago 
    # Variables para efecto de flotacion en mago
    float_offset = 0
    float_direction = 1
    
    #Resto de definiciones del jugador
    player_item=""
    inmunidad=0
    player_pts=cr.player.pts
    temporizador=0
    invul_base=1*60 #segundos*FPS para frame
    invul_frames=invul_base #segundos*FPS para frames
    colision_detected=True
    
    # Bandera para evitar acumulación de bonus de victoria
    victoria_detectada = False
    
    #Spawnear Item
    #Espada
    sword=item.sword()
    sword.spawn()
    
   #Escudo
    shield=item.shield()
    while True:
        shield.spawn()
        if shield.actual_x!=sword.actual_x and shield.actual_y!=sword.actual_y:
            break
        
    #Anillo
    ring=item.ring()
    while True:
        ring.spawn()
        if ring.actual_x!=sword.actual_x and ring.actual_y!=sword.actual_y and ring.actual_x!=shield.actual_x and ring.actual_y!=shield.actual_y:
            break
    
    #spawnear powerups
    #speed_boost=pw.speed_boost()
    #while True:
    #    speed_boost.random_spawn()
    #    if speed_boost.actual_x!=sword.actual_x and speed_boost.actual_y!=sword.actual_y and speed_boost.actual_x!=shield.actual_x and speed_boost.actual_y!=shield.actual_y and speed_boost.actual_x!=ring.actual_x and speed_boost.actual_y!=ring.actual_y:
    #        break
        
    slow_time=pw.slow_time()
    while True:
        slow_time.random_spawn()
        if slow_time.actual_x!=sword.actual_x and slow_time.actual_y!=sword.actual_y and slow_time.actual_x!=shield.actual_x and slow_time.actual_y!=shield.actual_y and slow_time.actual_x!=ring.actual_x and slow_time.actual_y!=ring.actual_y:
            break
        
    multiplier=pw.multiplier()
    divisor=pw.divisor()

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
    
    def reiniciar_juego():
        nonlocal player_y, player_x, pos_x, pos_y, player_hp, player_item, inmunidad, temporizador, invul_frames, colision_detected
        nonlocal sword, shield, ring, slow_time, multiplier, divisor
        nonlocal dir_x, dir_y, float_offset, float_direction
        nonlocal player_pts  # Ignorar para conservar el puntaje
        nonlocal cero, pigarto, raiznegativa  # Instancias de enemigos que se reasignan
        nonlocal victoria_detectada  # Resetear la bandera
        
        # Reiniciar posición del jugador
        player_y = cr.player.positions_y #posición en grid
        player_x = cr.player.positions_x #posición en grid
        pos_x = player_x * cfg.TILE #posición en pixeles
        pos_y = player_y * cfg.TILE #posición en pixeles
        
        # Reiniciar vida del jugador
        player_hp = cr.player.hp
        
        # Reiniciar item del jugador
        player_item = ""
        
        # Reiniciar inmunidad
        inmunidad = 0
        
        # Reiniciar temporizador
        temporizador = 0
        
        # Reiniciar frames de invulnerabilidad
        invul_frames = 2 * 60
        
        # Reiniciar detección de colisión
        colision_detected = True
        
        # Reiniciar movimiento
        dir_x = 0
        dir_y = 0
        move_timer = 0
        
        # Reiniciar efecto de flotación
        float_offset = 0
        float_direction = 1
        
        # Reiniciar enemigos (clases globales)
        cr.pigarto.pos = 0
        cr.pigarto.exist = 1
        cr.cero.exist = 1
        cr.raiznegativa.exist = 1
        
        # Reiniciar items (respawnear)
        sword=item.sword()
        sword.spawn()
        
        #Escudo
        shield=item.shield()
        while True:
            shield.spawn()
            if shield.actual_x!=sword.actual_x and shield.actual_y!=sword.actual_y:
                break
                
        #Anillo
        ring=item.ring()
        while True:
            ring.spawn()
            if ring.actual_x!=sword.actual_x and ring.actual_y!=sword.actual_y and ring.actual_x!=shield.actual_x and ring.actual_y!=shield.actual_y:
                break
            
        #spawnear powerups
        #speed_boost=pw.speed_boost()
        #while True:
        #    speed_boost.random_spawn()
        #    if speed_boost.actual_x!=sword.actual_x and speed_boost.actual_y!=sword.actual_y and speed_boost.actual_x!=shield.actual_x and speed_boost.actual_y!=shield.actual_y and speed_boost.actual_x!=ring.actual_x and speed_boost.actual_y!=ring.actual_y:
        #        break
                
        slow_time=pw.slow_time()
        while True:
            slow_time.random_spawn()
            if slow_time.actual_x!=sword.actual_x and slow_time.actual_y!=sword.actual_y and slow_time.actual_x!=shield.actual_x and slow_time.actual_y!=shield.actual_y and slow_time.actual_x!=ring.actual_x and slow_time.actual_y!=ring.actual_y:
                break
        
        # Reiniciar instancias de enemigos
        cero = cr.cero()
        pigarto = cr.pigarto()
        raiznegativa = cr.raiznegativa()
        
        # Resetear bandera de victoria (evita la acumulación de puntaje)
        victoria_detectada = False
        
        print("Juego reiniciado")
    
    #Instanciar ENEMIGO
    cero = cr.cero()
    pigarto=cr.pigarto()
    raiznegativa=cr.raiznegativa()
    
    #CONFIGURAR en función de dificultad
    if cfg.DIFICULTAD_GLOBAL=="DIFICIL":
        cero.movement_ratio=cero.movement_ratio*0.75
        pigarto.movement_ratio=pigarto.movement_ratio*0.75
        raiznegativa.ratios[0]=raiznegativa.ratios[0]*0.75
        raiznegativa.ratios[1]=raiznegativa.ratios[1]*0.75
    
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

    mostrando_mensaje_victoria = False  
    mensaje_temporizador = 0  # Temporizador para el mensaje (en frames)
    
    while running:
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- AÑADIR MANEJO DE ESCAPE EN JUEGO ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    running = False # Detiene el bucle para salir o ir a Game Over
                    return True 

            if event.type == pygame.KEYDOWN:
                # --- ARRIBA (W) ---
                if event.key in (pygame.K_w, pygame.K_UP):
                    deseada_x = 0
                    deseada_y = -1  
                    lista_actual = ANIMACION_ATRAS 
                # --- ABAJO (S) ---
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    deseada_x = 0
                    deseada_y = 1
                    lista_actual = ANIMACION_FRENTE 
                
                # --- IZQUIERDA (A) --
                if event.key in (pygame.K_a, pygame.K_LEFT):
                
                    deseada_x = -1
                    deseada_y = 0 
                    lista_actual = ANIMACION_IZQUIERDA
                # --- DERECHA (D) --
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    deseada_x = 1
                    deseada_y = 0
                    lista_actual = ANIMACION_DERECHA

   
        # Convierte la posición de píxeles a casilla
   
        tile_x = round(pos_x / cfg.TILE) 
        tile_y = round(pos_y / cfg.TILE)

        # Calcula si esta el jugador esta centrado
        alineado_x = (pos_x % cfg.TILE) == 0   # Si el resto es 0 esta alineado
        alineado_y = (pos_y % cfg.TILE) == 0   # tile = 32

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
        cero.mover(player_y, player_x, colision.maze)
        pigarto.mover()
        raiznegativa.mover(player_y, player_x, colision.maze)
        
        #SPAWNEO EN MITAD DE PARTIDA
        spawn_chance=random.randint(1, 60*30)
        print("contador random:", spawn_chance)
        if spawn_chance==1 and multiplier.spawned==False:
            while True:
                multiplier.random_spawn()
                if multiplier.actual_x!=sword.actual_x and multiplier.actual_y!=sword.actual_y and multiplier.actual_x!=shield.actual_x and multiplier.actual_y!=shield.actual_y and multiplier.actual_x!=ring.actual_x and multiplier.actual_y!=ring.actual_y and multiplier.actual_x!=slow_time.actual_x and multiplier.actual_y!=slow_time.actual_y:
                    break
        if spawn_chance==2 and divisor.spawned==False:
            while True:
                divisor.random_spawn()
                if divisor.actual_x!=sword.actual_x and divisor.actual_y!=sword.actual_y and divisor.actual_x!=shield.actual_x and divisor.actual_y!=shield.actual_y and divisor.actual_x!=ring.actual_x and divisor.actual_y!=ring.actual_y and divisor.actual_x!=slow_time.actual_x and divisor.actual_y!=slow_time.actual_y and divisor.actual_x!=multiplier.actual_x and divisor.actual_y!=multiplier.actual_y:
                    break
        # ---------------------------
        # COLISIÓN (Lógica de DERROTA)
        # ---------------------------
        #Con CERO
        if cero.colisionar(player_y, player_x) and colision_detected==False:
            colision_detected=True
            if player_item==shield.name:
                cero.positions_x=10
                cero.positions_y=13
                player_item=""
                inmunidad=0
                cfg.play_sfx("player_hurt")
            elif player_item==sword.name:
                if multiplier.state==True and divisor.state==False:
                    player_pts+=cero.pts*2
                elif divisor.state==True and multiplier.state==False:
                    player_pts+=cero.pts//2
                elif divisor.state==True and multiplier.state==True:
                    player_pts+=cero.pts
                else:
                    player_pts+=cero.pts
                player_item=""
                cero.exist=0
                cfg.play_sfx("enemy_die")
                
            elif inmunidad!=1 and player_hp-cero.damage>0:
                player_x=cr.player.positions_x
                player_y=cr.player.positions_y
                player_hp-=cero.damage
                cfg.play_sfx("player_hurt")
            elif inmunidad!=1 and player_hp-cero.damage<=0:
                cfg.play_sfx("player_hurt")
                print("💀 cero")
                pygame.mixer.music.stop() 
                if cfg.es_top_3(player_pts):
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return True #Volver al menú
                else:
                    return False #Mostrar pantalla bajo puntaje
            
        #Con Pigarto
        if pigarto.colisionar(player_y, player_x) and colision_detected==False:
            colision_detected=True
            if player_item==shield.name:
                pigarto.resetear_ruta()
                inmunidad=0
                player_item=""
                cfg.play_sfx("player_hurt")
            elif player_item==sword.name:
                if cero.exist==1 or raiznegativa.exist==1:
                    pigarto.hp=pigarto.hp-sword.damage
                    cfg.play_sfx("player_hurt")
                if cero.exist==0 and raiznegativa.exist==0 and pigarto.exist==1:
                    pigarto.exist=0
                    if multiplier.state==True and divisor.state==False:
                        player_pts+=pigarto.pts*2
                    elif divisor.state==True and multiplier.state==False:
                        player_pts+=pigarto.pts//2
                    elif divisor.state==True and multiplier.state==True:
                        player_pts+=pigarto.pts
                    else:
                        player_pts+=pigarto.pts
                player_item=""
                
                pigarto.resetear_ruta()
                if pigarto.hp<=0:
                    if multiplier.state==True and divisor.state==False:
                        player_pts+=pigarto.pts*2
                    elif divisor.state==True and multiplier.state==False:
                        player_pts+=pigarto.pts//2
                    elif divisor.state==True and multiplier.state==True:
                        player_pts+=pigarto.pts
                    else:
                        player_pts+=pigarto.pts
                    pigarto.exist=0
            elif player_item==ring.name:
                player_pts+=pigarto.pts
                player_item=""
                pigarto.exist=0
                cfg.play_sfx("enemy_die")
                
            elif inmunidad!=1 and player_hp-pigarto.damage>0:
                player_x=cr.player.positions_x
                player_y=cr.player.positions_y
                player_hp-=pigarto.damage
                cfg.play_sfx("player_hurt")
            elif inmunidad!=1 and player_hp-pigarto.damage<=0:
                cfg.play_sfx("player_hurt")
                print("💀 pigarto")
                pygame.mixer.music.stop() 
                if cfg.es_top_3(player_pts):
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return True #Volver al menú
                else:
                    return False #Mostrar pantalla bajo puntaje
            
        #Con Raiz negativa
        if raiznegativa.colisionar(player_y, player_x) and colision_detected==False:
            colision_detected=True
            if player_item==shield.name:
                if multiplier.state==True and divisor.state==False:
                    player_pts+=raiznegativa.pts*2
                elif divisor.state==True and multiplier.state==False:
                    player_pts+=raiznegativa.pts//2
                elif divisor.state==True and multiplier.state==True:
                    player_pts+=raiznegativa.pts
                else:
                    player_pts+=raiznegativa.pts
                player_item=""
                raiznegativa.exist=0
                inmunidad=0
                cfg.play_sfx("enemy_die")
            elif player_item==sword.name:
                raiznegativa.hp-=sword.damage
                raiznegativa.positions_x=10
                raiznegativa.positions_y=9
                player_item=""
                cfg.play_sfx("player_hurt")
                if raiznegativa.hp<=0:
                    raiznegativa.exist=0
                    if multiplier.state==True and divisor.state==False:
                        player_pts+=raiznegativa.pts*2
                    elif divisor.state==True and multiplier.state==False:
                        player_pts+=raiznegativa.pts//2
                    elif divisor.state==True and multiplier.state==True:
                        player_pts+=raiznegativa.pts
                    else:
                        player_pts+=raiznegativa.pts
                else:
                    player_pts+=100
            elif inmunidad!=1 and player_hp-raiznegativa.damage>0:
                player_x=cr.player.positions_x
                player_y=cr.player.positions_y
                player_hp-=raiznegativa.damage
                cfg.play_sfx("player_hurt")
            elif inmunidad!=1 and player_hp-raiznegativa.damage<=0:
                cfg.play_sfx("player_hurt")
                print("💀 raiz")
                pygame.mixer.music.stop() 
                if cfg.es_top_3(player_pts):
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return True #Volver al menú 
                else:
                    return False #Mostrar pantalla bajo puntaje
        
        #COLISIÓN CON ITEMS
        #Espada
        if sword.colision(player_y, player_x):
            player_item=sword.name
            sword.actual_x=0
            sword.actual_y=1
            if multiplier.state==True and divisor.state==False:
                player_pts+=sword.pts*2
            elif divisor.state==True and multiplier.state==False:
                player_pts+=sword.pts//2
            elif divisor.state==True and multiplier.state==True:
                player_pts+=sword.pts
            else:
                player_pts+=sword.pts
            inmunidad=0
            cfg.play_sfx("item_pickup")
            
        #Escudo
        if shield.colision(player_y, player_x):
            player_item=shield.name
            inmunidad=1
            shield.actual_x=0
            shield.actual_y=2
            if multiplier.state==True and divisor.state==False:
                player_pts+=shield.pts*2
            elif divisor.state==True and multiplier.state==False:
                player_pts+=shield.pts//2
            elif divisor.state==True and multiplier.state==True:
                player_pts+=shield.pts
            else:
                player_pts+=shield.pts
            cfg.play_sfx("item_pickup")
        
        #Anillo
        if ring.colision(player_y, player_x):
            player_item=ring.name
            ring.actual_x=0
            ring.actual_y=3
            if multiplier.state==True and divisor.state==False:
                player_pts+=ring.pts*2
            elif divisor.state==True and multiplier.state==False:
                player_pts+=ring.pts//2
            elif divisor.state==True and multiplier.state==True:
                player_pts+=ring.pts
            else:
                player_pts+=ring.pts
            inmunidad=0
            cfg.play_sfx("item_pickup")
            
        #Power-ups
        """
        #Funcionaria de no ser por un problema con los cambios de velocidad del jugador.
        if speed_boost.colision(player_y, player_x):
            if speed_boost.pos==-1: #es la forma auxiliar de expresar que la variable no se ha usado
                speed_boost.pos=60*4 #pos se usará como auxiliar para contar la cnatidad de frames (frame*segunodp)
                speed=4 #tiene que ser divisor de 32
            else:
                speed_boost.pos-=1
                #if speed_boost.pos==0:
                #    speed=2
                #    speed_boost.pos=-1 #resetear variable auxiliar
        """
        if slow_time.colision(player_y, player_x):
            cfg.play_sfx("buff_pickup")
            if multiplier.state==True and divisor.state==False:
                player_pts+=slow_time.pts*2
            elif divisor.state==True and multiplier.state==False:
                player_pts+=slow_time.pts//2
            elif divisor.state==True and multiplier.state==True:
                player_pts+=slow_time.pts
            else:
                player_pts+=slow_time.pts
            if slow_time.pos==-1: #es la forma auxiliar de expresar que la variable no se ha usado
                slow_time.pos=60*10 #pos se usará como auxiliar para contar la cnatidad de frames (frame*segunodp)
                aux=[cero.movement_ratio, pigarto.movement_ratio, raiznegativa.movement_ratio]
                cero.movement_ratio=cero.movement_ratio*2
                pigarto.movement_ratio=pigarto.movement_ratio*2
                raiznegativa.movement_ratio=raiznegativa.movement_ratio*2
                
        if slow_time.pos!=-1:
            slow_time.pos-=1
            if slow_time.pos==0:
                cero.movement_ratio=aux[0]
                pigarto.movement_ratio=aux[1]
                raiznegativa.movement_ratio=aux[2]
                slow_time.pos=-1 #resetear variable auxiliar
                
        if multiplier.colision(player_y, player_x):
            cfg.play_sfx("buff_pickup")
            if multiplier.pos==-1:
                multiplier.pos=60*15
                multiplier.state=True
                multiplier.spawned=False
        if multiplier.pos!=-1:
            multiplier.pos-=1
            if multiplier.pos==0:
                multiplier.pos=-1
                multiplier.state=False
        
        if divisor.colision(player_y, player_x):
            cfg.play_sfx("buff_pickup")
            if divisor.pos==-1:
                divisor.pos=60*15
                divisor.state=True
                divisor.spawned=False
        if divisor.pos!=-1:
            divisor.pos-=1
            if divisor.pos==0:
                divisor.pos=-1
                divisor.state=False
            
        # DIBUJO DE todo LO QUE SE VE EN PANTALLA
        #Mapa
        #for anidado para recorrer todas las filas (r) y columnas (c)
        #matriz.maze contiene valores si una celda es pared (0)
        #suelo transitable (1) o teletransporte (2) o (3)
        #al momento de dibujar solo se distingue entre pared y suelo
        for r in range(FILAS):
            for c in range(COLUMNAS):
                # Calculamos la posición en píxeles donde se dibujará cada tile.
                # Se multiplica la columna/fila por el tamaño del tile (32 px)
                # y se suma offset_x/y para centrar visualmente el laberinto en pantalla.
                #Recorremos matriz y multiplicamos por 32
                #Por ejemplo si tenemos (0,1) se dibuja en (32px, 0px)
                #Se le suma offset_x/y para dibujar mapa centrado y que no empieze en (0,0)
                x = c * cfg.TILE + cfg.offset_x
                y = r * cfg.TILE + cfg.offset_y
                #Si celda vale 0 sera una pared y se dibuja en sus respectivas cordenas con .blit()
                if colision.maze[r][c] == 0:
                    screen.blit(WALL, (x, y))
                #En cualquier otro caso 1,2,3 sera dibujado como suelo transitable
                else:
                    screen.blit(FLOOR, (x, y))
          
        # ENEMIGOS 
        # Cada enemigo tiene su propio método .dibujar(), el cual sabe
        # cómo colocarse correctamente en la pantalla según su posición (x, y).
        # screen: superficie principal donde se dibuja el juego
        # CERO: sprite del enemigo
        # cfg.TILE: tamaño de cada tile del mapa (32 px)
        # cfg.offset_x / cfg.offset_y: desplazamiento para centrar el laberinto
        cero.dibujar(screen, CERO, cfg.TILE, cfg.offset_x, cfg.offset_y)
        pigarto.dibujar(screen, PIGARTO, cfg.TILE, cfg.offset_x, cfg.offset_y)
        raiznegativa.dibujar(screen, RAIZNEGATIVA, cfg.TILE, cfg.offset_x, cfg.offset_y)
        
        #ITEMS
        # ITEMS
        # Cada ítem tiene su propio método .draw(), el cual sabe
        # cómo colocarse correctamente en la pantalla según su posición dentro del mapa.
        # screen: superficie principal donde se dibuja el juego.
        # El método .draw() se encarga internamente de:
        #   - convertir la posición del ítem en la matriz (fila, columna)
        #     a coordenadas de píxeles usando TILE.
        #   - aplicar offset_x y offset_y para centrar el mapa en pantalla.
        #   - dibujar su sprite en la ubicación correcta del laberinto.
        sword.draw(screen)
        shield.draw(screen)
        ring.draw(screen)
        #speed_boost.draw(screen)
        slow_time.draw(screen)
        multiplier.draw(screen)
        divisor.draw(screen)
        # EFECTO DE FLOTACIÓN DEL MAGO ARRIBA/ABAJO
        #float_offset es cambio constante en eje y
        """ float_offset = 0----> desplazamiento vertical que se suma a mago, ej con 1 baja 1 pixel con -2 sube 2 pixeles
            float_direction = 1   1---> se mueve hacia abajo y -1 hacia arriba
        """
        float_offset += float_direction * 0.2
        # Si el desplazamiento supera +2 píxeles, el mago debe empezar a moverse hacia arriba.
        if float_offset > 2:
            float_direction = -1
        # Si el desplazamiento supera -2 píxeles, el mago debe empezar a moverse hacia abajo.
        elif float_offset < -2:
            float_direction = 1
                # --- LÓGICA DE ANIMACIÓN ---
        if dir_x == 0 and dir_y == 0:
            # Si está quieto, usamos el frame 0 (estático)
            frame = 0
        else:
            # Si se mueve, alternamos frame cada 200 milisegundos aprox.
            # pygame.time.get_ticks() // 200 nos da un número que cambia cada 0.2 seg
            # % 2 hace que ese número solo sea 0 o 1
            frame = (pygame.time.get_ticks() // 200) % 2 
        
        # --- DIBUJO DEL MAGO ---
        screen.blit(
            lista_actual[frame], # Selecciona el frame 0 o 1 de la lista activa
            (
                player_x * cfg.TILE + cfg.offset_x,
                player_y * cfg.TILE + cfg.offset_y + float_offset
            )
        )
                
        
        temporizador+=1
        if colision_detected==True:
            if invul_frames>0:
                invul_frames-=1
            elif invul_frames<=0:
                invul_frames=invul_base #Invul_frame vuelve a la constante original
                colision_detected=False
        
# Lógica de VICTORIA
        if pigarto.exist == 0 and cero.exist == 0 and raiznegativa.exist == 0 and not victoria_detectada:
            victoria_detectada = True
            print("Puntaje sin bonus por tiempo:", player_pts)
            print("Segundos", temporizador / 60)
            if temporizador / 60 <= 12:
                player_pts += 2000
                print("TIEMPO INHUMANO") 
            elif temporizador / 60 <= 15:
                player_pts += 1000
            elif temporizador / 60 <= 20:
                player_pts += 500
            elif temporizador / 60 <= 40:
                player_pts += 250
            elif temporizador / 60 <= 60:
                player_pts += 100
            else:
                player_pts += 0
                            
            print("Puntaje total:", player_pts)
            mostrando_mensaje_victoria = True
            mensaje_temporizador = 90  # 1.5 segundos a 60 FPS
       
        # Manejo del mensaje de victoria
        if mostrando_mensaje_victoria:
            mensaje_temporizador -= 1 # Por cada frame del juego, se va restando 1 hasta que se cumplan los 3 segundos
            if mensaje_temporizador <= 0:
                reiniciar_juego()  # Reinicia todo excepto el puntaje después del mensaje
                mostrando_mensaje_victoria = False
            else:
                # Dibuja el mensaje de victoria (fondo negro y texto)
                overlay = pygame.Surface((cfg.ANCHO_PANTALLA, cfg.ALTO_PANTALLA), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 255))  # Fondo negro 
                screen.blit(overlay, (0, 0)) # Comienza a dibujar desde la esquina izquierda
                
                fuente_titulo = cfg.get_letra(60)
                fuente_sub = cfg.get_letra(30)
                texto_titulo = fuente_titulo.render("¡NIVEL COMPLETADO!", True, (255, 255, 0))  # Amarillo
                texto_puntaje = fuente_sub.render(f"PUNTAJE ACUMULADO: {player_pts}", True, (255, 255, 255))  # Blanco
                
                screen.blit(texto_titulo, texto_titulo.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y - 50))) # Dibujar en la pantalla
                screen.blit(texto_puntaje, texto_puntaje.get_rect(center=(cfg.CENTRO_X, cfg.CENTRO_Y + 50))) # Dibujar en la pantalla
    
        dibujar_hud(screen, player_pts, player_hp, player_item) 
        pygame.display.flip() # Actualizar la pantalla

    # Si sale del bucle 'while running' por QUIT o ESCAPE, regresa al menú
    return True # Indica que debe ir al menú principal