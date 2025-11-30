class item():
    def __init__(self, places, name, damage, pts):
        self.places=places
        self.name=name
        self.damage=damage
        self.pts=pts

class sword(item):
    name="Espada Divisora"
    places_y=[3, 2, 7, 11, 26, 23] #0, 1, 2, 3, 4, 5
    places_x=[16, 18, 2, 2, 17, 18]
    damage=2
    pts=250

class shield(item):
    name="Escudo Absoluto"
    places_y=[2, 2, 7, 9, 24, 11]
    places_x=[4, 9, 2, 17, 3, 2 ]
    damage=0
    pts=250
    
class ring(item):
    name="Anillo de Pi"
    #cambiar spawns
    places_y=[3, 2, 7, 11, 26, 23] #0, 1, 2, 3, 4, 5
    places_x=[16, 18, 2, 2, 17, 18]
    damage=0
    pts=250
    
class mathray(item):
    name="Materayo"
    places_y=[11]
    places_x=[9]