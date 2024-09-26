import tkinter as tk
import random

def encontrar_espacio_vacio(tablero):
    # Encuentra el primer espacio vacío (0) en el tablero
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None, None  # No hay espacios vacíos

def movimiento_valido(tablero, fila, col, num):
    # Verifica si num puede colocarse en la fila
    for x in range(9):
        if tablero[fila][x] == num:
            return False
    # Verifica si num puede colocarse en la columna
    for x in range(9):
        if tablero[x][col] == num:
            return False
    # Verifica si num puede colocarse en la subgrilla 3x3
    fila_inicial, col_inicial = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[i + fila_inicial][j + col_inicial] == num:
                return False
    return True

def impresion(tablero):
    # Imprime el tablero de Sudoku
    for fila in tablero:
        print(fila)

def solucion_BT(tablero):
    # Solución por backtracking
    fila, col = encontrar_espacio_vacio(tablero)
    if fila is None:
        return True
    for num in range(1, 10):
        if movimiento_valido(tablero, fila, col, num):
            tablero[fila][col] = num
            if solucion_BT(tablero):
                return True
            tablero[fila][col] = 0  # Backtracking
    return False

def solucion_BT_FC(tablero):
    # Solución por backtracking con comprobación hacia adelante
    fila, col = encontrar_espacio_vacio(tablero)
    if fila is None:
        return True
    for num in range(1, 10):
        if movimiento_valido(tablero, fila, col, num):
            tablero[fila][col] = num
            if forward_check(tablero, fila, col, num):
                if solucion_BT_FC(tablero):
                    return True
            tablero[fila][col] = 0  # Backtracking
    return False

def forward_check(tablero, fila, col, num):
    # Simula colocar el número y verifica si no rompe las restricciones futuras
    for i in range(9):
        # Verificar si hay conflictos en la fila o la columna
        if (tablero[fila][i] == num and i != col) or (tablero[i][col] == num and i != fila):
            return False

    # Verificar si hay conflictos en la subgrilla 3x3
    fila_inicial, col_inicial = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[fila_inicial + i][col_inicial + j] == num and (fila_inicial + i != fila or col_inicial + j != col):
                return False

    return True  # Si no hay conflictos, la asignación es válida

def solucion_FB(tablero, tablero_original):
    # Solución por fuerza bruta sin retroceso
    while True:
        try:
            for i in range(9):
                for j in range(9):
                    if tablero[i][j] == 0:
                        num = random.randint(1, 9)  # Elige un número aleatorio entre 1 y 9
                        if movimiento_valido(tablero, i, j, num):
                            tablero[i][j] = num  # Coloca el número
                        else:
                            raise ValueError("Tablero inválido, reintentando...")  # Si es inválido, rehace el tablero
            return True  # Si llega aquí, el tablero es válido
        except ValueError:
            # Reinicia todo el tablero si no es válido
            for i in range(9):
                for j in range(9):
                    if tablero[i][j] != tablero_original[i][j]:  # No toca las celdas originales
                        tablero[i][j] = 0
    
    return False  # No se encontró solución

if __name__ == "__main__":
    # Tablero inicial de Sudoku
    tablero_original = [
        [0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]
    ]
    
    # Clonar el tablero original para cada solución
    tablero = [fila[:] for fila in tablero_original]

    # Solución con Backtracking y Comprobación hacia Adelante
    print("\nSolución con Backtracking y Comprobación hacia Adelante:")
    if solucion_BT_FC(tablero):
        impresion(tablero)
    else:
        print("No se encontró solución.")
    
    # Reiniciar el tablero para la siguiente solución
    tablero = [fila[:] for fila in tablero_original]

    # Solución con Backtracking básico
    print("\nSolución con Backtracking:")
    if solucion_BT(tablero):
        impresion(tablero)
    else:
        print("No se encontró solución.")

    # Reiniciar el tablero para la siguiente solución
    tablero = [fila[:] for fila in tablero_original]



        #------------------------------------DIBUJAR TABLERO SOLUCIONADO-------------------------#


def dibujar_tablero(tablero):
    
    # Crear una ventana
    ventana = tk.Tk()
    ventana.title("Sudoku Solucionado")
    
    # Crear un canvas para dibujar el tablero
    canvas = tk.Canvas(ventana, width=450, height=450)
    canvas.pack()

    # Dibujar la cuadrícula
    for i in range(10):  # 9 líneas más 1 al final
        if i % 3 == 0:  # Líneas más gruesas para dividir las subgrillas
            grosor = 3
        else:
            grosor = 1
        canvas.create_line(50 * i, 0, 50 * i, 450, width=grosor)
        canvas.create_line(0, 50 * i, 450, 50 * i, width=grosor)

    # Dibujar los números
    for i in range(9):
        for j in range(9):
            if tablero[i][j] != 0:
                canvas.create_text(25 + 50 * j, 25 + 50 * i, text=str(tablero[i][j]), font=("Arial", 24))

    ventana.mainloop()

# Impresion de tablero de solucion

tablero = [
    [4, 8, 3, 9, 2, 1, 6, 5, 7],
    [9, 6, 7, 3, 4, 5, 8, 2, 1],
    [2, 5, 1, 8, 7, 6, 4, 9, 3],
    [5, 4, 8, 1, 3, 2, 9, 7, 6],
    [7, 2, 9, 5, 6, 4, 1, 3, 8],
    [1, 3, 6, 7, 9, 8, 2, 4, 5],
    [3, 7, 2, 6, 8, 9, 5, 1, 4],
    [8, 1, 4, 2, 5, 3, 7, 6, 9],
    [6, 9, 5, 4, 1, 7, 3, 8, 2]
]

          
dibujar_tablero(tablero)

#---------------- EJECUCION FUERZA BRUTA--------------------#

# Solución por Fuerza Bruta
print("\nSolución por Fuerza Bruta:")
if solucion_FB(tablero, tablero_original):
        impresion(tablero)
else:
        print("No se encontró solución.")





    
