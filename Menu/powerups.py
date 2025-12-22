import items as item
from sprites import SPEED_BOOST, SLOW_TIME, MULTIPLIER, DIVISOR

"""
class powerup(item.item):
    def __init__(self):
        super().__init__(
            name="",
            places_y=0,
            places_x=0,
            damage=0,
            pts=100,
            pos=0,
            actual_x=0,
            actual_y=0,
            obj_sprite=""
        )
"""
    
class speed_boost(item.item):
    def __init__(self):
        super().__init__(
            name="e",
            places_y=0,
            places_x=0,
            damage=0,
            pts=100,
            pos=-1,
            actual_x=0,
            actual_y=0,
            obj_sprite=SPEED_BOOST,
            exist=1
            )
    
class slow_time(item.item):
    def __init__(self):
        super().__init__(
            name="Tiempo Ralentizado",
            places_y=0,
            places_x=0,
            damage=0,
            pts=100,
            pos=-1,
            actual_x=0,
            actual_y=0,
            obj_sprite=SLOW_TIME,
            exist=1
            )

class multiplier(item.item):
    def __init__(self):
        super().__init__(
            name="Multiplicador",
            places_y=0,
            places_x=0,
            damage=0,
            pts=100,
            pos=-1,
            actual_x=0,
            actual_y=0,
            obj_sprite=MULTIPLIER,
            exist=0
            )
        self.state=False
        self.spawned=False
        
class divisor(item.item):
    def __init__(self):
        super().__init__(
            name="Divisor",
            places_y=0,
            places_x=0,
            damage=0,
            pts=100,
            pos=-1,
            actual_x=0,
            actual_y=0,
            obj_sprite=DIVISOR,
            exist=0
        )
        self.state=False
        self.spawned=False