class criature:
    def __init__(self, hp, speed, name, positions_x, positions_y):
        self.positions_x=positions_x
        self.positions_y=positions_y
        self.hp=hp
        self.speed=speed
        self.name=name

class player(criature):
    hp=3
    speed=1
    name=""

class cero(criature):
    hp=2
    speed=1
    name="Cero"

class pigarto(criature):
    hp=6
    speed=4
    name="Pigarto"
    positions_x=[2, 2, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20]#20
    positions_x=[2, 2, 3, [6, 4], [5, 4], [4, 4], [3, 5], [2, 6], [2, 7], [2, 8], [3, 9], [2, 10], [2, 11], [2, 12], [3, 13], [4, 14], [4, 15], [3, 16], [3, 17], [3, 18], [4, 19], [4, 20], [5, 21], [6, 22], [7, 23], [8, 23], [9, 23], [10, 23], [11, 23], [12, 23], [13, 23], [14, 22], [15, 21], [16, 20], [16, 19], [15, 17], [15, 16], [16, 15], [16, 14], [16, 13], [16, 12], [16, 11], [15, 10], [15, 9], [16, 8], [16, 7], [15, 6], [14, 5], [14, 4], [13, 3], [12, 3], [11, 3], [10, 2]]
    positions_y=[9, 8, 7, 6, 5, 4, 3, 2, 2, 2, 3, 2, 2, 2, 3, 4, 4, 3, 3, 3, 4, 4, 5, 6,]