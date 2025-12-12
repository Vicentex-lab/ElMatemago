import configuracion as cfg
import random
from sprites import ESPADA, ESCUDO, ANILLO

class item():
    def __init__(self, places_y, places_x, name, damage, pts, pos, actual_y, actual_x, obj_sprite):
        self.name=name
        self.damage=damage
        self.pts=pts
        self.places_y=places_y
        self.places_x=places_x
        self.pos=pos
        self.actual_y=actual_y
        self.actual_x=actual_x
        self.obj_sprite=obj_sprite
        
    def spawn(self):
        self.pos=random.randint(0, len(self.places_x)-1)
        self.actual_y=self.places_y[self.pos]
        self.actual_x=self.places_x[self.pos]
    
    def colision(self, player_y, player_x):
        if self.actual_y == player_y and self.actual_x == player_x:
            return True
        return False
    
    def draw(self, screen):
        screen.blit(
            self.obj_sprite,
            (
                self.actual_x * cfg.TILE + cfg.offset_x,
                self.actual_y * cfg.TILE + cfg.offset_y
            )
        )

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
            obj_sprite=ESPADA
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
        obj_sprite=ESCUDO
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
        obj_sprite=ANILLO
        )
    
class mathray(item):
    name="Materayo"
    places_y=[11]
    places_x=[9]
    damage=99999
    pts=250
    pos=0
    actual_x=0
    actual_y=0
    obj_sprite=0