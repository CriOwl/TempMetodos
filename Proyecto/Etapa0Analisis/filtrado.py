import csv

def filtrado(archivoCrudo, archivoFiltrado):
    """filtrado
    Filtra el dataset original de la ISIC2024 con las variables selecionadas:
    {
    target,clin_size_long_diam_mm,tbp_lv_areaMM2,tbp_lv_perimeterMM,tbp_lv_color_std_mean,
    tbp_lv_deltaLBnorm,tbp_lv_minorAxisMM,tbp_lv_norm_border,tbp_lv_symm_2axis,
    tbp_lv_symm_2axis_angle
    }
    este filtrado solo toma en cuenta las imagenes que son 3D: XP y se quitan los datos que 
    contiene un dato nulo con las variables selecionadas
    Args:
        archivoCrudo (str): path del dataset original
        archivoFiltrado (str): path del dataset filtrado
    """

    try:
        listadoFiltrado = []
        with open(archivoCrudo, "r", encoding="utf-8", newline="") as archivo:
            reader = csv.reader(archivo)
            header = next(reader)
            listadoFiltrado.append([header[1], header[6], header[19], header[20], header[21], header[26], header[30], header[32], header[33], header[35]]) 
            for row in reader:
                if row[1] != "" and row[6] != "" and row[19] != "" and row[20] != "" and row[21] != "" and row[26] != "" and row[30] != "" and row[32] != "" and row[33] != "" and row[35] != "" and row[8].__contains__("3D: XP"):
                    listadoFiltrado.append([row[1], row[6], row[19], row[20], row[21], row[26], row[30], row[32], row[33], row[35]])
        with open(archivoFiltrado, "w", encoding="utf-8", newline="") as archivoE:
            writer = csv.writer(archivoE)
            for row in listadoFiltrado:
                writer.writerow(row)
    except Exception as e:
        print(f"Se ha producido un error: {e}")

def mediana(lista):
    """
    Obtiene la mediana de una lista para ello lo organiza
    y luego obtiene la mediana
    Args:
    lista (list): lista de la cual se obtiene la mediana
    return (float): valor de la mediana
    """
    lista_ordenada = sorted(lista)
    n = len(lista_ordenada)
    mitad = n // 2

    if n % 2 == 0:
        return (lista_ordenada[mitad + 1] + lista_ordenada[mitad]) / 2
    else:
        return lista_ordenada[mitad]


