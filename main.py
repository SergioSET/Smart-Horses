import pygame
import random

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

# Clase para representar el tablero del juego
class Tablero:
    def __init__(self):
        self.matriz = [[0] * COLUMNAS for _ in range(FILAS)]
        self.caballo_blanco_x = random.randint(0, COLUMNAS - 1)
        self.caballo_blanco_y = random.randint(0, FILAS - 1)

        self.caballo_negro_x = random.randint(0, COLUMNAS - 1)
        self.caballo_negro_y = random.randint(0, FILAS - 1)

    def dibujar(self, ventana):
        ventana.fill(COLOR_FONDO)
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                # Celda con borde de color negro
                pygame.draw.rect(ventana, COLOR_CELDA, (columna * ANCHO_CELDA, fila * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))
                pygame.draw.rect(ventana, COLOR_BORDE_CELDA, (columna * ANCHO_CELDA, fila * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA), 1)

                # Dibujar caballos
                if fila == self.caballo_blanco_y and columna == self.caballo_blanco_x:
                    pygame.draw.circle(ventana, COLOR_CABALLO_BLANCO, (columna * ANCHO_CELDA + ANCHO_CELDA // 2, fila * ALTO_CELDA + ALTO_CELDA // 2), min(ANCHO_CELDA, ALTO_CELDA) // 2)
                if fila == self.caballo_negro_y and columna == self.caballo_negro_x:
                    pygame.draw.circle(ventana, COLOR_CABALLO_NEGRO, (columna * ANCHO_CELDA + ANCHO_CELDA // 2, fila * ALTO_CELDA + ALTO_CELDA // 2), min(ANCHO_CELDA, ALTO_CELDA) // 2)


    def mover_caballo(self, x, y, turno):
        if 0 <= x < COLUMNAS and 0 <= y < FILAS:
            if turno == -1:
                self.caballo_blanco_x = x
                self.caballo_blanco_y = y
            else:
                self.caballo_negro_x = x
                self.caballo_negro_y = y
                

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego del Caballo")

# Crear el tablero
tablero = Tablero()
turno = -1

# Bucle principal del juego
while True:
    # -1 para el caballo blanco, 1 para el caballo negro
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            fila = y // ALTO_CELDA
            columna = x // ANCHO_CELDA
            tablero.mover_caballo(columna, fila, turno)
            turno *= -1

    tablero.dibujar(ventana)
    pygame.display.flip()
 