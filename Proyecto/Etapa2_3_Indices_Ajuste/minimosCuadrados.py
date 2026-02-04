import math
from . import recursosMatrices as rm

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

    Xt = rm.transponer_matriz(X)
    XtX = rm.multiplicar_matrices(Xt, X)
    XtY = rm.multiplicar_matrices(Xt, Y)
    

    beta = rm.resolver_sistema_gauss(XtX, XtY)

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

