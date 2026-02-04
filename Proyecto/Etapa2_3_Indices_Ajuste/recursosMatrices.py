
def transponer_matriz(matriz):
    """transponer_matriz
    Matriz transpuesta de matriz
    Cambia filas por columnas
    Args:
        matriz (list): matriz a ser transpuesta

    Returns:
        transpuesta: matriz transpuesta
    """
    filas = len(matriz)
    columnas = len(matriz[0])
    transpuesta = [[0] * filas for _ in range(columnas)]

    for i in range(filas):
        for j in range(columnas):
            transpuesta[j][i] = matriz[i][j]
    return transpuesta


def multiplicar_matrices(matriz_a, matriz_b):
    """multiplicar_matrices
    Multiplica dos matrices A y B
    
    Args:
        matriz (list): matriz A
        matriz (list): matriz B

    Returns:
        matrizResultante: matriz resultante de la multiplicacion de A y B 
        o una matriz vacia si no son compatibles
    """
    filas_A = len(matriz_a)
    cols_A = len(matriz_a[0])
    filas_B = len(matriz_b)
    cols_B = len(matriz_b[0])

    if cols_A != filas_B:
        print("Matrices no compatibles para multiplicar")
        return[[]];

    matrizResultante = [[0] * cols_B for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(cols_B):
            suma = 0
            for k in range(cols_A):
                suma += matriz_a[i][k] * matriz_b[k][j]
            matrizResultante[i][j] = suma
    return matrizResultante


def imprimir_matriz(matriz, nombre="Matriz"):
    """imprimir_matriz
    Imprime una matriz
    
    Args:
        matriz (list): matriz A
    """
    print(f"{nombre}:")
    for fila in matriz:
        print([round(x, 4) for x in fila])
    print()

def resolver_sistema_gauss(matrizA, matrizB):
    """resolver_sistema_gauss
    Resuelve un sistema de ecuaciones lineales por eliminacion de Gauss
        
    Args:
        matrizA (list): matriz de coeficientes
        matrizB (list): matriz de valores independientes
    Returns:
        x (list): lista con las incognitas
    """
    n = len(matrizA)
    # Crear la matriz aumentada copiando los valores
    matrizAumentada = [matrizA[i][:] + matrizB[i][:] for i in range(n)]
    for i in range(n):
        max_fila = i
        for k in range(i + 1, n):
            if abs(matrizAumentada[k][i]) > abs(matrizAumentada[max_fila][i]):
                max_fila = k
        matrizAumentada[i], matrizAumentada[max_fila] = matrizAumentada[max_fila], matrizAumentada[i]

        pivote = matrizAumentada[i][i]
        if abs(pivote) < 1e-10:
            raise ValueError("El sistema no tiene solucion unica o matriz singular!")

        for k in range(i + 1, n):
            factor = matrizAumentada[k][i] / pivote
            for j in range(i, n + 1):
                matrizAumentada[k][j] -= factor * matrizAumentada[i][j]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        suma = sum(matrizAumentada[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (matrizAumentada[i][n] - suma) / matrizAumentada[i][i]
    return x