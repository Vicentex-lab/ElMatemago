import criaturas as cr
import configuracion as cfg
import random
import colisiones as colision
from sprites import ESPADA, ESCUDO, ANILLO, SPEED_BOOST

class item():
    def __init__(self, places_y, places_x, name, damage, pts, pos, actual_y, actual_x, obj_sprite, exist):
        self.name=name
        self.damage=damage
        self.pts=pts
        self.places_y=places_y
        self.places_x=places_x
        self.pos=pos
        self.actual_y=actual_y
        self.actual_x=actual_x
        self.obj_sprite=obj_sprite
        self.exist=exist
        
    def spawn(self):
        self.pos=random.randint(0, len(self.places_x)-1)
        self.actual_y=self.places_y[self.pos]
        self.actual_x=self.places_x[self.pos]
    
    def colision(self, player_y, player_x):
        if self.actual_y == player_y and self.actual_x == player_x and self.exist==1:
            self.exist=0
            return True
        return False
    
    def draw(self, screen):
        if self.exist==1:
            screen.blit(
                self.obj_sprite,
                (
                    self.actual_x * cfg.TILE + cfg.offset_x,
                    self.actual_y * cfg.TILE + cfg.offset_y
                )
            )
    
    def random_spawn(self):
        while True:
            self.actual_y=random.randint(0, len(colision.maze)-1) #len(maze) toma cuantos arreglos tiene maze
            self.actual_x=random.randint(0, len(colision.maze[0])-1) #len(maze[0]) toma cuantos valores tiene el primer arreglo de maze
            if colision.maze[self.actual_y][self.actual_x]==1 and self.actual_x!=cr.player.positions_x and self.actual_y!=cr.player.positions_y:
                break
            else:
                continue

class sword(item):
    def __init__(self):
        super().__init__(
            name="Espada Divisora",
            places_y=[3, 2, 7, 11, 26, 23], #0, 1, 2, 3, 4, 5
            places_x=[16, 18, 2, 2, 17, 18],
            damage=2,
            pts=250,
            pos=0,
            actual_x=0,
            actual_y=0,
            obj_sprite=ESPADA,
            exist=1
            )

class shield(item):
    def __init__(self):
        super().__init__(
        name="Escudo Absoluto",
        places_y=[2, 2, 7, 9, 24, 11],
        places_x=[4, 9, 2, 17, 3, 2 ],
        damage=0,
        pts=250,
        pos=0,
        actual_x=0,
        actual_y=0,
        obj_sprite=ESCUDO,
        exist=1
    )
    
class ring(item):
    def __init__(self):
        super().__init__(
        name="Anillo de Pi",
        #cambiar spawns
        places_y=[3, 2, 7, 11, 26, 23], #0, 1, 2, 3, 4, 5
        places_x=[16, 18, 2, 2, 17, 18],
        damage=0,
        pts=250,
        pos=0,
        actual_x=0,
        actual_y=0,
        obj_sprite=ANILLO,
        exist=1
        )
    
class mathray(item):
    name="Materayo"
    places_y=[11]
    places_x=[9]