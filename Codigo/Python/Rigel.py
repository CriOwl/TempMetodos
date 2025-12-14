import csv
import  math
import  numpy  as  np
filtradoFile = "../../processed_data.csv"
NormalizadoFile = "../../normal_Data.csv"
maxValores=list()
minValores=list()
valoresColumnas=list()
def normalizar(x, xmax, xmin):
    if xmax == xmin:
        return 0.0
    return (x - xmin) / (xmax - xmin)

def normalizarArchivo():
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
normalizarArchivo()
agregarVColumnas()


# PCA

def PCA(matriz):

    X = np.array(matriz).T

    media_X = np.mean(X, axis=0)
    X_centrado = X - media_X

    #Para la matriz de covarianza

    covarianza = np.dot(X_centrado.T, X_centrado) / (X.shape[0] - 1)

    autovalores, autovectores = np.linalg.eig(covarianza)

    idx = np.argsort(autovalores)[::-1]
    autovalores = autovalores[idx]
    autovectores = autovectores[:, idx]

    pesos_pca = autovectores[:, 0]

    indice_pca = np.dot(X_centrado, pesos_pca)

    return indice_pca

# MINIMOS CUADRADOS


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
# Comparar eficiencia de metodos
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


target = valoresColumnas[0]

indice_pcaColor = PCA(valoresColumnas[4:6])
print(indice_pcaColor,"Color")
indice_pcaAsimetria = PCA(valoresColumnas[8:])
print(indice_pcaAsimetria,"Asimetria")
#1///6
matrizTemp2=[]
matrizTemp2.append(valoresColumnas[1])
matrizTemp2.append(valoresColumnas[6])
indice_pcaDiametro = PCA(matrizTemp2)
print(indice_pcaDiametro,"Diametro")
# 2 -3 -6
matrizTemp=[]
matrizTemp.append(valoresColumnas[2])
matrizTemp.append(valoresColumnas[3])
matrizTemp.append(valoresColumnas[7])
indice_pcaBordes = PCA(matrizTemp)
print(indice_pcaBordes,"Bordes")

# Investigar otra forma de obtener mejores valores de indice

# Multivariable
#coeficientes = ajuste_minimos_cuadrados(datos_indices, target)
print("Coeficientes del modelo de minimos cuadrados:")
#print(coeficientes)




