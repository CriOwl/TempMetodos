
import Proyecto.Etapa0Analisis.filtrado as fil
import Proyecto.Etapa1Normalizacion.normalizacion as nor
import Proyecto.Etapa2_3_Indices_Ajuste.coeficientePearson as pears
import Proyecto.Etapa2_3_Indices_Ajuste.pca as pca
import Proyecto.Etapa2_3_Indices_Ajuste.regresionMultivaraible as rm

def entrenar(archivoEntrenamiento):
    """ 
    """
    archivoCrudo = archivoEntrenamiento
    archivoFiltrado = "Archivos/datasetFiltrado.csv"
    archivoNormalizado = "Archivos/datasetNormalizadoZ-score.csv"
    #fil.filtrado(archivoCrudo, archivoFiltrado)
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
entrenar("Archivos/train-metadata.csv")