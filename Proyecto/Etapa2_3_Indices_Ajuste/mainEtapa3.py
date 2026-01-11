import coeficientePearson as cp
import pca as pc
import regresionMultivaraible as rm
import numpy as np
import csv
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
minAsimetria,maxAsimetria,vector_Propio_Asimetria,indicePCA_Asimetria,media_Asimetria=pc.PCA(matrizAsimetria)
minBorde,maxBorde,vector_Propio_Borde,indicePCA_Borde,media_Borde=pc.PCA(matrizBorde)
minColor,maxColor,vector_Propio_Color,indicePCA_Color,media_Color=pc.PCA(matrizColor)
minDiametro,maxDiametro,vector_Propio_Diametro,indicePCA_Diametro,media_Diametro=pc.PCA(matrizDiametro)
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

vectoresPropio=[
    vector_Propio_Asimetria,
    vector_Propio_Borde,
    vector_Propio_Color,
    vector_Propio_Diametro
]
mediaPCA=[
    media_Asimetria,
    media_Borde,
    media_Color,
    media_Diametro
]
def obtenerY(valoresCrudos, promedios, desviaciones, vectoresPropios, mediaPCA):
    # normalizar los valores crudos utilizando Z-score
    valoresNormalizados = []
    for i,valores in enumerate(valoresCrudos):
        media = promedios[i]
        desviacionE = desviaciones[i]
        if desviacionE != 0:
            z = (valoresCrudos[i] - media) / desviacionE
        else:
            z = 0.0
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
    valoresCentradosPCA=[]
    indicePCA=[]
    for i,valores in enumerate(valoresNormalizadosDict.values()):
        valoresCentradosPCA.append(np.array(valores)-np.array(mediaPCA[i]))
        indicePCA.append(np.dot(valoresCentradosPCA[i], vectoresPropios[i]))
    #Ajuste Curva y= 0.0006890449 + -0.0001848667 *Asimetria + 0.002024672 *Borde + 0.0006305808 *Color + -0.0016166086 *Diametro
    y= (coeficientes[0] +
        coeficientes[1]*indicePCA[0]+
        coeficientes[2]*indicePCA[1]+
        coeficientes[3]*indicePCA[2]+
        coeficientes[4]*indicePCA[3])
    print(y)
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

for valor in matriz:
    valorNumerico=obtenerY(valor[1:], promedio, desviacion, vectoresPropio, mediaPCA)
    if valor[0]==1:
        if valorNumerico>valorMayorMelanoma:
            valorMayorMelanoma=valorNumerico
        if valorNumerico<valormenorMelanoma:
            valormenorMelanoma=valorNumerico
    else:
        if valorNumerico> 0.016660034540234795:
            contadorMax+=1
        elif valorNumerico<-0.0011328162072616226:
            contadorMin+=1
        else:
            contadorBet+=1  
        if valorNumerico>valorMayorlunar:
            valorMayorlunar=valorNumerico
        if valorNumerico<valormenorlunar:
            valormenorlunar=valorNumerico
print("Rango Melanoma:", valormenorMelanoma, " | ", valorMayorMelanoma)
print("Rango Lunar:", valormenorlunar, " | ", valorMayorlunar)
print("Lunares mal clasificados como Melanoma:", contadorMax)
print("Lunares mal clasificados como Lunares:", contadorMin)
print("Lunares correctamente clasificados:", contadorBet)
print(contadorMax+contadorMin)