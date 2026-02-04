import numpy as np
import math
import coeficientePearson as cp

def normalizar(valor, valorMax, valorMin):
    """
    Normalizar
    Se aplica la normalizacion Min-Max a un valor
    Args:
    valor (float): valor original
    valorMax (float): Valor maximo de la columna
    valorMin (float): Valor minimo de la columna
    """
    if valorMax == valorMin:
        return 0.0
    return (valor - valorMin) / (valorMax - valorMin)


def PCA(matriz):
    """PCA
    Realiza una reducion de dimensionalidad mediante el analisis de componentes principales (PCA)
    
    Args:
        matriz (list): es una matriz de datos donde cada fila tiene todos los valores de una varaible seleccionada

    Returns:
        min_val float: Valor minimo del PCA
        max_val float: Valor maximo del PCA
        pesosPCA list: Lista con los pesos PCA de cada variable
        indicesPCA list: Lista con los indices PCA calculados para cada fila
    """
    X = np.array(matriz).T
    media_X = np.mean(X, axis=0)
    X_centrado = X - media_X
    
    covarianza = np.dot(X_centrado.T, X_centrado) / (X.shape[0] - 1) 
    autovalores, autovectores = np.linalg.eig(covarianza)
    # Ordenar autovalores y autovectores de mayor a menor
    idx = np.argsort(autovalores)[::-1]
    autovalores = autovalores[idx]
    autovectores = autovectores[:, idx]
    pesos_pca = autovectores[:, 0]
    # Pesos positivos para cada indice de riesgo
    if np.sum(pesos_pca) < 0:
        pesos_pca = -1 * pesos_pca
    indice_pca = np.dot(X_centrado, pesos_pca)
    #Normalizacion por min-max
    min_val = np.min(indice_pca)
    max_val = np.max(indice_pca)
    indice_pca=normalizar(indice_pca, max_val, min_val)
    
    return min_val,max_val,pesos_pca,indice_pca



# Resultados:
#Indice del analisis de componentes principales PCA
#Asimetria: [0.59784655 0.737643   0.31531107 ... 0.22783228 0.79371181 0.25630703] [0.01062763 0.99994353]
#Variables usadas en Asimetria: ['tbp_lv_symm_2axis', 'tbp_lv_symm_2axis_angle']
#Borde: [0.41798844 0.13770192 0.42421557 ... 0.08080684 0.08205462 0.12921331] [0.01624593 0.11511295 0.99321955]
#Variables usadas en Borde: tbp_lv_areaMM2tbp_lv_perimeterMMtbp_lv_norm_border
#Color: [0.08285664 0.11406985 0.13636662 ... 0.14950765 0.21177612 0.28167881] []
#Variables usadas en Color: ['target', 'clin_size_long_diam_mm', 'tbp_lv_areaMM2', 'tbp_lv_perimeterMM', 'tbp_lv_color_std_mean', 'tbp_lv_deltaLBnorm', 'tbp_lv_minorAxisMM', 'tbp_lv_norm_border', 'tbp_lv_symm_2axis', 'tbp_lv_symm_2axis_angle']
#Diametro: [0.06736218 0.09999965 0.09659171 ... 0.05409235 0.09425056 0.10428924] [0.70062684 0.71352788]
#Variables usadas en Diametro: ['clin_size_long_diam_mm', 'tbp_lv_minorAxisMM']