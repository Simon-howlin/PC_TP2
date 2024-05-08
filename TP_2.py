from PIL import Image
import numpy as np
"""
Bloques esenciales:
-Convertidor Char a Num --> LISTO
-Convertidor Num a Char --> LISTO
-Aplicador Kuwahara
-Encodeador de mensajes ocultos
    - Transformar mensaje a secuencia --> LISTO
    - Poner secuencia en una imagen --> CASI LISTO
-Desencodeador de mensajes ocultos
    - Sacar secuencia de una imagen
    - Transformar secuencia a mensaje --> LISTO

Encriptación:
-Aplicar Kuwahara 
    -pasos (en la pag)
    -pasos (en la pag)
-Pasar a numeros
    -Poner -1 entre letras
    -Agregar un 0 (final)
-Modificar pixeles para encodear el mensaje
    -pasos (en la pag)
    -pasos (en la pag)
-El resultado es la imagen con filtro y mensaje

Desencriptación:
-Inversos del otro (del encripción)
"""
TABLA_CHARS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ".", ",", "?", "!", "¿", "¡", "(", ")", ":", ";", "-", '"', "'", "á", "é", "í", "ó", "ú", "ü", "ñ"]

def num_a_char(n):
    return TABLA_CHARS[n-1]

def char_a_num(c):
    return TABLA_CHARS.index(c) + 1

def string_a_seq(s):
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
       
#print(string_a_seq("Hola, ¿cómo estás?"))

def seq_a_string(seq):
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

#seq = [9, -1, 2, 6, -1, 2, 3, -1, 2, -1, 3, 10, -1, 3, 8, -1, 4, 3, -1, 4, -1, 5, 5, -1, 2, 4, -1, 2, 6, -1, 3, 8, -1, 6, -1, 2, 10, -1, 3, 1, -1, 5, 2, -1, 2, 10, -1, 4, 1, -1, 0]
#print(seq_a_string(seq))

def seq_en_imagen():
    im = Image.open("imagen.jpeg")
    width,height = im.size
    array = np.array(im)
    # array[num_fila,num_col,CANAL] # NUM_CANAL: rojo = 0, verde = 1, azul = 2

    secuencia = string_a_seq()

    for i in range(0,height,2):
        for j in range(0,width,2):
            varianzas = []
            contador = 0
            can_sup_izq = []
            can_sup_der = []
            can_inf_izq = []
            can_inf_der = []
            for canal in (0,3):
                sup_izq = array[i,j,canal]
                can_sup_izq.append(sup_izq[canal])
                sup_der = array[i,j+1,canal]
                can_sup_der.append(sup_der[canal])
                inf_izq = array[i+1,j,canal]
                can_inf_izq.append(inf_izq[canal])
                inf_der = array[i+1,j+1,canal]
                can_inf_der.append(inf_der[canal])

                chek_vari = np.var[sup_der[canal],sup_izq[canal], inf_izq[canal]]
                chek_vari.append(varianzas)

            min_varianzas = min(varianzas)
            modificar_x_canal = varianzas.index(min_varianzas)
            promedio_menor_var = sum(can_sup_izq[modificar_x_canal], can_sup_der[modificar_x_canal], can_inf_izq[modificar_x_canal], can_inf_der[modificar_x_canal]) / 3
            remplazar_canal = promedio_menor_var + secuencia[contador]
            
            canal_modificado = inf_der[modificar_x_canal] = remplazar_canal
            
            contador += 1
