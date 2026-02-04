from . import coeficientePearson as cp
from . import pca as pc
from . import regresionMultivaraible as rm
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
