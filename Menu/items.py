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
    damage=3
    pts=250

class shield(item):
    name="Escudo Absoluto"
    places_y=[3, 2, 7, 11, 26, 23] #Cambiar
    places_x=[16, 18, 2, 2, 17, 18 ]
    damage=0
    pts=250