import pygame
import random
import os


def limpiar_consola():
    if os.name == 'nt':  # Para sistemas Windows
        os.system('cls')
    else:  # Para sistemas basados en Unix (Linux, macOS, etc.)
        os.system('clear')


# Dimensiones de la ventana
ANCHO_VENTANA = 500
ALTO_VENTANA = 500

# Dimensiones de la matriz
FILAS = 8
COLUMNAS = 8

# Tamaño de cada celda de la matriz
ANCHO_CELDA = ANCHO_VENTANA // COLUMNAS
ALTO_CELDA = ALTO_VENTANA // FILAS

# Colores
COLOR_FONDO = (255, 255, 255)
COLOR_CELDA = (255, 255, 255)
COLOR_BORDE_CELDA = (0, 0, 0)
COLOR_CABALLO_BLANCO = (200, 200, 255)
COLOR_CABALLO_NEGRO = (0, 0, 0)
COLOR_PUNTUACION = (191, 202, 197)
COLOR_RESALTAR = (152, 253, 209)

# Rutas de las imágenes de caballos
RUTA_CABALLO_BLANCO = "caballo_blanco.png"
RUTA_CABALLO_NEGRO = "caballo_negro.png"

#Profundidad del arbol minimax
MAX_PROFUNDIDAD = 3

posiciones_caballo = []
while len(posiciones_caballo) < 2:
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    nueva_posicion = [x, y]

    if nueva_posicion not in posiciones_caballo:
        posiciones_caballo.append(nueva_posicion)

matriz = [[0] * COLUMNAS for _ in range(FILAS)]

puntuaciones = []
while len(puntuaciones) < 8:
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    nueva_posicion = [x, y]

    if nueva_posicion not in puntuaciones and nueva_posicion not in posiciones_caballo:
        puntuaciones.append(nueva_posicion)

for i in range(len(puntuaciones)):
    x = puntuaciones[i][0]
    y = puntuaciones[i][1]
    matriz[y][x] = i

# Clase para representar el tablero del juego
class Tablero:
    def __init__(self):
        # Matriz
        self.matriz = matriz

        # -1 para el caballo blanco, 1 para el caballo negro
        self.turno = -1

        # Puntuaciones
        self.puntuaciones = puntuaciones

        # Posiciones de los caballos
        self.posicion_caballo_blanco = posiciones_caballo[0]
        self.posicion_caballo_negro = posiciones_caballo[1]

        # Puntuación de los caballos
        self.puntuacion_caballo_blanco = 0
        self.puntuacion_caballo_negro = 0

    def dibujar(self, ventana):
        ventana.fill(COLOR_FONDO)

        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                x = columna * ANCHO_CELDA
                y = fila * ALTO_CELDA

                pygame.draw.rect(ventana, COLOR_CELDA, (x, y, ANCHO_CELDA, ALTO_CELDA))
                pygame.draw.rect(ventana, COLOR_BORDE_CELDA, (x, y, ANCHO_CELDA, ALTO_CELDA), 1)

                puntuacion = self.matriz[fila][columna]
                if puntuacion != 0:
                    imagen = pygame.image.load(f"puntuacion_{puntuacion}.png")
                    ventana.blit(imagen, (x, y))

        # Dibujar caballos
        x_blanco = self.posicion_caballo_blanco[0] * ANCHO_CELDA
        y_blanco = self.posicion_caballo_blanco[1] * ALTO_CELDA
        x_negro = self.posicion_caballo_negro[0] * ANCHO_CELDA
        y_negro = self.posicion_caballo_negro[1] * ALTO_CELDA

        pygame.draw.rect(ventana, COLOR_CABALLO_BLANCO, (x_blanco, y_blanco, ANCHO_CELDA, ALTO_CELDA))
        pygame.draw.rect(ventana, COLOR_CABALLO_NEGRO, (x_negro, y_negro, ANCHO_CELDA, ALTO_CELDA))

        pygame.display.update()

    def verificarGanador(self):
        if self.puntuacion_caballo_blanco + self.puntuacion_caballo_negro == len(self.puntuaciones):
            return True
        return False

    def posiciones_disponibles(self):
        posiciones = []

        movimientos = [
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2),
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1)
        ]

        for movimiento in movimientos:
            x = self.posicion_caballo_blanco[0] + movimiento[0]
            y = self.posicion_caballo_blanco[1] + movimiento[1]

            if 0 <= x < COLUMNAS and 0 <= y < FILAS and self.matriz[y][x] == 0:
                posiciones.append((x, y))

        return posiciones

    def mover_caballo(self, columna, fila, posiciones):
        if (columna, fila) in posiciones:
            self.matriz[self.posicion_caballo_blanco[1]][self.posicion_caballo_blanco[0]] = 0
            self.posicion_caballo_blanco = (columna, fila)
            self.puntuacion_caballo_blanco += 1

            # Actualizar puntuaciones
            for puntuacion in self.puntuaciones:
                if puntuacion[0] == columna and puntuacion[1] == fila:
                    self.puntuaciones.remove(puntuacion)
                    break

        # Mover caballo negro
        posiciones_disponibles_negro = self.posiciones_disponibles_negro()
        if len(posiciones_disponibles_negro) > 0:
            self.mover_caballo_negro(posiciones_disponibles_negro)

    def posiciones_disponibles_negro(self):
        posiciones = []

        movimientos = [
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2),
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1)
        ]

        for movimiento in movimientos:
            x = self.posicion_caballo_negro[0] + movimiento[0]
            y = self.posicion_caballo_negro[1] + movimiento[1]

            if 0 <= x < COLUMNAS and 0 <= y < FILAS and self.matriz[y][x] == 0:
                posiciones.append((x, y))

        return posiciones

    def mover_caballo_negro(self, posiciones):
        movimiento = minimax(self, MAX_PROFUNDIDAD)
        self.matriz[self.posicion_caballo_negro[1]][self.posicion_caballo_negro[0]] = 0
        self.posicion_caballo_negro = movimiento
        self.puntuacion_caballo_negro += 1

        # Actualizar puntuaciones
        for puntuacion in self.puntuaciones:
            if puntuacion[0] == movimiento[0] and puntuacion[1] == movimiento[1]:
                self.puntuaciones.remove(puntuacion)
                break


def minimax(tablero, profundidad):
    if profundidad == 0 or tablero.verificarGanador():
        return tablero.posicion_caballo_negro

    mejor_movimiento = None
    mejor_puntuacion = float('-inf') if tablero.turno == -1 else float('inf')

    posiciones_disponibles_negro = tablero.posiciones_disponibles_negro()
    for movimiento in posiciones_disponibles_negro:
        copia_tablero = Tablero()  # Crear una copia del tablero original
        copia_tablero.matriz = tablero.matriz
        copia_tablero.puntuaciones = tablero.puntuaciones
        copia_tablero.posicion_caballo_blanco = tablero.posicion_caballo_blanco
        copia_tablero.posicion_caballo_negro = tablero.posicion_caballo_negro
        copia_tablero.puntuacion_caballo_blanco = tablero.puntuacion_caballo_blanco
        copia_tablero.puntuacion_caballo_negro = tablero.puntuacion_caballo_negro

        copia_tablero.matriz[movimiento[1]][movimiento[0]] = 1
        copia_tablero.posicion_caballo_negro = movimiento
        copia_tablero.puntuacion_caballo_negro += 1

        # Cambiar turno
        copia_tablero.turno *= -1

        puntuacion = minimax(copia_tablero, profundidad - 1)

        if tablero.turno == -1:  # Maximizar
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_movimiento = movimiento
        else:  # Minimizar
            if puntuacion < mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_movimiento = movimiento

    return mejor_movimiento


# Crear instancia del tablero
tablero = Tablero()

# Inicializar Pygame
pygame.init()

# Crear ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Nombre de la ventana
pygame.display.set_caption("Smart Horses")

# Bucle principal del juego
while not tablero.verificarGanador():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Dibujar tablero
    tablero.dibujar(ventana)

    # Realizar movimiento
    posiciones_disponibles = tablero.posiciones_disponibles()
    if len(posiciones_disponibles) > 0:
        tablero.mover_caballo(random.choice(posiciones_disponibles))

    # Actualizar ventana
    pygame.display.update()

pygame.quit()
