import coeficientePearson as cp
import pca as pc
import regresionMultivaraible as rm
archivoNormalizado = "Archivos/datasetZScore.csv"

listaColumnas,encabezado=cp.obtenerColunmas(archivoNormalizado)
promedio=[3.955877238084303, 8.626383141872125, 11.911934960384956, 1.0776789497811687, 7.675518232618807, 2.5449166518056723, 3.4527523151897266, 0.3078127401545026, 86.38305649118757]
desviacion=[1.7715892643386137, 9.85873906139436, 5.9758202200215065, 0.7892753964542302, 2.545224664609628, 1.189693225217179, 1.7391597458529817, 0.12638911026574534, 52.61625728963092]
matrizAsimetria=listaColumnas[8:]
matrizBorde=[listaColumnas[2], listaColumnas[3],listaColumnas[7]]
matrizColor=listaColumnas[4:6]
matrizDiametro=[listaColumnas[1], listaColumnas[6]]
print("-----------------------------")
print("Indice del analisis de componentes principales PCA")
minAsimetria,maxAsimetria,pesosPCA_Asimetria,indicePCA_Asimetria,media_Asimetria,vector_Propio_Asimetria=pc.PCA(matrizAsimetria)
minBorde,maxBorde,pesosPCA_Borde,indicePCA_Borde,media_Borde,vector_Propio_Borde=pc.PCA(matrizBorde)
minColor,maxColor,pesosPCA_Color,indicePCA_Color,media_Color,vector_Propio_Color=pc.PCA(matrizColor)
minDiametro,maxDiametro,pesosPCA_Diametro,indicePCA_Diametro,media_Diametro,vector_Propio_Diametro=pc.PCA(matrizDiametro)
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


