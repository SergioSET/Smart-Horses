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
COLOR_RESALTAR = (128, 128, 128)

# Rutas de las imágenes de caballos
RUTA_CABALLO_BLANCO = "caballo_blanco.png"
RUTA_CABALLO_NEGRO = "caballo_negro.png"

posiciones_caballo = []
while len(posiciones_caballo) < 2:
    x = random.randint(0,7)
    y = random.randint(0,7)
    nueva_posicion = [x, y]

    if nueva_posicion not in posiciones_caballo:
        posiciones_caballo.append(nueva_posicion)

matriz = [[0] * COLUMNAS for _ in range(FILAS)]

puntuaciones = []
while len(puntuaciones) < 8:
    x = random.randint(0,7)
    y = random.randint(0,7)
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

        # Atributos caballo blanco
        self.caballo_blanco_x = posiciones_caballo[0][0]
        self.caballo_blanco_y = posiciones_caballo[0][1]
        self.puntuacion_caballo_blanco = 0
        self.imagen_caballo_blanco = pygame.image.load(RUTA_CABALLO_BLANCO)

        # Atributos caballo negro
        self.caballo_negro_x = posiciones_caballo[1][0]
        self.caballo_negro_y = posiciones_caballo[1][1]
        self.puntuacion_caballo_negro = 0
        self.imagen_caballo_negro = pygame.image.load(RUTA_CABALLO_NEGRO)


    def dibujar(self, ventana, resaltar):
        ventana.fill(COLOR_FONDO)
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                # Celda con borde de color negro
                if (resaltar.__contains__([fila, columna])):
                    pygame.draw.rect(ventana, COLOR_RESALTAR, (columna * ANCHO_CELDA, fila * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))
                    pygame.draw.rect(ventana, COLOR_BORDE_CELDA, (columna * ANCHO_CELDA, fila * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA), 1)
                else: 
                    pygame.draw.rect(ventana, COLOR_CELDA, (columna * ANCHO_CELDA, fila * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))
                    pygame.draw.rect(ventana, COLOR_BORDE_CELDA, (columna * ANCHO_CELDA, fila * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA), 1)

                if (self.matriz[fila][columna] > 0):
                    valor = self.matriz[fila][columna]
                    fuente = pygame.font.Font(None, 20)
                    texto = fuente.render(str(valor), True, COLOR_BORDE_CELDA)
                    ventana.blit(texto, (columna * ANCHO_CELDA + 5, fila * ALTO_CELDA + 5))

                # Dibujar caballo blanco
                if fila == self.caballo_blanco_y and columna == self.caballo_blanco_x:
                    # pygame.draw.circle(ventana, COLOR_CABALLO_BLANCO, (columna * ANCHO_CELDA + ANCHO_CELDA // 2, fila * ALTO_CELDA + ALTO_CELDA // 2), min(ANCHO_CELDA, ALTO_CELDA) // 2)
                    ventana.blit(self.imagen_caballo_blanco, (columna * ANCHO_CELDA, fila * ALTO_CELDA))
                

                # Dibujar caballo negro
                if fila == self.caballo_negro_y and columna == self.caballo_negro_x:
                    #pygame.draw.circle(ventana, COLOR_CABALLO_NEGRO, (columna * ANCHO_CELDA + ANCHO_CELDA // 2, fila * ALTO_CELDA + ALTO_CELDA // 2), min(ANCHO_CELDA, ALTO_CELDA) // 2)
                    ventana.blit(self.imagen_caballo_negro, (columna * ANCHO_CELDA, fila * ALTO_CELDA))


    def posiciones_disponibles(self):
        posiciones = []
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                if self.turno == -1:
                    if ((fila == self.caballo_blanco_y + 2 or fila == self.caballo_blanco_y - 2) and (columna == self.caballo_blanco_x + 1 or columna == self.caballo_blanco_x - 1)):
                        posiciones.append([fila,columna])
                        
                    if ((fila == self.caballo_blanco_y + 1 or fila == self.caballo_blanco_y - 1) and (columna == self.caballo_blanco_x + 2 or columna == self.caballo_blanco_x - 2)):
                        posiciones.append([fila,columna])

                    if (posiciones.__contains__([self.caballo_negro_y, self.caballo_negro_x])):
                        posiciones.remove([self.caballo_negro_y, self.caballo_negro_x])

                else:
                    if ((fila == self.caballo_negro_y + 2 or fila == self.caballo_negro_y - 2) and (columna == self.caballo_negro_x + 1 or columna == self.caballo_negro_x - 1)):
                        posiciones.append([fila,columna])
                        
                    if ((fila == self.caballo_negro_y + 1 or fila == self.caballo_negro_y - 1) and (columna == self.caballo_negro_x + 2 or columna == self.caballo_negro_x - 2)):
                        posiciones.append([fila,columna])

                    if (posiciones.__contains__([self.caballo_blanco_y, self.caballo_blanco_x])):
                        posiciones.remove([self.caballo_blanco_y, self.caballo_blanco_x])

        return posiciones


    def mover_caballo(self, x, y, posiciones):
        valor = self.matriz[y][x]
        if posiciones.__contains__([y, x]):
            if self.turno == -1:
                self.caballo_blanco_x = x
                self.caballo_blanco_y = y
                self.puntuacion_caballo_blanco += valor
            else:
                self.caballo_negro_x = x
                self.caballo_negro_y = y
                self.puntuacion_caballo_negro += valor
                
            self.matriz[y][x] = 0
            self.turno *= -1

        print("Puntuación caballo blanco: " + str(self.puntuacion_caballo_blanco))
        print("Puntuación caballo negro: " + str(self.puntuacion_caballo_negro))

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego del Caballo")

# Crear el tablero
tablero = Tablero()

# Bucle principal del juego
while True:       
    posiciones = tablero.posiciones_disponibles()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            fila = y // ALTO_CELDA
            columna = x // ANCHO_CELDA

            tablero.mover_caballo(columna, fila, posiciones)
    
    tablero.dibujar(ventana, posiciones)
    pygame.display.flip()
 