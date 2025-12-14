import csv
ruta_entrada = "../../processed_data.csv"
ruta_salida = "../../normal_Data.csv"
def normalizar(x, xmax, xmin):
    if xmax == xmin:
        return 0.0
    return (x - xmin) / (xmax - xmin)
with open(ruta_entrada,"r") as f:
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
with open(ruta_entrada, newline="") as f_in, \
     open(ruta_salida, "w", newline="") as f_out:
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
