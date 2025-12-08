import pygame, sys
import random
import configuracion as cfg
import colisiones as colision 
import criaturas as cr         
import items as item           
from sprites import CERO, RAIZNEGATIVA, PIGARTO, ESPADA, ESCUDO, ANILLO, CORAZON, WALL, FLOOR

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
        txt_pts = fuente.render(f"PUNTAJE: {player_pts}", True, (255, 255, 120))   
        #.render convierte string en surface, mostramos puntaje jugador, True es para bordes suaves no pixelados
        screen.blit(txt_pts, (hud_x + 30, hud_y + 20))  # Se dibuja HUD creado en pantalla con su texto con sus coordenadas
    
        # SECCIÓN: VIDA 
        fuente_vida = cfg.get_letra(22)  #Funcion en cfg para retornar texto en pygame con tamaño 22
        #.render convierte string en surface, mostramos puntaje jugador, True es para bordes suaves no pixelados
        txt_vida = fuente_vida.render("VIDA:", True, (255, 255, 255))
        #.render convierte string en surface, mostramos puntaje jugador, True es para bordes suaves no pixelados
        screen.blit(txt_vida, (hud_x + 30, hud_y + 90))
        #nueva variable con corazon reescalado para que encaje con tamaño hud, escala 28x28
        CORAZON_HUD = pygame.transform.scale(CORAZON, (28, 28)) 
        # Dibujamos un corazón por cada punto de vida
        #Ciclo for para dibujar corazones, cada uno cambiara en "i * 32" pixeles a la derecha
        for i in range(player_hp):
            screen.blit(CORAZON_HUD, (hud_x + 150 + i*32, hud_y + 88)) 
    
            # SECCIÓN: ITEM
        fuente_item = cfg.get_letra(22)  #Funcion en cfg para retornar texto en pygame con tamaño 22
        txt_item = fuente_item.render("ITEM:", True, (255, 255, 255))
        #.render convierte string en surface, mostramos puntaje jugador, True es para bordes suaves no pixelados
        screen.blit(txt_item, (hud_x + 30, hud_y + 160)) # Se dibuja HUD creado en pantalla con su texto con sus coordenadas
    
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
            screen.blit(ITEM_HUD, (hud_x + 160, hud_y + 160))
        else:
            # Si NO hay un ítem equipado, se escribe la palabra "NINGUNO"
            txt_none = fuente_item.render("NINGUNO", True, (160, 160, 160)) 
            #.render convierte string en surface, mostramos puntaje jugador, True es para bordes suaves no pixelados
            screen.blit(txt_none, (hud_x + 160, hud_y + 160))
        #SECCION

    
    FPS = 60
    
    FILAS = len(colision.maze)
    COLUMNAS = len(colision.maze[0])
    
    screen = SCREEN # Usar la variable pasada como argumento
    clock = pygame.time.Clock()
    
    #Definiciones del jugador
    player_y = cr.player.positions_y
    player_x = cr.player.positions_x
    player_hp = cr.player.hp
    
    
    
    from sprites import MAGO_1, MAGO_2
    # --- Animación del mago Mago izquierda derecha
    player_sprite = MAGO_1      # sprite actual del mago
    anim_frame = 0              # alterna entre 0 y 1
    facing = "right"            # dirección actual del mago
    
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
        nonlocal player_y, player_x, player_hp, player_item, inmunidad, temporizador, invul_frames, colision_detected
        nonlocal dir_x, dir_y, float_offset, float_direction
        nonlocal player_pts  # Ignorar para conservar el puntaje
        nonlocal cero, pigarto, raiznegativa  # Instancias de enemigos que se reasignan
        nonlocal victoria_detectada  # Resetear la bandera
        
        # Reiniciar posición del jugador
        player_y = cr.player.positions_y
        player_x = cr.player.positions_x
        
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
        sword.spawn()
        while True:
            shield.spawn()
            if shield.actual_x != sword.actual_x or shield.actual_y != sword.actual_y:
                break
        while True:
            ring.spawn()
            if (ring.actual_x != sword.actual_x or ring.actual_y != sword.actual_y) and \
               (ring.actual_x != shield.actual_x or ring.actual_y != shield.actual_y):
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

                # Guardar dirección DESEADA siempre
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    deseada_x = 0
                    deseada_y = -1

                if event.key in (pygame.K_s, pygame.K_DOWN):
                    deseada_x = 0
                    deseada_y = 1
                #Animacion izquierda derecha mago
                
                
                if event.key in (pygame.K_a, pygame.K_LEFT):
                
                    deseada_x = -1
                    deseada_y = 0
                
                    # SOLO animar si la dirección cambió
                    if facing != "left":
                        facing = "left"
                        anim_frame = 1 - anim_frame
                        player_sprite = MAGO_1 if anim_frame == 0 else MAGO_2

                if event.key in (pygame.K_d, pygame.K_RIGHT):
                
                    deseada_x = 1
                    deseada_y = 0
                
                    # SOLO animar si la dirección cambió
                    if facing != "right":
                        facing = "right"
                        anim_frame = 1 - anim_frame
                        player_sprite = MAGO_1 if anim_frame == 0 else MAGO_2

   
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
            elif player_item==sword.name:
                player_pts+=cero.pts
                player_item=""
                cero.exist=0
            elif inmunidad!=1 and player_hp-cero.damage>0:
                player_x=cr.player.positions_x
                player_y=cr.player.positions_y
                player_hp-=cero.damage
            elif inmunidad!=1 and player_hp-cero.damage<=0:
                print("💀 cero")
                pygame.mixer.music.stop() 
                if player_pts > 0:
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
            elif player_item==sword.name:
                if cero.exist==1 or raiznegativa.exist==1:
                    pigarto.hp=pigarto.hp-sword.damage
                if cero.exist==0 and raiznegativa.exist==0 and pigarto.exist==1:
                    pigarto.exist=0
                    player_pts+=pigarto.pts
                player_item=""
                
                pigarto.resetear_ruta()
                if pigarto.hp<=0:
                    player_pts+=pigarto.pts
                    pigarto.exist=0
            elif player_item==ring.name:
                player_pts+=pigarto.pts
                player_item=""
                pigarto.exist=0
            elif inmunidad!=1 and player_hp-pigarto.damage>0:
                player_x=cr.player.positions_x
                player_y=cr.player.positions_y
                player_hp-=pigarto.damage
            elif inmunidad!=1 and player_hp-pigarto.damage<=0:
                print("💀 pigarto")
                pygame.mixer.music.stop() 
                if player_pts > 0:
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return True #Volver al menú
                else:
                    return False #Mostrar pantalla bajo puntaje
            
        #Con Raiz negativa
        if raiznegativa.colisionar(player_y, player_x) and colision_detected==False:
            colision_detected=True
            if player_item==shield.name:
                player_pts+=raiznegativa.pts
                player_item=""
                raiznegativa.exist=0
                inmunidad=0
            elif player_item==sword.name:
                raiznegativa.hp-=sword.damage
                raiznegativa.positions_x=10
                raiznegativa.positions_y=9
                player_item=""
                if raiznegativa.hp<=0:
                    raiznegativa.exist=0
                    player_pts+=raiznegativa.pts
                else:
                    player_pts+=100
            elif inmunidad!=1 and player_hp-raiznegativa.damage>0:
                player_x=cr.player.positions_x
                player_y=cr.player.positions_y
                player_hp-=raiznegativa.damage
            elif inmunidad!=1 and player_hp-raiznegativa.damage<=0:
                print("💀 raiz")
                pygame.mixer.music.stop() 
                if player_pts > 0:
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
            player_pts+=sword.pts
            inmunidad=0
            
        #Escudo
        if shield.colision(player_y, player_x):
            player_item=shield.name
            inmunidad=1
            shield.actual_x=0
            shield.actual_y=2
            player_pts+=shield.pts
        
        #Anillo
        if ring.colision(player_y, player_x):
            player_item=ring.name
            ring.actual_x=0
            ring.actual_y=3
            player_pts+=ring.pts
            inmunidad=0
            
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
        #Misma lógica de dibujado pero con sprite animado y flotamiento
        screen.blit(
            player_sprite,
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
            mensaje_temporizador = 180  # 3 segundos a 60 FPS
       
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
