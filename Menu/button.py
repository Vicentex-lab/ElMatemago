class Button():
    # El constructor de la clase. Se llama al crear un nuevo botón.
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        # 1. Almacenamiento de Atributos Básicos
        self.image = image # La imagen de fondo del botón (puede ser None).
        self.x_pos = pos[0] # Coordenada X central.
        self.y_pos = pos[1] # Coordenada Y central.
        self.font = font # Objeto de fuente de Pygame.
        self.base_color, self.hovering_color = base_color, hovering_color # Colores de texto.
        self.text_input = text_input # El texto que se mostrará (ej. "JUGAR").

        # 2. Renderizado Inicial del Texto
        # Renderiza el texto la primera vez, usando el color base.
        # Esto crea una superficie (Surface) de Pygame con el texto.
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        # 3. Asignación de Imagen de Fondo
        # Si no se proporciona una imagen, usa la superficie del texto como imagen base.
        if self.image is None:
            self.image = self.text
            
        # 4. Creación de Rectángulos (Áreas de Colisión/Posición)
        # self.rect es el rectángulo que define el área de la imagen/botón.
        # Se usa para el cálculo de la posición y la detección de colisiones del mouse.
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
        # self.text_rect es el rectángulo que define el área del texto.
        # Asegura que el texto esté centrado correctamente, incluso si la imagen es None.
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # Método para dibujar el botón en la pantalla
    def update(self, screen):
        # Dibuja la imagen de fondo si existe.
        if self.image is not None:
            screen.blit(self.image, self.rect)
        # Dibuja el texto renderizado encima de la imagen (o solo el texto si image es None).
        screen.blit(self.text, self.text_rect)

    # Método para verificar si el cursor del mouse está sobre el botón
    def checkForInput(self, position):
        # position es la tupla (x, y) del cursor del mouse.
        
        # Comprueba si la coordenada X del mouse está dentro del rango horizontal del rectángulo.
        # Y si la coordenada Y del mouse está dentro del rango vertical del rectángulo.
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True # El mouse está sobre el botón (o ha hecho clic en él).
        return False # El mouse está fuera del botón.

    # Método para cambiar el color del texto si el mouse está encima (efecto hover)
    def changeColor(self, position):
        # Comprueba si el mouse está sobre el área del botón.
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            # Si está encima, renderiza el texto usando el color de "hovering".
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            # Si no está encima, renderiza el texto usando el color base.
            self.text = self.font.render(self.text_input, True, self.base_color)