class item():
    def __init__(self, places, name, damage):
        self.places=places
        self.name=name
        self.damage=damage

class sword(item):       #amarillo
    name="Espada Divisora"
    places_y=[3, 2, 7, 11, 26, 23] #0, 1, 2, 3, 4, 5
    places_x=[16, 18, 2, 2, 17, 18]
    damage=3

class shield(item):    #naranjo
    name="Escudo Absoluto"
    places_y=[3, 2, 7, 11, 26, 23] #Cambiar
    places_x=[16, 18, 2, 2, 17, 18 ]
    damage=0