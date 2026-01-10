import csv
archivoFiltrado = "Archivos/datasetFiltrado.csv"
archivoNormalizado = "Archivos/datasetNormalizado.csv"
valoresColumnas=list()

def normalizar(valor, valorMax, valorMin):
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


def normalizarArchivo():
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
    global archivoFiltrado
    global archivoNormalizado
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
                salida.append(normalizar(v, maxValores[i], minValores[i]))
            writer.writerow(salida)
    listadoNormalizado = []
    with open(archivoFiltrado, "r", encoding="utf-8", newline="") as archivo:
        reader = csv.reader(archivo)
        encabezado = next(reader) 
        for row in reader:
            temporalList=[]
            for i,valor in enumerate(row):
                temporalList.append(normalizar(float(valor), maxValores[i], minValores[i]))
            listadoNormalizado.append(temporalList)
    with open(archivoNormalizado, "w", encoding="utf-8", newline="") as archivoE:
        writer = csv.writer(archivoE)
        writer.writerow(encabezado)
        for row in listadoNormalizado:
            writer.writerow(row)
                            
#normalizarArchivo()