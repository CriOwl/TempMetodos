import coeficientePearson as cp
import pca as pc
import regresionMultivaraible as rm
import numpy as np
import csv
archivoNormalizado = "Archivos/datasetZScore.csv"

listaColumnas,encabezado=cp.obtenerColunmas(archivoNormalizado)
print(encabezado)
for coeficiente in listaColumnas[1:]:
    valorPearson=cp.pearson(coeficiente,listaColumnas[0])
    print(valorPearson,"-----",encabezado[listaColumnas.index(coeficiente)])
matrizAsimetria=listaColumnas[8:]
matrizBorde=[listaColumnas[2], listaColumnas[3],listaColumnas[7]]
matrizColor=listaColumnas[4:6]
matrizDiametro=[listaColumnas[1], listaColumnas[6]]
min=[0.0006890448858528942, 3.955877238084303, 8.626383141872125, 11.911934960384956, 1.0776789497811687, 7.675518232618807, 2.5449166518056723, 3.4527523151897266, 0.3078127401545026, 86.38305649118757]
max=[0.026240665224301147, 1.7715892643386137, 9.85873906139436, 5.9758202200215065, 0.7892753964542302, 2.545224664609628, 1.189693225217179, 1.7391597458529817, 0.12638911026574534, 52.61625728963092]
matrizTemp=[]
indicePCA_Asimetria=[]
indicePCA_Borde=[]
indicePCA_Color=[]
indicePCA_Diametro=[]
for i in range(len(matrizAsimetria)):
    for j in range(len(matrizAsimetria[0])):
        indicePCA_Asimetria.append(matrizAsimetria[0][j]*-0.003250227120819911 + matrizAsimetria[1][j]*.0005004242912260194)
for i in range(len(matrizBorde)):
    for j in range(len(matrizBorde[0])):
        indicePCA_Borde.append(0.04302830016159504*matrizBorde[0][j]+0.03482986852518373*matrizBorde[1][j]+0.025109405446333402*matrizBorde[2][j])
for i in range(len(matrizColor)):
    for j in range(len(matrizColor[0])):
        indicePCA_Color.append(0.0283547398762334*matrizColor[0][j]+0.025109405446333402*matrizColor[1][j])
for i in range(len(matrizDiametro)):
    for j in range(len(matrizDiametro[0])):
        indicePCA_Diametro.append(matrizDiametro[0][j]*0.0325833090744688 + matrizDiametro[1][j]*0.0361992544374807)

for i in range(len(listaColumnas[0])):
    fila = [
        indicePCA_Asimetria[i],
        indicePCA_Borde[i],
        indicePCA_Color[i],
        indicePCA_Diametro[i]
    ]
    matrizTemp.append(fila)

coeficientes=rm.ajuste_minimos_cuadrados(matrizTemp, listaColumnas[0])
print("Ajuste Curva", "y=", round(coeficientes[0],10), "+", round(coeficientes[1],10), "*Asimetria +", round(coeficientes[2],10), "*Borde +", round(coeficientes[3],10), "*Color +", round(coeficientes[4],10), "*Diametro")

def obtenerY(valoresCrudos):
    # normalizar los valores crudos utilizando Z-score
    valoresNormalizados = []
    for i,valores in enumerate(valoresCrudos):
        z = (valores - min[i]) / (max[i] - min[i])
        valoresNormalizados.append(z)
        
#target ,
# clin_size_long_diam_mm, 0
# tbp_lv_areaMM2, 1
# tbp_lv_perimeterMM, 2
# tbp_lv_color_std_mean, 3
# tbp_lv_deltaLBnorm, 4
# tbp_lv_minorAxisMM, 5
# tbp_lv_norm_border, 6
# tbp_lv_symm_2axis, 7
# tbp_lv_symm_2axis_angle 8
    valoresNormalizadosDict={
            "Asimetria": valoresNormalizados[7:],
            "Borde": [valoresNormalizados[1], valoresNormalizados[2], valoresNormalizados[6]],
            "Color": [valoresNormalizados[3],valoresNormalizados[4]],
            "Diametro": [valoresNormalizados[0], valoresNormalizados[5]]
    }

#0.0325833090744688 ----- clin_size_long_diam_mm
#0.04302830016159504 ----- tbp_lv_areaMM2
#0.03482986852518373 ----- tbp_lv_perimeterMM
#0.0283547398762334 ----- tbp_lv_color_std_mean
#0.025109405446333402 ----- tbp_lv_deltaLBnorm
#0.0361992544374807 ----- tbp_lv_minorAxisMM
#0.0018941843418726419 ----- tbp_lv_norm_border
#-0.003250227120820135 ----- tbp_lv_symm_2axis
#0.0005004242912265165 ----- tbp_lv_symm_2axis_angle
    valoresCentradosPCA=[]
    indiceABCDE=[]
    indiceABCDE.append(-0.003250227120819911*valoresNormalizados[7]+0.0005004242912260194*valoresNormalizados[8])
    indiceABCDE.append(0.04302830016159504*valoresNormalizados[1]+0.03482986852518373*valoresNormalizados[2]+0.025109405446333402*valoresNormalizados[6])
    indiceABCDE.append(0.0283547398762334*valoresNormalizados[3]+0.025109405446333402*valoresNormalizados[4])
    indiceABCDE.append(0.0325833090744688*valoresNormalizados[0]+0.0361992544374807*valoresNormalizados[8])
    
    y= (coeficientes[0] +
        coeficientes[1]*indiceABCDE[0]+
        coeficientes[2]*indiceABCDE[1]+
        coeficientes[3]*indiceABCDE[2]+
        coeficientes[4]*indiceABCDE[3])
    return y
    # obtener indice PCA para cada componente
def procesar_datos_melanoma(nombre_archivo):
    matriz = []
    try:
        with open(nombre_archivo, 'r') as f:
            lector = csv.reader(f)
            
            # 1. Saltar la cabecera (target, clin_size_long_diam_mm, etc.)
            next(lector, None)
            
            for fila in lector:
                if fila: # Asegurarse de que la fila no esté vacía
                    # 2. 'fila[1:]' crea una nueva lista ignorando el primer elemento (target)
                    # 3. 'float(x)' convierte cada texto a número decimal
                    datos_procesados = [float(x) for x in fila[:]]
                    matriz.append(datos_procesados)
                    
        return matriz
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return []
    except ValueError:
        print("Error: Se encontró un valor que no se pudo convertir a número.")
        return []
matriz=procesar_datos_melanoma("Archivos/datasetFiltrado.csv")
valorMayorMelanoma=float('-inf')
valormenorMelanoma=float('inf')
valorMayorlunar=float('-inf')
valormenorlunar=float('inf')
contadorMax=0
contadorMin=0
contadorBet=0

# Recopilar todos los scores y etiquetas
all_scores = []
all_labels = []
melanomas=0
lunares=0
# Calcular scores para todas las filas
for valor in matriz:
    valorNumerico = obtenerY(valor[1:])
    all_scores.append(valorNumerico)
    all_labels.append(int(valor[0]))
print(f"\nTotal Melanomas Clasificados: {melanomas}")
##64298 
#197
all_scores = np.array(all_scores)
all_labels = np.array(all_labels)

# Analisis de Rangos
scores_melanoma = all_scores[all_labels == 1]
scores_lunar = all_scores[all_labels == 0]

print("\n--- Estadisticas de Scores ---")
print(f"Melanoma (n={len(scores_melanoma)}): Min={scores_melanoma.min():.5f}, Max={scores_melanoma.max():.5f}, Media={scores_melanoma.mean():.5f}")
print(f"Lunar    (n={len(scores_lunar)}): Min={scores_lunar.min():.5f}, Max={scores_lunar.max():.5f}, Media={scores_lunar.mean():.5f}")

# Busqueda de Umbral Optimo (Grid Search)
print("\n--- Buscando mejor umbral (Maximizando Sensibilidad) ---")

umbrales = np.linspace(all_scores.min(), all_scores.max(), 100)
mejor_umbral = 0
mejor_sensibilidad = 0
mejor_especificidad = 0
mejor_confusion = {}

# Queremos alta sensibilidad (detectar melanomas) pero una especificidad razonable
# Si solo maximizamos sensibilidad, el umbral sera el minimo y clasificara todo como melanoma.
# Busquemos un balance, o reportemos varios.
# En este caso, priorizamos sensibilidad > 0.5 si es posible.

for umbral in umbrales:
    y_pred = (all_scores >= umbral).astype(int)
    
    tp = np.sum((all_labels == 1) & (y_pred == 1))
    fn = np.sum((all_labels == 1) & (y_pred == 0))
    tn = np.sum((all_labels == 0) & (y_pred == 0))
    fp = np.sum((all_labels == 0) & (y_pred == 1))
    
    sensibilidad = tp / (tp + fn) if (tp + fn) > 0 else 0
    especificidad = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    # Criterio Ponderado: Priorizar Sensibilidad (Minimizar Falsos Negativos)
    # Damos doble peso a la sensibilidad para reducir Falsos Negativos
    # Score = 2 * Sensibilidad + Especificidad
    weighted_score = 1.00 * sensibilidad + especificidad
    
    if weighted_score > (1.00 * mejor_sensibilidad + mejor_especificidad):
        mejor_sensibilidad = sensibilidad
        mejor_especificidad = especificidad
        mejor_umbral = umbral
        mejor_confusion = {'TP': tp, 'FN': fn, 'TN': tn, 'FP': fp}

print(f"Sensibilidad: {mejor_sensibilidad:.2%}")
print(f"Especificidad: {mejor_especificidad:.2%}")
print(f"Matriz de Confusion: TP={mejor_confusion['TP']}, FN={mejor_confusion['FN']} (Melanomas perdidos), FP={mejor_confusion['FP']}, TN={mejor_confusion['TN']}")

# Clasificacion final con este umbral
print("\n--- Resultados Finales con Umbral Optimo ---")
preds_final = (all_scores >= mejor_umbral).astype(int)
print(mejor_umbral,"-------")
mal_clasificados_melanoma = np.sum((all_labels == 1) & (preds_final == 0)) # FN
mal_clasificados_lunar = np.sum((all_labels == 0) & (preds_final == 1))    # FP
bien_clasificados_lunar = np.sum((all_labels == 0) & (preds_final == 0))   # TN
bien_clasificados_melanoma = np.sum((all_labels == 1) & (preds_final == 1)) # TP

print(f"Lunares mal clasificados como Melanoma (Falsos Positivos): {mal_clasificados_lunar}")
print(f"Melanomas mal clasificados como Lunares (Falsos Negativos): {mal_clasificados_melanoma}")
print(f"Lunares correctamente clasificados: {bien_clasificados_lunar}")
print(f"Melanomas correctamente clasificados: {bien_clasificados_melanoma}")
