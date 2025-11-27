
from PIL import Image, ImageTk
import tkinter
import os
import sys
import pygame
import main  

#  CONFIGURACIÓN VENTANA TK

ventana = tkinter.Tk()
ventana.configure(bg="black")
ventana.geometry("1000x800")
ventana.title("EL MATEMAGO - Menú")

# Frames / pantallas
frame_menu = tkinter.Frame(ventana, bg="black")
frame_menu.pack(fill="both", expand=True)

frame_jugar = tkinter.Frame(ventana, bg="black")
frame_configuraciones = tkinter.Frame(ventana, bg="black")
frame_controles = tkinter.Frame(ventana, bg="black")
frame_manual = tkinter.Frame(ventana, bg="black")
frame_puntuaciones = tkinter.Frame(ventana, bg="black")

#  FUNCIONES DE NAVEGACIÓN

def abrir_manual_pdf():
    pdf_path = os.path.join("assets", "manual_matemagia.pdf")
    try:
        os.startfile(pdf_path)  # Windows
        print("Abriendo manual:", pdf_path)
    except Exception as e:
        print("No se pudo abrir el PDF:", e)

def volver_al_menu():
    print("Volviste al menú inicial")
    frame_jugar.pack_forget()
    frame_configuraciones.pack_forget()
    frame_controles.pack_forget()
    frame_manual.pack_forget()
    frame_puntuaciones.pack_forget()
    frame_menu.pack(fill="both", expand=True)


#  BOTONES PRINCIPALES


def accion_jugar():
    """
    Opción A:
    Cerramos la ventana Tkinter y lanzamos tu juego original de Pygame.
    NO se modifica main.py, solo lo llamamos.
    """
    print("Hiciste click en Jugar (Tkinter) -> lanzando main.jugar()")
    ventana.destroy()       # cerramos el menú Tkinter
    main.jugar()            # aquí empieza  juego tal cual en main.py

def accion_configuraciones():
    print("Hiciste click en configuraciones")
    frame_menu.pack_forget()
    frame_configuraciones.pack(fill="both", expand=True)

def accion_controles():
    print("Hiciste click en controles")
    frame_menu.pack_forget()
    frame_controles.pack(fill="both", expand=True)

def accion_manual():
    print("Hiciste click en manual")
    frame_menu.pack_forget()
    frame_manual.pack(fill="both", expand=True)

def accion_puntuaciones():
    print("Hiciste click en puntuaciones")
    frame_menu.pack_forget()
    frame_puntuaciones.pack(fill="both", expand=True)

def accion_salir():
    print("Hiciste click en salir")
    ventana.destroy()
    pygame.quit()
    sys.exit()


#  PANTALLA CONFIGURACIONES


label_titulo_config = tkinter.Label(
    frame_configuraciones,
    text="Configuraciones",
    bg="black",
    fg="white",
    font=("Press Start 2P", 22)
)
label_titulo_config.pack(pady=10)

label_sonido = tkinter.Button(
    frame_configuraciones,
    text="Ajustar sonido",
    bg="#1E0033",
    fg="white",
    activebackground="#3B0066",
    activeforeground="white",
    highlightthickness=2,
    highlightbackground="#FFA800",
    highlightcolor="#FFA800",
    font=("Press Start 2P", 18)
)
label_sonido.pack(pady=10)

label_brillo = tkinter.Button(
    frame_configuraciones,
    text="Ajustar brillo",
    bg="#1E0033",
    fg="white",
    activebackground="#3B0066",
    activeforeground="white",
    highlightthickness=2,
    highlightbackground="#FFA800",
    highlightcolor="#FFA800",
    font=("Press Start 2P", 18)
)
label_brillo.pack(pady=10)

label_idioma = tkinter.Button(
    frame_configuraciones,
    text="Ajustar idioma",
    bg="#1E0033",
    fg="white",
    activebackground="#3B0066",
    activeforeground="white",
    highlightthickness=2,
    highlightbackground="#FFA800",
    highlightcolor="#FFA800",
    font=("Press Start 2P", 18)
)
label_idioma.pack(pady=10)

label_resolucion = tkinter.Button(
    frame_configuraciones,
    text="Ajustar resolución",
    bg="#1E0033",
    fg="white",
    activebackground="#3B0066",
    activeforeground="white",
    highlightthickness=2,
    highlightbackground="#FFA800",
    highlightcolor="#FFA800",
    font=("Press Start 2P", 18)
)
label_resolucion.pack(pady=10)

#  PANTALLA CONTROLES


label_titulo_controles = tkinter.Label(
    frame_controles,
    text="Movimiento WASD",
    bg="black",
    fg="white",
    font=("Press Start 2P", 22)
)
label_titulo_controles.pack(pady=10)


#  PANTALLA MANUAL


label_titulo_manual = tkinter.Label(
    frame_manual,
    text="Manual de juego",
    bg="black",
    fg="white",
    font=("Press Start 2P", 22)
)
label_titulo_manual.pack(pady=10)

boton_abrir_manual_pdf = tkinter.Button(
    frame_manual,
    text="Abrir manual en PDF",
    bg="#1E0033",
    fg="white",
    activebackground="#3B0066",
    activeforeground="white",
    highlightthickness=2,
    highlightbackground="#FFA800",
    highlightcolor="#FFA800",
    font=("Press Start 2P", 18),
    command=abrir_manual_pdf
)
boton_abrir_manual_pdf.pack(pady=10)


#  PANTALLA PUNTUACIONES 

label_titulo_puntuaciones = tkinter.Label(
    frame_puntuaciones,
    text="Ranking puntuaciones",
    bg="black",
    fg="white",
    font=("Press Start 2P", 22)
)
label_titulo_puntuaciones.pack(pady=10)

label_puntuaciones1 = tkinter.Label(
    frame_puntuaciones,
    text="Puntuación top 1 = 1000👑",
    bg="black",
    fg="white",
    font=("Press Start 2P", 18)
)
label_puntuaciones1.pack(pady=10)

label_puntuaciones2 = tkinter.Label(
    frame_puntuaciones,
    text="Puntuación top 2 = 500🥈",
    bg="black",
    fg="white",
    font=("Press Start 2P", 18)
)
label_puntuaciones2.pack(pady=10)

label_puntuaciones3 = tkinter.Label(
    frame_puntuaciones,
    text="Puntuación top 3 = 100🥉",
    bg="black",
    fg="white",
    font=("Press Start 2P", 18)
)
label_puntuaciones3.pack(pady=10)


#  MENÚ PRINCIPAL


etiqueta_titulo = tkinter.Label(
    frame_menu,
    text="Matemagia",
    bg="black",
    fg="white",
    font=("Press Start 2P", 32)
)
etiqueta_titulo.pack(pady=10)

# Imagen
try:
    imagen = Image.open("EL_MATEMAGO.png")
    imagen = imagen.resize((800, 330))
    img_tk = ImageTk.PhotoImage(imagen)
    etiqueta_imagen = tkinter.Label(frame_menu, image=img_tk, bg="black")
    etiqueta_imagen.pack(pady=10)
except Exception as e:
    print("No se pudo cargar la imagen del título:", e)

frame_botones = tkinter.Frame(frame_menu, bg="black")
frame_botones.pack(pady=10)

def crear_boton(texto, accion):
    return tkinter.Button(
        frame_botones,
        text=texto,
        font=("Press Start 2P", 14),
        width=15,
        bg="#1E0033",
        fg="white",
        activebackground="#FFDD33",
        activeforeground="black",
        highlightthickness=3,
        highlightbackground="#FFA800",
        command=accion
    )

crear_boton("Jugar", accion_jugar).pack(pady=2)
crear_boton("Configuraciones", accion_configuraciones).pack(pady=2)
crear_boton("Controles", accion_controles).pack(pady=2)
crear_boton("Manual", accion_manual).pack(pady=2)
crear_boton("Puntuaciones", accion_puntuaciones).pack(pady=2)
crear_boton("Salir", accion_salir).pack(pady=2)

# Botones "Volver al menú" para los otros frames
def crear_boton_volver(frame):
    return tkinter.Button(
        frame,
        text="Volver al menú",
        font=("Press Start 2P", 12),
        bg="#1E0033",
        fg="white",
        activebackground="#FFDD33",
        activeforeground="black",
        highlightbackground="#FFA800",
        highlightthickness=3,
        command=volver_al_menu
    )

crear_boton_volver(frame_jugar).pack()
crear_boton_volver(frame_configuraciones).pack()
crear_boton_volver(frame_controles).pack()
crear_boton_volver(frame_manual).pack()
crear_boton_volver(frame_puntuaciones).pack()

#  MAINLOOP

ventana.mainloop()
