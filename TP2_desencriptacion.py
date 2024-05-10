from PIL import Image
import numpy as np

TABLA_CHARS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ".", ",", "?", "!", "¿", "¡", "(", ")", ":", ";", "-", '"', "'", "á", "é", "í", "ó", "ú", "ü", "ñ"]

def num_a_char(n : int) -> str:
    """
    Recibe un número y lo convierte al caracter 
    correspondiente según la tabla de caracteres.

    PARAMETRO:
        - n (int): el numero que es pasado a caracter.
    
    RETURN:
        - str: caracter correspondiente con el número dado.
    """
    return TABLA_CHARS[n-1]

def seq_a_string(seq : list) -> str:
    """
    Recibe una secuencia de números y devuelve el string correspondiente.

    PARAMETRO:
        - seq (list): la secuencia para convertir a cadena. 
    
    RETURN:
        - str: cadena correspondiente para la secuencia de números.
    """
    string = ''
    guardar_todo = []
    guardar_char = ''
    for n in seq:
        if n == 0:
            for num in guardar_todo:
                string += num_a_char(int(num))
            return string 
        if n == -1:
            guardar_todo.append(guardar_char)
            guardar_char = ''
        else:
            guardar_char += str(n - 1)
        
def calcular_varianza(array_im: np.array, i: int, j: int) -> int:
    """
    Recibe el array 3D de la imagen y una posición, y devuelve
    las varianzas de cada canal y los valores de los 3 canales en cada posición del cuadrante.

    PARAMETRO:
        - array (np.array): array 3D de la imagen.
        - i (int): numero de fila de la posicion superior izquierda.
        - j (int): numero de columna de la posicion superior izquierda.
    
    RETURN:
        - list: una lista con las varianzas de los 3 canales.
        - np.array: valores de los 3 canales de la posicion superior izquierda.
        - np.array: valores de los 3 canales de la posicion superior derecha.
        - np.array: valores de los 3 canales de la posicion inferior izquierda.
        - np.array: valores de los 3 canales de la posicion inferior derecha.
    """
    varianzas = []

    sup_izq = array_im[i,j,:]
    sup_der = array_im[i,j+1,:]
    inf_izq = array_im[i+1,j,:]
    inf_der = array_im[i+1,j+1,:]
    for canal in range(0,3):
        chek_vari = np.var([sup_izq[canal], sup_der[canal], inf_izq[canal]])
        varianzas.append(chek_vari)
    return varianzas, sup_izq, sup_der, inf_izq, inf_der

def imagen_a_seq(array_im: np.array) -> list:
    """
    Recibe un array 3D correspondiente con una imagen
    y devuelve una secuencia de números oculta en ella.

    PARAMETRO:
        - array_im (np.array): array 3D de la imagen.
    
    RETURN:
        - list: secuencia de números escondidos en la imagen.
    """
    height,width,_ = array_im.shape

    seq = []
    for i in range(0,height,2):
        for j in range(0,width,2):
            varianzas, sup_izq, sup_der, inf_izq, inf_der = calcular_varianza(array_im, i, j)

            min_varianzas = min(varianzas)
            canal_encript = varianzas.index(min_varianzas)

            promedio_menor_var = sum([sup_izq[canal_encript], sup_der[canal_encript], inf_izq[canal_encript]]) // 3
            extraer_valor = inf_der[canal_encript] - promedio_menor_var
            if extraer_valor < -1:
                extraer_valor += 256

            seq.append(extraer_valor)
            if extraer_valor == 0:
                return seq
            