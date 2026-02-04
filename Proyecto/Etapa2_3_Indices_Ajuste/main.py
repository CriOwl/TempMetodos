
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
    archivoSinOutliers = "Archivos/datasetMAD.csv"
    archivoNormalizado = "Archivos/datasetNormalizadoZ-score.csv"
    fil.filtrado(archivoCrudo, archivoFiltrado)
    fil.eliminarOutliersMAD(archivoFiltrado, archivoSinOutliers)
    promedios = nor.promedioxColumna(archivoFiltrado)
    desviaciones = nor.desviacionxColumna(promedios, archivoFiltrado)
    nor.zscore(promedios, desviaciones, archivoSinOutliers, archivoNormalizado)
    quit()
    columnasDatos= pears.obtenerColunmas(archivoNormalizado)
    matrizAsimetria=[columnasDatos[12],columnasDatos[25]]
    matrizBorde=[columnasDatos[13],columnasDatos[23]]
    matrizColor=[columnasDatos[26],columnasDatos[19],columnasDatos[14],columnasDatos[24]]
    matrizDiametro=[columnasDatos[1], columnasDatos [21]]
    
entrenar("Archivos/train-metadata.csv")