import csv

"""
def normalizar(valor, valorMax, valorMin):
    
    Normalizar
    Se aplica la normalizacion Min-Max a un valor
    Args:
    valor (float): valor original
    valorMax (float): Valor maximo de la columna
    valorMin (float): Valor minimo de la columna
    
    if valorMax == valorMin:
        return 0.0
    return (valor - valorMin) / (valorMax - valorMin)


def normalizarArchivo():
    
    normalizarArchivo
    Normalizamos todas las columnas de un archivo CSV utilizando
    el metodo Min-Max y guardamos el resultado en otro archivo CSV

    El procedimiento se divide en dos fases:
    1. Calculo de valores maximos y minimos por columna
    2. Generacion del archivo normalizado
    
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
"""
def promedioxColumna(archivoFiltrado):
    """
    Calcula la meda aritmética de cada columna numérica en el dataset filtado

    Returns:
        list: una lista de floats que representan el promedio de cada columna

    Raises: 
        FileNotFoundError: Si el archivo especificado en archivoFiltrado no existi. 
    """
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

def desviacionxColumna(promedios,archivoFiltrado):
    """
    Calcula la desviacion estandar poblacional para cada columna del dataset

    Args:
        promedios list: Lista con los promedios previamente calculados de cada columna 
    
    Returns:
        list: Una lista de floats con la desviaciones estándar por columna
        
    
    :param promedios: Description
    """

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
    """
        Aplica la normalizacion zscore a los datos del archivo

        la formula aplicada es z = (x - media) / desviacion. La columna target se mantiene sin cambios para no afectar la clasificacion binaria

    Args:
        :param promedio: Lista de medias de las colimnas
        :param desviacion: Lista de desviaciones estandar de las columnas
        :param archivoFiltrado: Ruta del archivo fuente
        :param archivoNormalizadoZScore: Ruta donde se guarda el archivo de estandarizacion

    Returns:
        None: se escriben directamente en el archivo de salida
    """

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
