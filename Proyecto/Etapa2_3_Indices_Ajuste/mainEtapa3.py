from . import coeficientePearson as cp
from . import pca as pc
from . import minimosCuadrados as rm
archivoNormalizado = "Archivos/datasetNormalizado.csv"

listaColumnas,encabezado=cp.obtenerColunmas(archivoNormalizado)

matrizAsimetria=listaColumnas[8:]
matrizBorde=[listaColumnas[2], listaColumnas[3],listaColumnas[7]]
matrizColor=listaColumnas[4:6]
matrizDiametro=[listaColumnas[1], listaColumnas[6]]
print("-----------------------------")
print("Indice del analisis de componentes principales PCA")
minAsimetria,maxAsimetria,pesosPCA_Asimetria,indicePCA_Asimetria=pc.PCA(matrizAsimetria)
minBorde,maxBorde,pesosPCA_Borde,indicePCA_Borde=pc.PCA(matrizBorde)
minColor,maxColor,pesosPCA_Color,indicePCA_Color=pc.PCA(matrizColor)
minDiametro,maxDiametro,pesosPCA_Diametro,indicePCA_Diametro=pc.PCA(matrizDiametro)
print("Asimetria:", indicePCA_Asimetria,pesosPCA_Asimetria)
print("Variables usadas en Asimetria:", encabezado[8:])
print("Borde:", indicePCA_Borde,pesosPCA_Borde)
print("Variables usadas en Borde:", encabezado[2]+encabezado[3]+encabezado[7])
print("Color:", indicePCA_Color,pesosPCA_Color[4:6])
print("Variables usadas en Color:", encabezado)
print("Diametro:", indicePCA_Diametro,pesosPCA_Diametro)
print("Variables usadas en Diametro:", [encabezado[1], encabezado[6]])
print("-----------------------------")
matrizTemp=[]
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


# hacer funcion para el umbral
for valor in matriz:
    valorNumerico = obtenerY(valor[1:], promedio, desviacion, vectoresPropio, mediaPCA)
    all_scores.append(valorNumerico)
    all_labels.append(int(valor[0]))
    #if valorNumerico >= 0.0010853300321642134:
    #    melanomas+=1
    #else:
    #    lunares+=1
all_scores = np.array(all_scores)
all_labels = np.array(all_labels)

scores_melanoma = all_scores[all_labels == 1]
scores_lunar = all_scores[all_labels == 0]

print("\n Rango")
print(f"Melanoma (n={len(scores_melanoma)}): Min={scores_melanoma.min():.5f}, Max={scores_melanoma.max():.5f}, Media={scores_melanoma.mean():.5f}")
print(f"Lunar    (n={len(scores_lunar)}): Min={scores_lunar.min():.5f}, Max={scores_lunar.max():.5f}, Media={scores_lunar.mean():.5f}")

print("\n Umbral (GRID SEARCH)")

umbrales = np.linspace(all_scores.min(), all_scores.max(), 100)
mejor_umbral = 0
mejor_sensibilidad = 0
mejor_especificidad = 0
mejor_confusion = {}

for umbral in umbrales:
    y_pred = (all_scores >= umbral).astype(int)
    
    tp = np.sum((all_labels == 1) & (y_pred == 1))
    fn = np.sum((all_labels == 1) & (y_pred == 0))
    tn = np.sum((all_labels == 0) & (y_pred == 0))
    fp = np.sum((all_labels == 0) & (y_pred == 1))
    
    sensibilidad = tp / (tp + fn) if (tp + fn) > 0 else 0
    especificidad = tn / (tn + fp) if (tn + fp) > 0 else 0
    weighted_score = 1.50 * sensibilidad + especificidad
    
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
