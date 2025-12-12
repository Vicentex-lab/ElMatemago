import items
import sprites

class powerup(items.item):
    def __init__(self):
        super().__init__(
            name="",
            places_y=[3, 2, 7, 11, 26, 23], #0, 1, 2, 3, 4, 5
            places_x=[16, 18, 2, 2, 17, 18],
            damage=0,
            pts=250,
            pos=0,
            actual_x=0,
            actual_y=0,
            obj_sprite=0
            )