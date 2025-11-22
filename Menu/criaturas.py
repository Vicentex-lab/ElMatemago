import colisiones

class criature:
    def __init__(self, hp, movement_ratio, name, positions_x, positions_y, pos):
        self.positions_x=positions_x
        self.positions_y=positions_y
        self.pos=pos
        self.hp=hp
        self.movement_ratio=movement_ratio
        self.name=name

class player(criature):
    positions_x=10
    positions_y=23
    hp=3
    movement_ratio=1 #El jugador funciona bloque por bloque
    name=""

#Los monstruos funcionan por tiempo de espera (Milisegundos)

class cero(criature):
    positions_x=10
    positions_y=13
    hp=2
    movement_ratio=300
    name="Cero"

class pigarto(criature):
    hp=3.141592731
    movement_ratio=75
    name="Pigarto"
    pos=0
    positions_x=[10, 10, 9, 8, 8, 7, 6, 6, 5, 4, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 3, 3, 2, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14, 15, 15, 15, 16, 17, 17, 17, 18, 18, 18, 17, 17, 17, 16, 16, 16, 17, 17, 17, 17, 16, 16, 16, 16, 17, 17, 17, 17, 16, 16, 16, 17, 18, 18, 18, 18, 18, 17, 16, 15, 14, 14, 13, 12, 11, 10]  #106
    positions_y=[3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16, 17, 18, 19, 19, 20, 21, 21, 22, 22, 23, 24, 24, 25, 25, 25, 24, 24, 23, 23, 23, 23, 23, 23, 23, 23, 23, 24, 24, 25, 26, 26, 26, 25, 24, 24, 23, 22, 22, 21, 20, 20, 19, 18, 18, 17, 16, 15, 15, 14, 13, 12, 11, 11, 10, 9, 8, 8, 7, 6, 6, 6, 5, 4, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3] #106

class raiznegativa(criature):
    hp=3
    movement_ratio=300
    name="Raiz negativa"
    pos=0
    positions_x=11
    positions_y=13
    
    def estocada():
        if player.positions_x==raiznegativa.positions_x: #si están al mismo largo
            distance=raiznegativa.positions_y - player.positions_y #sacar distancia entre ambos
            if distance<0: #si el jugador esta por debajo
                if colisiones.maze[raiznegativa.positions_y+raiznegativa.pos][raiznegativa.positions_x]!=0 and raiznegativa.pos!=abs(distance):
                    raiznegativa.pos=0
                    raiznegativa.movement_ratio=75
                else:
                    raiznegativa.pos+=1
                    raiznegativa.movement_ratio=300