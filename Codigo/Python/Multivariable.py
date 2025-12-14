import math

def transponer_matriz(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    transpuesta = [[0] * filas for _ in range(columnas)]

    for i in range(filas):
        for j in range(columnas):
            transpuesta[j][i] = matriz[i][j]
    return transpuesta

def multiplicar_matrices(matriz_a, matriz_b):
    filas_A = len(matriz_a)
    cols_A = len(matriz_a[0])
    filas_B = len(matriz_b)
    cols_B = len(matriz_b[0])

    if cols_A != filas_B:
        raise ValueError("Dimensiones incompatibles para multiplicar!!")
    
    C = [[0] * cols_B for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(cols_B):
            suma = 0
            for k in range(cols_A):
                suma += matriz_a[i][k] * matriz_b[k][j]
            C[i][j] = suma
    return C