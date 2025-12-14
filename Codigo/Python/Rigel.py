import csv
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
        valoresColumnas = [[0]]*len(encabezado)
        for fila in reader:
            for i,valor in enumerate(fila):
                valoresColumnas[i].append(float(valor))
normalizarArchivo()
agregarVColumnas()






