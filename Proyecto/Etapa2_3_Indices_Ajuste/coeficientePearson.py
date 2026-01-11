import numpy as np
import math
import csv

def obtenerColunmas(archivo):
    """ObtenerColunmas
    Lee un archivo y devuelve la informacion de sus columnas en listas de listas

    Args:
        archivo (str): path del archivo CSV
    Returns:
        valoresColumnas(list): Listado de listas, cada lista contiene los valores de una columna
    """
    valoresColumnas=list()
    with open(archivo, newline="") as f_in:
        reader = csv.reader(f_in)
        encabezado = next(reader)
        valoresColumnas = [[] for _ in range(len(encabezado))]
        for fila in reader:
            for i,valor in enumerate(fila):
                valoresColumnas[i].append(float(valor))
    return valoresColumnas,encabezado

def pearson(valorX, valorY):
    """
    Pearson
    valorX: Vector para la variable independiente del dataset
    valorY: Vector para la variable dependiente del dataset
    Returns
        Coeficiente de correlación de Pearson entre valorX e valorY
    """
    valorX = np.asarray(valorX)
    valorY = np.asarray(valorY)
    cantidadDatos = len(valorX)
    mediaX = np.mean(valorX)
    mediaY = np.mean(valorY)
    sumaXY = 0.0
    sumaX2 = 0.0
    sumaY2 = 0.0
        
    for i in range(cantidadDatos):
        dx = valorX[i] - mediaX 
        dy = valorY[i] - mediaY
        sumaXY += dx * dy
        sumaX2 += dx * dx
        sumaY2 += dy * dy
    
    return sumaXY / math.sqrt(sumaX2 * sumaY2)


#Resultados:
#Coeficiente de Pearson
#0.032583309074479656 ----- clin_size_long_diam_mm
#0.04302830016159388 ----- tbp_lv_areaMM2
#0.03482986852518968 ----- tbp_lv_perimeterMM
#0.02835473987624596 ----- tbp_lv_color_std_mean
#0.025109405446334842 ----- tbp_lv_deltaLBnorm
#0.03619925443748412 ----- tbp_lv_minorAxisMM
#0.001894184341872667 ----- tbp_lv_norm_border
#-0.003250227120819911 ----- tbp_lv_symm_2axis
#0.0005004242912260194 ----- tbp_lv_symm_2axis_angle

#0.0325833090744688 ----- clin_size_long_diam_mm
#0.04302830016159504 ----- tbp_lv_areaMM2
#0.03482986852518373 ----- tbp_lv_perimeterMM
#0.0283547398762334 ----- tbp_lv_color_std_mean
#0.025109405446333402 ----- tbp_lv_deltaLBnorm
#0.0361992544374807 ----- tbp_lv_minorAxisMM
#0.0018941843418726419 ----- tbp_lv_norm_border
#-0.003250227120820135 ----- tbp_lv_symm_2axis
#0.0005004242912265165 ----- tbp_lv_symm_2axis_angle

