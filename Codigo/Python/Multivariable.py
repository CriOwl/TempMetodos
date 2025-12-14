import math

def transponer_matriz(matriz):
    """
    Docstring for transponer_matriz
    Calcular la matriz transpuesta

    :Parametros matriz (list of list): matriz original de dimensiones m x n

    Retorna: Matriz transpuesta de dimensiones n x m
    """

    filas = len(matriz)
    columnas = len(matriz[0])
    transpuesta = [[0] * filas for _ in range(columnas)]

    for i in range(filas):
        for j in range(columnas):
            transpuesta[j][i] = matriz[i][j]
    return transpuesta

def multiplicar_matrices(matriz_a, matriz_b):
    """
    Realizamos la multiplicacion entre dos matrices que sean compatibles
    
    :param matriz_a: Matriz A de tamano m x n
    :param matriz_b: Matriz B de tamano n x p

    Retorna: Matriz resultante C de tamano m x p

    Devuelve un error si las dinesiones no permiten la multiplicacion
    """

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
    """
    Imprime la matriz
    """

    print(f"{nombre}:")
    for fila in matriz:
        print([round(x, 4) for x in fila])
    print()


"""
Sistemas de Gauss-Jordan
"""
def resolver_sistema_gauss(A, B):
    """
    Docstring for resolver_sistema_gauss
    Resuelve un sitema de ecuaciones lienales usando eliminacion de GAUSS
    El sistema tiene la forma:
    A * x = B

    Retorna: Vector solucion del sistema

    Devuelve un error si el sistema no tiene solucion unica
    """

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
    """
    Docstring for ajuste_minimos_cuadrados
    Calculamos los coeficientes del emodelo lineal mediante minimos cuadrados

    El modelo tiene la forma:
    y = beta_0 + beta_1 * x_1 + beta_2 * x_2 + ... + beta_n * x_n

    Retorna: Vector de coeficientes del modelo
    """
    X = [[1.0] + fila for fila in datos_indices]
    Y = [[val] for val in target]

    print("--- Pasos Intermedios ---")
    Xt = transponer_matriz(X)
    XtX = multiplicar_matrices(Xt, X)
    XtY = multiplicar_matrices(Xt, Y)
    

    print("Resolviendo sistema lineal...")
    beta = resolver_sistema_gauss(XtX, XtY)

    return beta

def estimar(variables, coeficientes):
    """
    Docstring for estimar
    Estimamos el valor de salida para una sola observacion

    :param variables: Valiables independientes
    :param coeficientes: Coeficientes del modelo

    Retorna: Valor estimado
    """
    y_estimado = coeficientes[0]
    for i in range(len(variables)):
        y_estimado += coeficientes[i + 1] * variables[i]
    return y_estimado

def estimar_dataset(datos_indices, coeficientes):
    """
    Docstring for estimar_dataset
    Estimamos los valores de salida para multipes observaciones

    :param datos_indices: Matriz de variables indepedientes
    :param coeficientes: Coeficientes del modelo

    Retorna: lista de valores estimados
    """

    estimaciones = []
    for fila in datos_indices:
        estimaciones.append(estimar(fila, coeficientes))
    return estimaciones


def error_cuadratico_medio(y_real, y_estimado):
    """
    Docstring for error_cuadratico_medio
    Calculamos el error cuadratico Medio del modelo

    :param y_real: Valores reales
    :param y_estimado: Valores estimados

    Retorna: Error cuadratico medio
    """

    n = len(y_real)
    suma = 0.0
    for i in range(n):
        suma =+ (y_real[i] - y_estimado[i]) ** 2
    return suma / n
