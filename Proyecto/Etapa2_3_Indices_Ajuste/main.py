
import Proyecto.Etapa0Analisis.filtrado as fil
import Proyecto.Etapa1Normalizacion.normalizacion as nor
import Proyecto.Etapa2_3_Indices_Ajuste.coeficientePearson as pears
import Proyecto.Etapa2_3_Indices_Ajuste.pca as pca
import Proyecto.Etapa2_3_Indices_Ajuste.regresionMultivaraible as rm
import json
import numpy as np
import math
diccionarioEntrenamientoPath = "Archivos/diccionario_entrenamiento.json"

def preparar_para_json(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: preparar_para_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [preparar_para_json(v) for v in obj]
    else:
        return obj


def obtenerY(archivoDatos):
    
    """
    Docstring for obtenerY
    Esta funcion aplica el modelo previamente entrenado a nuevos datos, 
    siguiendo el flujo de normalizacion, proyeccion PCA con vectores propios calculados 
    y aplicacion de la ecuacion de minimos cuadrados.

    :param diccionarioEntrenamiento: DIccionario que contiene los parametros aprendidos. 
    :param archivoDatos: Ruta del archivo CSV con los datos a evaluar "testeo"
    """
    global diccionarioEntrenamientoPath
    with open(diccionarioEntrenamientoPath, "r", encoding="utf-8") as f:
        diccionarioEntrenamiento = json.load(f)
    promedios = diccionarioEntrenamiento["promedios"]
    desviaciones = diccionarioEntrenamiento["desviaciones"]
    archivoFiltrado = "Archivos/datasetTesteoFiltrado.csv"
    archivoNormalizadoZ= "Archivos/datasetTesteoNormalizadoZ-score.csv"
    fil.filtrado(archivoDatos, archivoFiltrado)
    nor.zscore(promedios, desviaciones, archivoFiltrado, archivoNormalizadoZ)
    columnasDatos, _ = pears.obtenerColunmas(archivoNormalizadoZ)
    matrizAsimetria=[]
    matrizBorde=[]
    matrizColor=[]
    matrizDiametro=[]
    for i in range(len(columnasDatos[0])):
        matrizAsimetria.append([columnasDatos[2][i],columnasDatos[3][i]])
        matrizBorde.append([columnasDatos[3][i],columnasDatos[7][i]])
        matrizColor.append([columnasDatos[4][i],columnasDatos[5][i],columnasDatos[8][i],columnasDatos[9][i]])
        matrizDiametro.append([columnasDatos[1][i], columnasDatos [6][i]])
    indiceAsimetria = []
    vectorPropio_Asimetria = diccionarioEntrenamiento["Asimetria"]["vectorPropio"]
    media_Asimetria = diccionarioEntrenamiento["Asimetria"]["media"]
    vectorPropio_Borde = diccionarioEntrenamiento["Borde"]["vectorPropio"]
    media_Borde = diccionarioEntrenamiento["Borde"]["media"]
    vectorPropio_Color = diccionarioEntrenamiento["Color"]["vectorPropio"]
    media_Color = diccionarioEntrenamiento["Color"]["media"]
    vectorPropio_Diametro = diccionarioEntrenamiento["Diametro"]["vectorPropio"]
    media_Diametro = diccionarioEntrenamiento["Diametro"]["media"]
    indiceAsimetria = []
    indiceBorde = []
    indiceColor = []
    indiceDiametro = []
    for i in range(len(matrizAsimetria)):
        indiceAsimetria.append(pca.calcularIndicePCA(matrizAsimetria[i], media_Asimetria, vectorPropio_Asimetria))
        indiceDiametro.append(pca.calcularIndicePCA(matrizDiametro[i], media_Diametro, vectorPropio_Diametro))
        indiceBorde.append(pca.calcularIndicePCA(matrizBorde[i], media_Borde, vectorPropio_Borde))
        indiceColor.append(pca.calcularIndicePCA(matrizColor[i], media_Color, vectorPropio_Color))
    coeficientes=diccionarioEntrenamiento["coeficientes"]
    y_estimado = []
    for i in range(len(indiceAsimetria)):
        y = (
            coeficientes["terminoIndependiente"] + 
            coeficientes["Asimetria"] * indiceAsimetria[i] + 
            coeficientes["Borde"] * indiceBorde[i] + 
            coeficientes["Color"] * indiceColor[i] + 
            coeficientes["Diametro"] * indiceDiametro[i]
        )
        y_estimado.append(y)
    return y_estimado

def optimizar_umbral_desde_scores(y_scores,target,n_puntos=100,w_sens=1.50,w_spec=1.00):
    """

    """
    scores = np.asarray(y_scores, dtype=float)
    y_true = np.asarray(target, dtype=int)

    if scores.shape[0] != y_true.shape[0]:
        print("Error: Las dimensiones de y_scores y target no coinciden.")
        return
    
    smin, smax = float(scores.min()), float(scores.max())
    umbrales = np.linspace(smin, smax, int(n_puntos))
    mejor_umbral = float(umbrales[0])
    mejor_obj = -np.inf
    mejor = None
    for t in umbrales:
        y_pred = (scores >= t).astype(int)
        tp = int(np.sum((y_true == 1) & (y_pred == 1)))
        fn = int(np.sum((y_true == 1) & (y_pred == 0)))
        tn = int(np.sum((y_true == 0) & (y_pred == 0)))
        fp = int(np.sum((y_true == 0) & (y_pred == 1)))
        sens = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        weighted_score = w_sens * sens + w_spec * spec
        if weighted_score > mejor_obj:
            mejor_obj = weighted_score
            mejor_umbral = float(t)
            mejor = {
                "TP": tp, "FN": fn, "TN": tn, "FP": fp,
                "sensibilidad": float(sens),
                "especificidad": float(spec),
                "weighted_score": float(weighted_score),
            }
    return mejor_umbral

def entrenar(archivoEntrenamiento):
    """ 
    Ejecuta el flujo completo de entrenamiento del modelo para la deteccion de melanoma

    Este proceso integra todas las etapas del analisis numerico desarrollado:
    1. Preprocesamiento: Calculo de promedio, desviaciones y normalizacion zscore
    2. Reduccion de dimensionalidad: agrupacion de variables segun el estandar ABCD y aplicacion de PCA para obtener vectores propios u medias de proyecccion.
    3. Ajuste Numerico: Construccion de la matriz de diseño y resolucion del sistema de ecuaciones mediante minimos cuadrados para hallar los coeficientes beta.

    Args:
        archivoEntrenamiento (str): Ruta del archivo CSV con el dataset crudo. 

    Returns:
        dict: Diccionario de parametros del modelo que incluye
            - promedios y desviaciones para normalizar datos nuevos
            - vectorPropio y media para categiriaas ABCD para el PCA
            - coeficientes pesos finales para la regresion multivariable

    Note:
        se imprime en consola la ecuacion final del modelo ajustado
        y = b0 + b1*Asimetria + b2*Borde + b3*Color + b4*Diametro.
    """
    global diccionarioEntrenamientoPath
    archivoCrudo = archivoEntrenamiento
    archivoFiltrado = "Archivos/datasetFiltrado.csv"
    archivoNormalizado = "Archivos/datasetNormalizadoZ-score.csv"
    fil.filtrado(archivoCrudo, archivoFiltrado)
    promedios = nor.promedioxColumna(archivoFiltrado)
    desviaciones = nor.desviacionxColumna(promedios, archivoFiltrado)
    nor.zscore(promedios, desviaciones, archivoFiltrado, archivoNormalizado)
    columnasDatos,encabezado= pears.obtenerColunmas(archivoNormalizado)
    matrizAsimetria=[columnasDatos[2],columnasDatos[3]]
    matrizBorde=[columnasDatos[3],columnasDatos[7]]
    matrizColor=[columnasDatos[4],columnasDatos[5],columnasDatos[8],columnasDatos[9]]
    matrizDiametro=[columnasDatos[1], columnasDatos [6]]
    _,_,vector_Propio_Asimetria,indicePCA_Asimetria,media_Asimetria=pca.PCA(matrizAsimetria)
    _,_,vector_Propio_Borde,indicePCA_Borde,media_Borde=pca.PCA(matrizBorde)
    _,_,vector_Propio_Color,indicePCA_Color,media_Color=pca.PCA(matrizColor)
    _,_,vector_Propio_Diametro,indicePCA_Diametro,media_Diametro=pca.PCA(matrizDiametro)
    matrizTemp=[]
    for i in range(len(columnasDatos[0])):
        fila = [
            indicePCA_Asimetria[i],
            indicePCA_Borde[i],
            indicePCA_Color[i],
            indicePCA_Diametro[i]
        ]
        matrizTemp.append(fila)
    coeficientes=rm.ajuste_minimos_cuadrados(matrizTemp, columnasDatos[0])
    print("Ajuste Curva", "y=", round(coeficientes[0],10), "+", round(coeficientes[1],10), "*Asimetria +", round(coeficientes[2],10), "*Borde +", round(coeficientes[3],10), "*Color +", round(coeficientes[4],10), "*Diametro")
    diccionarioEntrenamiento={
        "promedios": promedios,
        "desviaciones": desviaciones,
        "Asimetria": {"vectorPropio": vector_Propio_Asimetria, "media": media_Asimetria},
        "Borde": {"vectorPropio": vector_Propio_Borde, "media": media_Borde},
        "Color": {"vectorPropio": vector_Propio_Color, "media": media_Color},
        "Diametro": {"vectorPropio": vector_Propio_Diametro, "media": media_Diametro},
        "coeficientes": {"terminoIndependiente": coeficientes[0], "Asimetria": coeficientes[1], "Borde": coeficientes[2], "Color": coeficientes[3], "Diametro": coeficientes[4]}
    }
    diccionarioEntrenamiento = preparar_para_json(diccionarioEntrenamiento)
    with open(diccionarioEntrenamientoPath, "w", encoding="utf-8") as f:
        json.dump(diccionarioEntrenamiento, f, indent=4)
    valoresY=obtenerY(archivoEntrenamiento)
    umbral=optimizar_umbral_desde_scores(valoresY,columnasDatos[0],n_puntos=1000,w_sens=1.50,w_spec=1.00)
    diccionarioEntrenamiento["umbral"] = umbral
    diccionarioEntrenamiento = preparar_para_json(diccionarioEntrenamiento)
    with open(diccionarioEntrenamientoPath, "w", encoding="utf-8") as f:
        json.dump(diccionarioEntrenamiento, f, indent=4)
    

test = entrenar("Archivos/train-metadata.csv")

