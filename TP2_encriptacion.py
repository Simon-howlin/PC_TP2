from PIL import Image
import numpy as np

TABLA_CHARS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ".", ",", "?", "!", "¿", "¡", "(", ")", ":", ";", "-", '"', "'", "á", "é", "í", "ó", "ú", "ü", "ñ"]

def char_a_num(c : str) -> int:
    """
    Recibe un caracter y lo convierte al número correspondiente según la tabla de caracteres.

    PARAMETRO:
        - c (str): el caracter que es pasado a número.
    
    RETURN:
        - int: número correspondiente con el caracter.
    """
    return TABLA_CHARS.index(c) + 1


def string_a_seq(s : str) -> list:
    """
    Recibe una cadena y devuelve una lista de los números correspondientes a cada caracter.

    PARAMETRO:
        - s(str): la cadena para convertir a secuencia de números.
    
    RETURN:
        - list: lista con la secuencia de números dentro.
    """
    s = s.lower()
    seq = []
    for c in s:
        num = char_a_num(c)
        num_str = str(num)
        for digito in num_str:
            seq.append(int(digito) + 1)
        seq.append(-1)
    seq.append(0)
    return seq


def calcular_varianza(array: np.array, i:int,j:int) -> tuple:
    """
    Recibe el array 3D de la imagen y una posición, y devuelve
    las varianzas de cada canal y los valores de los 3 canales en cada posición del cuadrante.

    PARAMETRO:
        - array (np.array): array 3D de la imagen.
        - i (int): numero de fila de la posicion superior izquierda.
        - j (int): numero de columna de la posicion superior izquierda.
    
    RETURN:
        - list: una lista con las varianzas de los 3 canales
        - np.array: valores de los 3 canales de la posicion superior izquierda.
        - np.array: valores de los 3 canales de la posicion superior derecha.
        - np.array: valores de los 3 canales de la posicion inferior izquierda.
        - np.array: valores de los 3 canales de la posicion inferior derecha.
    """
    varianzas = []

    sup_izq = array[i,j,:]
    sup_der = array[i,j+1,:]
    inf_izq = array[i+1,j,:]
    inf_der = array[i+1,j+1,:]
    for canal in range(0,3):
        chek_vari = np.var([sup_izq[canal], sup_der[canal], inf_izq[canal]])
        varianzas.append(chek_vari)
    return varianzas, sup_izq, sup_der, inf_izq, inf_der


def valor_a_cuadrante(valor: int, array: np.array, i: int, j: int) -> None:
    """
    Recibe el un valor, el array 3D de la imagen y una posición, y oculta el valor 
    en el cuadrante indicado del array en el canal con menos varianza.

    PARAMETRO:
        - valor (int): número a esconder.
        - array (np.array): array 3D de la imagen.
        - i (int): numero de fila de la posicion superior izquierda.
        - j (int): numero de columna de la posicion superior izquierda.
    """
    varianzas, sup_izq, sup_der, inf_izq, inf_der = calcular_varianza(array, i, j)

    min_varianzas = min(varianzas)
    modificar_x_canal = varianzas.index(min_varianzas)
    promedio_menor_var = sum([sup_izq[modificar_x_canal], sup_der[modificar_x_canal], inf_izq[modificar_x_canal]]) / 3
    reemplazar_canal = (promedio_menor_var + valor) % 256
    
    inf_der[modificar_x_canal] = reemplazar_canal


def seq_a_imagen(seq: list, array_im: np.array) -> Image:
    """
    Recibe una secuencia de números y un array 3D correspondiente con una imagen
    y devuelve una imagen con el mensaje oculto en ella.

    PARAMETRO:
        - seq (list): secuencia de números a esconder en la imagen.
        - array_im (np.array): array 3D de la imagen.
    
    RETURN:
        - (Image): Imagen habiendole ocultado la secuencia.
    """

    height,width,_ = array_im.shape

    contador = 0
    for i in range(0,height,2):
        for j in range(0,width,2):
            valor_a_cuadrante(seq[contador], array_im, i, j)
            
            contador += 1
            if contador >= len(seq):
                im_out = Image.fromarray(array_im)
                return im_out
            

def padding(array_im: np.array) -> np.array:
    """
    Recibe un array 3D correspondiente con una imagen y devuelve 
    array 3D de la imagen habiendole agregado 2 de padding en cada lado.

    PARAMETRO:
        - array_im (np.array): array 3D de la imagen.
    
    RETURN:
        - (np.array): array 3D de la imagen habiendole agregado 2 de padding en cada lado.
    """
    pad = np.pad(array_im,((2,2),(2,2),(0,0)),mode = 'edge')
    return pad


def calcular_varianza_3x3(array_im: np.array, i: int, j: int) -> tuple:
    """
    Recibe un array 3D correspondiente con una imagen y una posición,
    y devuelve la suma de las varianzas de cada canal de un cuadrante de 3x3 
    posicionado en la posición.

    PARAMETRO:
        - array_im (np.array): array 3D de la imagen.
        - i (int): numero de fila de la posicion superior izquierda del cuadrante.
        - j (int): numero de columna de la posicion superior izquierda del cuadrante.

    RETURN:
        - float: suma de las varianzas de cada canal del cuadrante 3x3.
        - np.array: cuadrante 3x3 utilizado.
    """
    suma_varianzas = 0
    for canal in range(0,3):
        suma_varianzas += np.var([array_im[i+offset_i, j+offset_j, canal] for offset_i in range(0,3) for offset_j in range(0,3)])
    
    return suma_varianzas, array_im[i:i+3,j:j+3,:]


def promedio_color(array_q: np.array, canal: int) -> int:
    """
    Recibe un array 3D correspondiente con un cuadrante y un numero de canal
    y devuelve el promedio de color de dicho cuadrante.

    PARAMETRO:
        - array_q (np.array): array 3D del cuadrante.
        - canal (int): numero de cuadrante del canal.

    RETURN:
        - int: promedio del canal en el cuadrante.
    """
    return sum([array_q[offset_i, offset_j, canal] for offset_i in range(0,3) for offset_j in range(0,3)]) // 9


def kuwahara(array_im: np.array) -> np.array:
    """
    Recibe un array 3D correspondiente con una imagen, y devuelve otro array 3D
    correspondiente con el filtro kuwahara aplicado en dicha imagen.

    PARAMETRO:
        - array_im (np.array): array 3D de la imagen.
    
    RETURN:
        - (np.array): array 3D de la imagen habiendole aplicado el filtro kuwahara.
    """
    height,width,_ = array_im.shape
    array_im_copy = array_im.copy()

    for i in range(2,height-2):
        for j in range(2,width-2):
            var_qA, qA = calcular_varianza_3x3(array_im, i-2, j-2)  
            var_qB, qB = calcular_varianza_3x3(array_im, i-2, j)    
            var_qC, qC = calcular_varianza_3x3(array_im, i, j-2)
            var_qD, qD = calcular_varianza_3x3(array_im, i, j)
            cuadrantes = [qA, qB, qC, qD]
            varianzas = [var_qA, var_qB, var_qC, var_qD]
            min_varianzas = min(varianzas)
            indice = varianzas.index(min_varianzas)

            q_seleccionado = cuadrantes[indice]
            nuevo_pixel = [promedio_color(q_seleccionado, 0), promedio_color(q_seleccionado, 1), promedio_color(q_seleccionado, 2)]
            array_im_copy[i,j,:] = nuevo_pixel
    
    return array_im_copy[2:height-2, 2:width-2, :] #sin pad :)


def main():
    print("≡≡Encriptador≡≡")
    path_entrada = input("Ingrese nombre de la imagen a utilizar como base: ")
    mensaje = input("Ingrese el mensaje a esconder: ")
    path_salida = input("Ingrese nombre del archivo de salida: ")

    im = Image.open(path_entrada)
    array_im = np.array(im)
    array_im = padding(array_im)
    array_im = kuwahara(array_im)
    seq = string_a_seq(mensaje)
    im_encriptada = seq_a_imagen(seq, array_im)
    im_encriptada.save(path_salida)

if __name__ == "__main__":
    main()