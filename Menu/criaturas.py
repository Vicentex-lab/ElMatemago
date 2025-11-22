class criature:
    def __init__(self, hp, speed, name, positions_x, positions_y):
        self.positions_x=positions_x
        self.positions_y=positions_y
        self.hp=hp
        self.speed=speed
        self.name=name

class player(criature):
    positions_x=10
    positions_y=23
    hp=3
    speed=1
    name=""

class cero(criature):
    positions_x=10
    positions_y=13
    hp=2
    speed=1
    name="Cero"
    
class pigarto(criature):
    hp=3.141592731
    speed=4
    name="Pigarto"
    positions_x=[10, 10, 9, 8, 8, 7, 6, 6, 5, 4, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 3, 3, 2, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14, 15, 15, 15, 16, 17, 17, 17, 18, 18, 18, 17, 17, 17, 16, 16, 16, 17, 17, 17, 17, 16, 16, 16, 16, 17, 17, 17, 17, 16, 16, 16, 17, 18, 18, 18, 18, 18, 17, 16, 15, 14, 14, 13, 12, 11, 10] 
    positions_y=[3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16, 17, 18, 19, 19, 20, 21, 21, 22, 22, 23, 24, 24, 25, 25, 25, 24, 24, 23, 23, 23, 23, 23, 23, 23, 23, 23, 24, 24, 25, 26, 26, 26, 25, 24, 24, 23, 22, 22, 21, 20, 20, 19, 18, 18, 17, 16, 15, 15, 14, 13, 12, 11, 11, 10, 9, 8, 8, 7, 6, 6, 6, 5, 4, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3,] 
    
class raiznegativa(criature):
    hp=3
    speed=1
    name="Raiz negativa"
    