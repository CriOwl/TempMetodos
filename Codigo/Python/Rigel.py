import csv
import  math
import  numpy  as  np
filtradoFile = "../../processed_data.csv"
NormalizadoFile = "../../normal_Data.csv"
maxValores=list()
minValores=list()
valoresColumnas=list()
def normalizar(x, xmax, xmin):
    if xmax == xmin:
        return 0.0
    return (x - xmin) / (xmax - xmin)
def normalizarArchivo():
    global maxValores
    global minValores
    global filtradoFile
    global NormalizadoFile
    with open(filtradoFile,"r") as f:
        reader = csv.reader(f)
        encabezado = next(reader)
        num_cols = len(encabezado)
        maxValores = [-1] * num_cols
        minValores = [ -1] * num_cols
        for fila in reader:
            for i in range(num_cols):
                valor = float(fila[i])
                if valor> maxValores[i] or maxValores[i]==-1:
                    maxValores[i] = valor
                if valor < minValores[i] or minValores[i]==-1:
                    minValores[i] = valor
    with open(filtradoFile, newline="") as f_in, \
            open(NormalizadoFile, "w", newline="") as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        encabezado = next(reader)
        writer.writerow(encabezado)
        for fila in reader:
            salida = []
            for i in range(num_cols):
                v = float(fila[i])
                salida.append(normalizar(v, maxValores[i], minValores[i]))
            writer.writerow(salida)
def agregarVColumnas():
    global valoresColumnas
    with open(NormalizadoFile, newline="") as f_in:
        reader = csv.reader(f_in)
        encabezado = next(reader)
        # Referencias de listas a una misma aaaaaaaaaaaaaaaaaaaaaaaaaaaaa py
        valoresColumnas = [[] for _ in range(len(encabezado))]
        for fila in reader:
            for i,valor in enumerate(fila):
                valoresColumnas[i].append(float(valor))
normalizarArchivo()
agregarVColumnas()
def pearson(x, y):
    """
    Pearson

    :param x: Vector para la variable del dataset
    :param y: Vector correspondiente a la variable objetivo (target)
    :return: Coeficiente de correlación de Pearson entre x e y
    """
    # Conversión a arrays de numpy (para tener compatiblidad con numpy)
    x = np.asarray(x)
    y = np.asarray(y)
    n = len(x)
    # Calculo de la medias
    media_x = np.mean(x)
    media_y = np.mean(y)
    # Inicializar las sumatorias
    sum_xy = 0.0
    sum_x2 = 0.0
    sum_y2 = 0.0
    for i in range(n):
        # numerador
        dx = x[i] - media_x
        dy = y[i] - media_y
        sum_xy += dx * dy
        # denominador X
        sum_x2 += dx * dx
        # denominador Y
        sum_y2 += dy * dy
    return sum_xy / math.sqrt(sum_x2 * sum_y2)
def coeficientesPearson():
    global valoresColumnas
    listaPearson = []
    for columna in valoresColumnas[1:]:
        coeficiente = pearson(columna,valoresColumnas[0])
        listaPearson.append(coeficiente)
    return listaPearson
print(coeficientesPearson())





