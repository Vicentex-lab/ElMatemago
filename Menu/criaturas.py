import colisiones
import pygame

class criature:
    def __init__(self, hp, movement_ratio, name, positions_x, positions_y, pos, exist, pts, damage, cooldown):
        self.positions_x=positions_x
        self.positions_y=positions_y
        self.pos=pos
        self.hp=hp
        self.movement_ratio=movement_ratio
        self.name=name
        self.exist=exist
        self.pts=pts
        self.damage=damage
        self.cooldown=cooldown

class player(criature):
    positions_x=10
    positions_y=23
    hp=3
    movement_ratio=1 #El jugador funciona bloque por bloque.
    name=""
    pts=0

#Los monstruos funcionan por tiempo de espera (Milisegundos)

class cero(criature):
    def __init__(self):
        # Inicializamos con los valores por defecto
        super().__init__(
            hp=2, 
            movement_ratio=250, 
            name="Cero", 
            positions_x=10, 
            positions_y=13, 
            pos=0, 
            exist=1, 
            pts=500, 
            damage=1,
            cooldown=0
        )

    def mover(self, target_y, target_x, maze):
        """Calcula el movimiento hacia el jugador respetando paredes y cooldown"""
        if not self.exist:
            return

        ahora = pygame.time.get_ticks()
            
        # Verificamos si ya pasó el tiempo para moverse
        if ahora - self.cooldown >= self.movement_ratio:
            self.cooldown = ahora
            
            pos_y = self.positions_y
            pos_x = self.positions_x
            
            # Lógica de movimiento (Inteligencia artificial simple)
            moved = False
            
            # Helper interno para verificar paredes
            def can_move(r, c):
                filas = len(maze)
                cols = len(maze[0])
                # Asumiendo que > 0 es suelo transitable
                return 0 <= r < filas and 0 <= c < cols and maze[r][c] >= 1

            # Intentar moverse verticalmente
            if target_y < pos_y and can_move(pos_y - 1, pos_x):
                self.positions_y -= 1
                moved = True
            elif target_y > pos_y and can_move(pos_y + 1, pos_x) and not moved:
                self.positions_y += 1
                moved = True
            
            # Intentar moverse horizontalmente (si no se movió en vertical o quieres diagonal)
            # El código original usaba elif, así que prioriza eje Y
            elif target_x < pos_x and can_move(pos_y, pos_x - 1) and not moved:
                self.positions_x -= 1
            elif target_x > pos_x and can_move(pos_y, pos_x + 1) and not moved:
                self.positions_x += 1

    def colisionar(self, player_y, player_x):
        """Retorna True si Cero está en la misma casilla que el jugador"""
        if self.exist==1 and self.positions_y == player_y and self.positions_x == player_x:
            return True
        return False

    def dibujar(self, screen, sprite, tile_size, offset_x, offset_y):
        """Se dibuja a sí mismo en la pantalla"""
        if self.exist:
            screen.blit(
                sprite,
                (
                    self.positions_x * tile_size + offset_x,
                    self.positions_y * tile_size + offset_y
                )
            )
    

class pigarto(criature):
    def __init__(self):
        # Definimos las rutas COMO ATRIBUTOS DE INSTANCIA
        self.path_x = [10, 10, 9, 8, 8, 7, 6, 6, 5, 4, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 3, 3, 2, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14, 15, 15, 15, 16, 17, 17, 17, 18, 18, 18, 17, 17, 17, 16, 16, 16, 17, 17, 17, 17, 16, 16, 16, 16, 17, 17, 17, 17, 16, 16, 16, 17, 18, 18, 18, 18, 18, 17, 16, 15, 14, 14, 13, 12, 11, 10, 0]
        self.path_y = [3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16, 17, 18, 19, 19, 20, 21, 21, 22, 22, 23, 24, 24, 25, 25, 25, 24, 24, 23, 23, 23, 23, 23, 23, 23, 23, 23, 24, 24, 25, 26, 26, 26, 25, 24, 24, 23, 22, 22, 21, 20, 20, 19, 18, 18, 17, 16, 15, 15, 14, 13, 12, 11, 11, 10, 9, 8, 8, 7, 6, 6, 6, 5, 4, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 0]

        super().__init__(
            hp=3.141592731, 
            movement_ratio=75, 
            name="Pigarto", 
            positions_x=self.path_x[0], # Posición inicial actual
            positions_y=self.path_y[0], 
            pos=0, 
            exist=1, 
            pts=500, 
            damage=1,
            cooldown=0
        )

    def mover(self):
        """Avanza en su ruta predefinida"""
        if not self.exist:
            return

        ahora = pygame.time.get_ticks()
        
        if ahora - self.cooldown >= self.movement_ratio:
            self.cooldown = ahora
            
            # Avanzar índice
            self.pos += 1
            
            # Si llega al final de la ruta (o al marcador de muerte/reinicio)
            if self.pos >= len(self.path_x) or self.pos >= 106: # Manteniendo tu lógica original de 106
                self.pos = 0
            
            # Actualizamos las coordenadas actuales para que coincidan con el índice
            self.positions_x = self.path_x[self.pos]
            self.positions_y = self.path_y[self.pos]

    def colisionar(self, player_y, player_x):
        """Verifica si la posición actual de la ruta toca al jugador"""
        if self.exist == 1 and self.positions_y == player_y and self.positions_x == player_x:
            return True
        return False

    def dibujar(self, screen, sprite, tile_size, offset_x, offset_y):
        if self.exist:
            screen.blit(
                sprite,
                (
                    self.positions_x * tile_size + offset_x,
                    self.positions_y * tile_size + offset_y
                )
            )
            
    def resetear_ruta(self):
        """Método auxiliar para enviar al Pigarto al inicio"""
        self.pos = 0
        self.positions_x = self.path_x[0]
        self.positions_y = self.path_y[0]

class raiznegativa(criature):
    def __init__(self):
        super().__init__(
            hp=6, 
            movement_ratio=350,
            name="Raiz negativa",
            pos=0,
            positions_x=10,
            positions_y=9,
            exist=1, 
            pts=500, 
            damage=1,
            cooldown=0
        )
        self.ratios=[350, 150] #0=Normal, 1=Rápida
        
    def mover(self, target_y, target_x, maze):
        """Calcula el movimiento hacia el jugador respetando paredes y cooldown"""
        if not self.exist:
            return

        ahora = pygame.time.get_ticks()
        
        if target_y==self.positions_y or target_x==self.positions_x:
            self.movement_ratio=self.ratios[1] #Velocidad Rápida
        else:
            self.movement_ratio=self.ratios[0] #Velocidad Normal
        
        # Verificamos si ya pasó el tiempo para moverse
        if ahora - self.cooldown >= self.movement_ratio:
            self.cooldown = ahora
            
            pos_y = self.positions_y
            pos_x = self.positions_x
            
            # Lógica de movimiento (Inteligencia artificial simple)
            moved = False
            
            # Helper interno para verificar paredes
            def can_move(r, c):
                filas = len(maze)
                cols = len(maze[0])
                # Asumiendo que > 0 es suelo transitable
                return 0 <= r < filas and 0 <= c < cols and maze[r][c] >= 1

            # Intentar moverse verticalmente
            if target_y < pos_y and can_move(pos_y - 1, pos_x):
                self.positions_y -= 1
                moved = True
            elif target_y > pos_y and can_move(pos_y + 1, pos_x) and not moved:
                self.positions_y += 1
                moved = True
            
            # Intentar moverse horizontalmente (si no se movió en vertical o quieres diagonal)
            # El código original usaba elif, así que prioriza eje Y
            elif target_x < pos_x and can_move(pos_y, pos_x - 1) and not moved:
                self.positions_x -= 1
            elif target_x > pos_x and can_move(pos_y, pos_x + 1) and not moved:
                self.positions_x += 1

    def colisionar(self, player_y, player_x):
        """Retorna True si Cero está en la misma casilla que el jugador"""
        if self.exist==1 and self.positions_y == player_y and self.positions_x == player_x:
            return True
        return False

    def dibujar(self, screen, sprite, tile_size, offset_x, offset_y):
        """Se dibuja a sí mismo en la pantalla"""
        if self.exist:
            screen.blit(
                sprite,
                (
                    self.positions_x * tile_size + offset_x,
                    self.positions_y * tile_size + offset_y
                )
            )