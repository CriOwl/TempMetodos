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

def imprimir_matriz(matriz, nombre="Matriz"):
    print(f"{nombre}:")
    for fila in matriz:
        print([round(x, 4) for x in fila])
    print()

"""
Sistemas de Gauss-Jordan
"""

def resolver_sistema_gauss(A, B):
    n = len(A)
    M = [A[i][:] + B[i][:] for i in range(n)]

    for i in range(n):
        max_fila = i
        for k in range(i + 1, n):
            if abs(M[k][i]) > abs(M[max_fila][i]):
                max_fila = k
        M[i], M[max_fila] = M[max_fila], M[i]

        pivote = M[i][i]
        if abs(pivote) < 1e-10: 
            raise ValueError("El sistema no tiene solucion unica o matriz singular!")
        
        for k in range(i + 1, n):
            factor = M[k][i] / pivote
            for j in range(i, n + 1):
                M[k][j] -= factor * M[i][j]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        suma = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (M[i][n] - suma) / M[i][i]

    return x

"""
Minimos cuadrados
"""

def ajuste_minimos_cuadrados(datos_indices, target):
    X = [] 
    for fila in datos_indices:
        X.append([1.0] + fila) 

    Y = [[val] for val in target]

    print("--- Pasos Intermedios ---")
    Xt = transponer_matriz(X)
    XtX = multiplicar_matrices(Xt, X)
    XtY = multiplicar_matrices(Xt, Y)
    

    print("Resolviendo sistema lineal...")
    beta = resolver_sistema_gauss(XtX, XtY)

    return beta

def estimar(indices_entrada, coeficientes):
    y_estimado = coeficientes[0] 
    for i in range(len(indices_entrada)):
        y_estimado += coeficientes[i+1] * indices_entrada[i]
    return y_estimado

