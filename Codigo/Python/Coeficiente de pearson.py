import  numpy  as  np
import  math


def pearson(x, y):
    """
    Pearson
    
    :param x: Vector para la variable del dataset
    :param y: Vector correspondiente a la variable objetivo (target)
    :return: Coeficiente de correlación de Pearson entre x e y
    """
    #Conversión a arrays de numpy (para tener compatiblidad con numpy)

    x = np.asarray(x)
    y = np.asarray(y)

    n = len(x)

    #Calculo de la medias
    media_x = np.mean(x)
    media_y = np.mean(y)

    #Inicializar las sumatorias

    sum_xy = 0.0
    sum_x2 = 0.0
    sum_y2 = 0.0
    
    for i in range(n):
        #numerador
        dx = x[i] - media_x 
        dy = y[i] - media_y
        sum_xy += dx * dy
        #denominador X
        sum_x2 += dx * dx
        #denominador Y
        sum_y2 += dy * dy

    return sum_xy / math.sqrt(sum_x2 * sum_y2)

r = pearson(x, y)
print("Coeficiente de correlación de Pearson: ", r)

