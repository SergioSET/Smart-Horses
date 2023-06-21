import os
import sys
import time
from main import *
import easygui as eg
from copy import deepcopy
from graphviz import Digraph
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


if __name__ == '__main__':
    main()


def costoUniforme(matriz):
    # matriz = [[1, 1, 1, 1],
    #           [1, 1, 1, 2],
    #           [0, 6, 1, 0],
    #           [0, 0, 0, 0],
    #           [1, 1, 1, 6]]

    colores = ['white', 'brown', 'orange', 'purple', 'green', 'blue', 'yellow']
    cmap = ListedColormap(colores)

    nodosExpandidos = 0
    profundidadArbol = 0
    costo = 0
    arrayExpansion = []
    timeInitial = time.time()

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 2:
                positionGoku = [i, j]

    class Nodo:
        def __init__(self, costo, profundidad, padre, posicion_y, posicion_x, hijos, matriz, semillas, esferas, ultimaPelea):
            self.costo = costo
            self.profundidad = profundidad
            self.expandido = False
            self.padre = padre
            self.posicion_y = posicion_y
            self.posicion_x = posicion_x
            self.hijos = hijos
            self.matriz = matriz
            self.semillas = semillas
            self.esferas = esferas
            self.ultimaPelea = ultimaPelea
            self.solucion = False
            self.devolver = False

        def expandir(self, arrayExpansion):
            self.expandido = True

            moves = [
            # Movimiento hacia arriba-derecha
           (self.posicion_y - 2, self.posicion_x + 1),
            # Movimiento hacia arriba-derecha
             (self.posicion_y - 1, self.posicion_x + 2),
            # Movimiento hacia abajo-derecha
             (self.posicion_y + 1, self.posicion_x + 2),
            # Movimiento hacia abajo-derecha
            (self.posicion_y + 2, self.posicion_x + 1),
            # Movimiento hacia abajo-izquierda
            (self.posicion_y + 2, self.posicion_x - 1),
            # Movimiento hacia abajo-izquierda
            (self.posicion_y + 1, self.posicion_x - 2),
            # Movimiento hacia arriba-izquierda
            (self.posicion_y - 1, self.posicion_x - 2),
            # Movimiento hacia arriba-izquierda
            (self.posicion_y - 2, self.posicion_x - 1)
        ]

            for move in moves:
              y, x = move
              if 0 <= y < len(self.matriz) and 0 <= x < len(self.matriz[self.posicion_y]):
               if self.matriz[y][x] != 1:
                self.crearHijo(y, x, arrayExpansion)

        def crearHijo(self, posicionAMover_y, posicionAMover_x, arrayExpansion):
            matrizNueva = deepcopy(self.matriz)
            costo = 1
            semillas = 0
            esferas = 0
            ultimaPelea = 0

            matrizNueva[self.posicion_y][self.posicion_x] = 0

            if self.matriz[posicionAMover_y][posicionAMover_x] == 3:
                if self.semillas == 0:
                    costo = 4
                    ultimaPelea = 3
                else:
                    semillas -= 1
            elif self.matriz[posicionAMover_y][posicionAMover_x] == 4:
                if self.semillas == 0:
                    costo = 7
                    ultimaPelea = 4
                else:
                    semillas -= 1
            elif self.matriz[posicionAMover_y][posicionAMover_x] == 5:
                semillas += 1
                self.devolver = True
            elif matrizNueva[posicionAMover_y][posicionAMover_x] == 6:
                esferas += 1
                self.devolver = True

            if self.ultimaPelea == 3:
                matrizNueva[self.posicion_y][self.posicion_x] = 3
            elif self.ultimaPelea == 4:
                matrizNueva[self.posicion_y][self.posicion_x] = 4

            matrizNueva[posicionAMover_y][posicionAMover_x] = 2

            nuevohijo = Nodo(self.costo+costo, self.profundidad+1, self, posicionAMover_y, posicionAMover_x,
                             [], matrizNueva, self.semillas+semillas, self.esferas+esferas, ultimaPelea)

            if self.padre == None:
                arrayExpansion.append(nuevohijo)
                self.hijos.append(nuevohijo)
            else:
                if self.padre.devolver == True:
                    arrayExpansion.append(nuevohijo)
                    self.hijos.append(nuevohijo)
                elif nuevohijo.seDevuelve(self.padre) == False:
                    arrayExpansion.append(nuevohijo)
                    self.hijos.append(nuevohijo)

        def seDevuelve(hijo, padre):
            if hijo.posicion_x == padre.posicion_x and hijo.posicion_y == padre.posicion_y:
                return True
            else:
                return False

        def imprimirMatriz(self):
            for i in range(len(self.matriz)):
                for j in range(len(self.matriz[i])):
                    print(self.matriz[i][j], end=' ')
                print()
            print()

        def encontrarAncestros(self):
            ancestros = []
            ancestros.append(self)
            ancestro = self.padre
            while ancestro != None:
                ancestros.append(ancestro)
                ancestro = ancestro.padre
            ancestros.reverse()
            return ancestros

        def generarposicion(self):
            return str(self.posicion_y) + " , " + str(self.posicion_x)

        def nodosExpandidos(self):
            nodos = 0
            if self.expandido == True:
                nodos += 1
                for i in self.hijos:
                    nodos += i.nodosExpandidos()
            return nodos

        def profundidadArbol(self):
            profundidad = self.profundidad
            for i in self.hijos:
                profundidad = max(profundidad, i.profundidadArbol())
            return profundidad

        def generarMatrizString(self):
            matrizString = ""
            for i in range(len(self.matriz)):
                for j in range(len(self.matriz[i])):
                    matrizString += str(self.matriz[i][j])
                matrizString += "\n"
            return matrizString

    raiz = Nodo(0, 0, None, positionGoku[0],
                positionGoku[1], [], matriz, 0, 0, 0)

    arrayExpansion.append(raiz)

    nodoMaestro = None

    achi=2
    while len(arrayExpansion) != 0:
        arrayExpansion.sort(key=lambda x: x.costo)
        if achi==0:
            
            nodoMaestro = arrayExpansion[0]
            nodoMaestro.solucion = True
            nodoMaestro.expandido = True
            break
        else:
            arrayExpansion[0].expandir(arrayExpansion)
            arrayExpansion.pop(0)
        achi=achi-1
            

    if not nodoMaestro:
        eg.msgbox(msg="No se encontró una solución con el siguiente input",
                  title="Resultado", image="images/mallaGokuSmart.png")
    else:
        camino = nodoMaestro.encontrarAncestros()
        nodosExpandidos = raiz.nodosExpandidos()
        profundidadArbol = raiz.profundidadArbol()
        costo = nodoMaestro.costo

        # Se imprime el camino con valores de profundidad y costo
        # for i in camino:
        #     i.imprimirMatriz()
        #     print("costo: ", i.costo, "profundidad: ", i.profundidad)
        #     print()

        # Generación de grafos
        def generar_grafo_1(nodo, grafo):
            temp = "Matriz:\n"+nodo.generarMatrizString()+"\nCon valor: " + \
                str(nodo.costo) + "\nExpandido: "+str(nodo.expandido)
            grafo.node(str(id(nodo)), label=temp)
            for hijo in nodo.hijos:
                grafo.edge(str(id(nodo)), str(id(hijo)))
                generar_grafo_1(hijo, grafo)
        grafo1 = Digraph()
        generar_grafo_1(raiz, grafo1)
        grafo1.render('grafo', view=True)

        # Impresión de resultados
        timeFinal = time.time()
        timeComputing = timeFinal - timeInitial
        eg.msgbox(msg="Se encontró una solución con los siguientes datos:\n\nNodos expandidos: " + str(nodosExpandidos) + "\nProfundidad del árbol: " +
                  str(profundidadArbol) + "\nCosto de la solución: " + str(costo) + "\nTiempo de ejecución: " + str(timeComputing)[:10] + " segundos\n\nAhora se visualizará el camino que tomaría Goku", title="Resultado")
