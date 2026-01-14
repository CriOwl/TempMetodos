import csv
archivoFiltrado = "Archivos/datasetEntrenamiento.csv"
archivoNormalizado = "Archivos/datasetNormalizadoMinMax.csv"
archivoNormalizadoZScore="Archivos/datasetZScore.csv"
valoresColumnas=list()

def normalizarMinMax(valor, valorMax, valorMin):
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


def normalizarArchivoMinMax(archivoFiltrado, archivoNormalizado):
    """
    normalizarArchivo
    Normalizamos todas las columnas de un archivo CSV utilizando
    el metodo Min-Max y guardamos el resultado en otro archivo CSV

    El procedimiento se divide en dos fases:
    1. Calculo de valores maximos y minimos por columna
    2. Generacion del archivo normalizado
    """
    maxValores=[]
    minValores=[]
    with open(archivoFiltrado,"r") as archivo:
        reader = csv.reader(archivo)
        encabezado = next(reader)
        numColumnas = len(encabezado)
        maxValores = [-1] * numColumnas
        minValores = [ -1] * numColumnas
        for fila in reader:
            for i in range(numColumnas):
                valor = float(fila[i])
                if valor> maxValores[i] or maxValores[i]==-1:
                    maxValores[i] = valor
                if valor < minValores[i] or minValores[i]==-1:
                    minValores[i] = valor
        print(maxValores)
        print(minValores)
        print("-------")
    with open(archivoFiltrado, newline="") as f_in, \
            open(archivoNormalizado, "w", newline="") as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        encabezado = next(reader)
        writer.writerow(encabezado)
        for fila in reader:
            salida = []
            for i in range(numColumnas):
                v = float(fila[i])
                salida.append(normalizarMinMax(v, maxValores[i], minValores[i]))
            writer.writerow(salida)
    listadoNormalizado = []
    with open(archivoFiltrado, "r", encoding="utf-8", newline="") as archivo:
        reader = csv.reader(archivo)
        encabezado = next(reader) 
        for row in reader:
            temporalList=[]
            for i,valor in enumerate(row):
                temporalList.append(normalizarMinMax(float(valor), maxValores[i], minValores[i]))
            listadoNormalizado.append(temporalList)
    with open(archivoNormalizado, "w", encoding="utf-8", newline="") as archivoE:
        writer = csv.writer(archivoE)
        writer.writerow(encabezado)
        for row in listadoNormalizado:
            writer.writerow(row)
                            

def promedioxColumna():
    with open(archivoFiltrado, "r", encoding="utf-8", newline="") as archivo:
        reader = csv.reader(archivo)
        encabezado = next(reader)

        numColumnas = len(encabezado)
        sumaColumnas = [0.0] * numColumnas
        contadorFilas = 0

        for fila in reader:
            for i in range(numColumnas):
                sumaColumnas[i] += float(fila[i])
            contadorFilas += 1

        promedios = []
        for i in range(numColumnas):
            promedio = sumaColumnas[i] / contadorFilas
            promedios.append(promedio)
            print(f"{encabezado[i]}: {promedio}")

    return promedios

def desviacionxColumna(promedios):
    with open(archivoFiltrado, "r", encoding="utf-8", newline="") as archivo:
        reader = csv.reader(archivo)
        encabezado = next(reader)

        numColumnas = len(encabezado)
        sumaDesviacion = [0.0] * numColumnas
        contadorFilas = 0

        for fila in reader:
            for i in range(numColumnas):
                sumaDesviacion[i] += (float(fila[i]) - promedios[i]) ** 2
            contadorFilas += 1

        desviaciones = []
        for i in range(numColumnas):
            varianza = sumaDesviacion[i] / (contadorFilas - 1)
            desviacion = varianza ** 0.5
            desviaciones.append(desviacion) 
            print(f"{encabezado[i]}: {desviacion}")

    return desviaciones

def zscore(promedio, desviacion, archivoFiltrado, archivoNormalizadoZScore):
    with open(archivoFiltrado, "r", encoding="utf-8", newline="") as archivo_entrada, \
         open(archivoNormalizadoZScore, "w", encoding="utf-8", newline="") as archivo_salida:
        reader = csv.reader(archivo_entrada)
        writer = csv.writer(archivo_salida)

        encabezado = next(reader)
        writer.writerow(encabezado)

        numColumnas = len(encabezado)
        indice_target = encabezado.index("target")

        for fila in reader:
            fila_normalizada = []
            for i in range(numColumnas):
                x = float(fila[i])
                if i == indice_target:
                    fila_normalizada.append(x)
                else:
                    media = promedio[i]
                    desviacionE = desviacion[i]
                    if desviacionE != 0:
                        z = (x - media) / desviacionE
                    else:
                        z = 0.0
                    
                    fila_normalizada.append(z)

            writer.writerow(fila_normalizada)


normalizarArchivoMinMax(archivoFiltrado, archivoNormalizado)
#print ("\nPromedios:\n")
promedios = promedioxColumna()
#print ("\nDesviaciones estandar:\n")
desviaciones = desviacionxColumna(promedios)
#print(promedios)
#print(desviaciones)
zscore(promedios, desviaciones,archivoFiltrado,archivoNormalizadoZScore)

#target,clin_size_long_diam_mm,tbp_lv_areaMM2,tbp_lv_perimeterMM,tbp_lv_color_std_mean,tbp_lv_deltaLBnorm,tbp_lv_minorAxisMM,tbp_lv_norm_border,tbp_lv_symm_2axis,tbp_lv_symm_2axis_angle
# MAX=[1.0, 28.4, 334.1527, 102.4939, 8.8956374248806, 30.4874559973219, 18.3879, 10.0, 0.977055449330784, 175.0]
# MIN=[0.0, 1.0, 0.544192156126853, 2.645713, 0.0, 3.00728914105364, 0.433188693164146, 0.5894259, 0.05203443, 0.0]

# --Promedio--
#target: 0.0007065358059754741
#clin_size_long_diam_mm: 3.9545476421989574
#tbp_lv_areaMM2: 8.621497690717874
#tbp_lv_perimeterMM: 11.906887224523816
#tbp_lv_color_std_mean: 1.0794695661641536
#tbp_lv_deltaLBnorm: 7.678605971715849
#tbp_lv_minorAxisMM: 2.5441429751158595
#tbp_lv_norm_border: 3.451411985727956
#tbp_lv_symm_2axis: 0.3076509608629095
#tbp_lv_symm_2axis_angle: 86.33251953466572

# --- Desviacion
#target: 0.026571442418072997
#clin_size_long_diam_mm: 1.7736399644493928
#tbp_lv_areaMM2: 9.86678224963287
#tbp_lv_perimeterMM: 5.967126826947403
#tbp_lv_color_std_mean: 0.7923160578626247
#tbp_lv_deltaLBnorm: 2.551027857901019
#tbp_lv_minorAxisMM: 1.1877901254262564
#tbp_lv_norm_border: 1.738646412398361
#tbp_lv_symm_2axis: 0.12637249221128327
#tbp_lv_symm_2axis_angle: 52.65331716463431




