import numpy as np
import matplotlib.pyplot as plt #biblioteca de los graficos 3d
import graflibNew as gl
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Scrollbar

class Cubo():
    """Modela un cubo genérico"""

    def __init__(self, posicion):
        """Inicializa los atributos del cubo"""
        self.nombre = "cubo"
        self.posicion = posicion
        self.v = np.array([
            [1, 1, 1],
            [-1, 1, 1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, -1],
            [1, -1, -1]
        ])
        self.vertices = [translateP3D(vertice, posicion) for vertice in self.v]
        self.escala = 1.0  #* Agregar una propiedad de escala inicial

        self.triangulos = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [2, 3, 7, 6],
            [1, 2, 6, 5],
            [0, 3, 7, 4]
        ]

def translateP3D(p, pt):
    P = np.array([p[0], p[1], p[2], 1])
    #Matriz de escala
    mT = np.array([
        [1, 0, 0, pt[0]],
        [0, 1, 0, pt[1]],
        [0, 0, 1, pt[2]],
        [0, 0, 0, 1]
    ])
    transformar_vertice = np.matmul(mT, P.transpose())
    return transformar_vertice[:3]  #* Devolver solo las tres primeras coordenadas (x, y, z)

#! función para actualizar la transformación del cubo
cubo2_rotacion = 0
def actualizar_transformacion_cubo(): 
    ax.clear()
    ax.set_box_aspect([1, 1, 1])  # Mantener una relación de aspecto constante
    ax.dist = 7.5  # FOV
    cubo2_rotar_matriz = rotate_around_y(cubo2_rotacion) #matriz de rotacion del eje y
    escala_vertices = [vertice * cubo2.escala for vertice in cubo2.v]  #* Escalar antes de aplicar la rotación pq si no da error
    trans_vertices = [translateP3D(np.matmul(cubo2_rotar_matriz, vertice), traslacion) for vertice in escala_vertices] #*aplicar la rotación a los vértices escalados
    gl.renderObject(trans_vertices, cubo2.triangulos, ax) #*renderizar el objeto con la funcion del maestro
    ax.set_xlim([-10 * zoom, 10 * zoom]) #limite con respecto al zoom
    ax.set_ylim([-10 * zoom, 10 * zoom])
    ax.set_zlim([-10 * zoom, 10 * zoom])
    plt.draw()

def zoom_mouse(event): #! función para hacer zoom con el mouse
    global zoom
    if event.button == 'up':
        zoom += 0.1
    elif event.button == 'down':
        zoom -= 0.1
    actualizar_transformacion_cubo()


def rotar_figura(valor): #! función para manejar el cambio en la barra de rotación
    global cubo2_rotacion
    cubo2_rotacion = rotation_slider.get()
    actualizar_transformacion_cubo()


def escala_cubo(valor): #! función para manejar el cambio en la barra de escala
    global escala
    escala = float(valor)  # Convertir el valor a un número de punto flotante si no da error
    cubo2.escala = escala
    actualizar_transformacion_cubo()


#! estas funciones el manejan cambio en las barras de traslación
traslacion = [0, 0, 0]
def trasladar_x(valor):
    traslacion[0] = x_controlar_traslacion.get() #? actualizar las coordenas de la traslacion del cubo segun este posicionado el scroll
    actualizar_transformacion_cubo()

def trasladar_y(valor):
    traslacion[1] = y_controlar_traslacion.get() 
    actualizar_transformacion_cubo()

def trasladar_z(valor):
    traslacion[2] = z_controlar_traslacion.get()
    actualizar_transformacion_cubo()


#! Función para realizar una rotación alrededor del eje y
def rotate_around_y(angulo):
    cos_a = np.cos(np.radians(angulo)) #* coseno del angulo en radianes
    sin_a = np.sin(np.radians(angulo)) 
    rotacion_matrix = np.array([ #crear matriz alrededor del eje y
        [cos_a, 0, sin_a],
        [0, 1, 0],
        [-sin_a, 0, cos_a]
    ])
    return rotacion_matrix

#* Forma de crear una figura y un eje 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
zoom = 1.0
escala = 1.0

cubo2 = Cubo((-4, 4, 4))
gl.renderObject(cubo2.vertices, cubo2.triangulos, ax)

# crear una ventana de tkinter
ui = tk.Tk()
ui.title("Examen")

# Agregar un lienzo para mostrar la visualización
canvas = FigureCanvasTkAgg(fig, master=ui)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

#! Crear barras de desplazamiento
x_scroll = Scrollbar(ui, orient="horizontal")
x_scroll.pack(side="bottom", fill="x")

y_scroll = Scrollbar(ui, orient="vertical")
y_scroll.pack(side="right", fill="y")

#Iyectar los elementos en la UI
rotation_slider = tk.Scale(ui, from_=0, to=360, label="Rotación", orient="horizontal", command=rotar_figura)
rotation_slider.pack()
rotation_slider.set(0)# valor inicial de la barra de scroll

x_controlar_traslacion = tk.Scale(ui, from_=-10, to=10, label="Traslación X", orient="horizontal", command=trasladar_x)
x_controlar_traslacion.pack()
x_controlar_traslacion.set(0) 

y_controlar_traslacion = tk.Scale(ui, from_=-10, to=10, label="Traslación Y", orient="horizontal", command=trasladar_y)
y_controlar_traslacion.pack()
y_controlar_traslacion.set(0)

z_controlar_traslacion = tk.Scale(ui, from_=-10, to=10, label="Traslación Z", orient="horizontal", command=trasladar_z)
z_controlar_traslacion.pack()
z_controlar_traslacion.set(0)

controlar_escala = tk.Scale(ui, from_=0.1, to=3, label="Escala", orient="horizontal", command=escala_cubo)
controlar_escala.pack()
controlar_escala.set(1.0)

fig.canvas.mpl_connect('scroll_event', zoom_mouse) # *concetar la funcion con el mouse

ui.mainloop() #? mostrar UI