import csv
import  math
import  numpy  as  np
import Multivariable as mv

filtradoFile = "../../processed_data.csv"
NormalizadoFile = "../../normal_Data.csv"
maxValores=list()
minValores=list()
valoresColumnas=list()

def normalizar(x, xmax, xmin):
    """
    Docstring for normalizar
    Aplicamos normalizacion Min-Max a un valor escalar

    :param x: valor original
    :param xmax: Valor maximo de la columna
    :param xmin: Valor minimo de la columna
    """
    if xmax == xmin:
        return 0.0
    return (x - xmin) / (xmax - xmin)


def normalizarArchivo():
    """
    Docstring for normalizarArchivo
    Normalizamos todas las columnas de un archivo CSV utilizando
    el metodo Min-Max y guardamos el resultado en otro archivo CSV

    El procedimiento se divide en dos fases:
    1. Calculo de valores maximos y minimos por columna
    2. Generacion del archivo normalizado
    """
    global maxValores
    global minValores
    global filtradoFile
    global NormalizadoFile
    with open(filtradoFile,"r") as f:
        reader = csv.reader(f)
        encabezado = next(reader)
        num_cols = len(encabezado)
        maxValores = [-1] * num_cols
        minValores = [ -1] * num_cols
        for fila in reader:
            for i in range(num_cols):
                valor = float(fila[i])
                if valor> maxValores[i] or maxValores[i]==-1:
                    maxValores[i] = valor
                if valor < minValores[i] or minValores[i]==-1:
                    minValores[i] = valor
    with open(filtradoFile, newline="") as f_in, \
            open(NormalizadoFile, "w", newline="") as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        encabezado = next(reader)
        writer.writerow(encabezado)
        for fila in reader:
            salida = []
            for i in range(num_cols):
                v = float(fila[i])
                salida.append(normalizar(v, maxValores[i], minValores[i]))
            writer.writerow(salida)

def agregarVColumnas():
    global valoresColumnas
    with open(NormalizadoFile, newline="") as f_in:
        reader = csv.reader(f_in)
        encabezado = next(reader)
        # Referencias de listas a una misma aaaaaaaaaaaaaaaaaaaaaaaaaaaaa py
        valoresColumnas = [[] for _ in range(len(encabezado))]
        for fila in reader:
            for i,valor in enumerate(fila):
                valoresColumnas[i].append(float(valor))
#normalizarArchivo()
agregarVColumnas()

def pearson(x, y):
    """
    Pearson

    :param x: Vector para la variable del dataset
    :param y: Vector correspondiente a la variable objetivo (target)
    :return: Coeficiente de correlación de Pearson entre x e y
    """
    # Conversión a arrays de numpy (para tener compatiblidad con numpy)
    x = np.asarray(x)
    y = np.asarray(y)
    n = len(x)
    # Calculo de la medias
    media_x = np.mean(x)
    media_y = np.mean(y)
    # Inicializar las sumatorias
    sum_xy = 0.0
    sum_x2 = 0.0
    sum_y2 = 0.0


# PCA
def PCA(matriz):
    # Transponemos para que las filas sean pacientes y columnas variables
    X = np.array(matriz).T

    media_X = np.mean(X, axis=0)
    X_centrado = X - media_X

    # Para la matriz de covarianza
    covarianza = np.dot(X_centrado.T, X_centrado) / (X.shape[0] - 1)

    autovalores, autovectores = np.linalg.eig(covarianza)

    # Ordenar autovalores y autovectores de mayor a menor
    idx = np.argsort(autovalores)[::-1]
    autovalores = autovalores[idx]
    autovectores = autovectores[:, idx]

    # Tomamos el primer componente principal (pesos)
    pesos_pca = autovectores[:, 0]

    # --- MODIFICACIÓN 1: Corrección de Signos ---
    # Si la suma de los pesos es negativa, invertimos el vector.
    # Esto asegura que un valor alto en las variables signifique un índice alto,
    # evitando que el índice salga invertido (ej. -0.7).
    if np.sum(pesos_pca) < 0:
        pesos_pca = -1 * pesos_pca

    # Proyección (Cálculo del índice crudo)
    indice_pca = np.dot(X_centrado, pesos_pca)

    # --- MODIFICACIÓN 2: Normalización Min-Max [0, 1] ---
    # Es obligatorio escalar el resultado entre 0 y 1 para que este índice
    # tenga el mismo peso que los demás (A, B, C, D) en la etapa de Mínimos Cuadrados.
    min_val = np.min(indice_pca)
    max_val = np.max(indice_pca)

    if max_val - min_val != 0:
        indice_pca = (indice_pca - min_val) / (max_val - min_val)
    else:
        # Caso borde: si todas las variables son iguales (varianza 0)
        indice_pca = np.zeros_like(indice_pca)
    print(pesos_pca)
    return indice_pca


# --- FUNCIONES AUXILIARES (Sin cambios, solo eliminada la duplicada) ---

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
    # Crear la matriz aumentada copiando los valores
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


target = valoresColumnas[0]

indice_pcaColor = PCA(valoresColumnas[4:6])
print("Color")
indice_pcaAsimetria = PCA(valoresColumnas[8:])
print("Asimetria")
#1///6
matrizTemp2=[]
matrizTemp2.append(valoresColumnas[1])
matrizTemp2.append(valoresColumnas[6])
indice_pcaDiametro = PCA(matrizTemp2)
print("Diametro")
# 2 -3 -6
matrizTemp=[]
matrizTemp.append(valoresColumnas[2])
matrizTemp.append(valoresColumnas[3])
matrizTemp.append(valoresColumnas[7])
indice_pcaBordes = PCA(matrizTemp)
print("Bordes")
matrizTemp=[indice_pcaBordes,indice_pcaAsimetria,indice_pcaDiametro,indice_pcaColor]

# Investigar otra forma de obtener mejores valores de indice
print(mv.ajuste_minimos_cuadrados(matrizTemp, target))

# Multivariable
#coeficientes = ajuste_minimos_cuadrados(datos_indices, target)
print("Coeficientes del modelo de minimos cuadrados:")
#print(coeficientes)




