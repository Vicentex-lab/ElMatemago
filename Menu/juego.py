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
        fuente_item = cfg.get_letra(22)  # Definir fuente para el ítem (agregado para corregir)
        txt_item = fuente_item.render("ITEM:", True, (255, 255, 255))
        screen.blit(txt_item, (hud_x + 30, hud_y + 160))
    
        # Selección del sprite del ítem
        if player_item == sword.name:
            sprite = ESPADA
        elif player_item == shield.name:
            sprite = ESCUDO
        elif player_item == ring.name:
            sprite = ANILLO
        else:
            sprite = None  # Si no tiene ítem, no hay imagen que mostrar
    
        if sprite:
            ITEM_HUD = pygame.transform.scale(sprite, (40, 40))  # Tamaño ideal para el HUD
            screen.blit(ITEM_HUD, (hud_x + 160, hud_y + 160))
        else:
            # Si NO hay un ítem equipado, se escribe la palabra "NINGUNO"
            txt_none = fuente_item.render("NINGUNO", True, (160, 160, 160))
            screen.blit(txt_none, (hud_x + 160, hud_y + 160))

    
    FPS = 60
    
    FILAS = len(colision.maze)
    COLUMNAS = len(colision.maze[0])
    
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
    invul_frames=2*60 #segundos*FPS para frames
    colision_detected=True
    
    # Nueva bandera para evitar acumulación de bonus de victoria
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
    
    def reiniciar_juego():
        nonlocal player_y, player_x, player_hp, player_item, inmunidad, temporizador, invul_frames, colision_detected
        nonlocal dir_x, dir_y, move_timer, float_offset, float_direction
        nonlocal player_pts  # Conservar el puntaje
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
        
        # Resetear bandera de victoria
        victoria_detectada = False
        
        print("Juego reiniciado")
    
    #Instanciar ENEMIGO
    cero = cr.cero()
    pigarto=cr.pigarto()
    raiznegativa=cr.raiznegativa()
    
    # ============================
    #  MOVIMIENTO DEL JUGADOR 
    # ============================
    dir_x = 0    # La dirección en donde se mueve le personaje en x
    dir_y = 0    # En y
    move_timer = 0     # acomula tiempo
    move_delay = 120   # velocidad del personaje 
    
    running = True
    mostrando_mensaje_victoria = False  
    mensaje_temporizador = 0  # Temporizador para el mensaje (en frames)
    
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
                    return True 

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
                if pigarto.exist==1 and raiznegativa.exist==0:
                    print("espada: cero")
                    sword.actual_y=cero.positions_y
                    sword.actual_x=cero.positions_x
            elif inmunidad!=1 and player_hp-cero.damage>0:
                player_x=cr.player.positions_x
                player_y=cr.player.positions_y
                player_hp-=cero.damage
            elif inmunidad!=1 and player_hp-cero.damage<=0:
                print("💀 cero")
                pygame.mixer.music.stop() 
                if player_pts > 0:
                    cfg.guardar_nuevo_puntaje(screen, player_pts)
                    return True
                else:
                    return False
            
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
                    return True
                else:
                    return False
            
        #Con Raiz negativa
        if raiznegativa.colisionar(player_y, player_x) and colision_detected==False:
            colision_detected=True
            if player_item==shield.name:
                player_pts+=raiznegativa.pts
                player_item=""
                raiznegativa.exist=0
                inmunidad=0
                if pigarto.exist==1 and cero.exist==0:
                    print("espada: cero")
                    sword.actual_y=cero.positions_y
                    sword.actual_x=cero.positions_x
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
                    return True
                else:
                    return False
        
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
        for r in range(FILAS):
            for c in range(COLUMNAS):
                x = c * cfg.TILE + cfg.offset_x
                y = r * cfg.TILE + cfg.offset_y
                if colision.maze[r][c] == 0:
                    screen.blit(WALL, (x, y))
                else:
                    screen.blit(FLOOR, (x, y))
          
        # ENEMIGOS 
        cero.dibujar(screen, CERO, cfg.TILE, cfg.offset_x, cfg.offset_y)
        pigarto.dibujar(screen, PIGARTO, cfg.TILE, cfg.offset_x, cfg.offset_y)
        raiznegativa.dibujar(screen, RAIZNEGATIVA, cfg.TILE, cfg.offset_x, cfg.offset_y)
        
        #ITEMS
        sword.draw(screen)
        shield.draw(screen)
        ring.draw(screen)
        
        # EFECTO DE FLOTACIÓN DEL MAGO
        float_offset += float_direction * 0.2
        if float_offset > 2:
            float_direction = -1
        elif float_offset < -2:
            float_direction = 1
        screen.blit(
            MAGO,
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
                invul_frames=2*60
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
            mensaje_temporizador -= 1 
            if mensaje_temporizador <= 0:
                reiniciar_juego()  # Reinicia todo después del mensaje
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
