from PIL import Image
import numpy as np
"""
Bloques esenciales:
-Convertidor Char a Num --> LISTO
-Convertidor Num a Char --> LISTO
-Aplicador Kuwahara
-Encodeador de mensajes ocultos
    - Transformar mensaje a secuencia --> LISTO
    - Poner secuencia en una imagen --> LISTO (optimizar)
-Desencodeador de mensajes ocultos
    - Sacar secuencia de una imagen --> LISTO (optimizar)
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
-El resultado es la imagen con filtro y mensaje (SIN EL PADDING!! se usa solo para aplicar kuahara)

Desencriptación:
-Inversos del otro (del encripción)
"""
TABLA_CHARS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ".", ",", "?", "!", "¿", "¡", "(", ")", ":", ";", "-", '"', "'", "á", "é", "í", "ó", "ú", "ü", "ñ"]

#func individuales:
def num_a_char(n : int) -> str:
    return TABLA_CHARS[n-1]

def char_a_num(c : str) -> int:
    return TABLA_CHARS.index(c) + 1

#func traducciones:
def string_a_seq(s : str) -> list:
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

def seq_a_string(seq : list) -> str:
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


########################################## codigos principales ##############################################################

#encript:
def seq_a_imagen():
    im = Image.open("imagen.jpeg")
    width,height = im.size
    array_im = np.array(im)
    # array[num_fila,num_col,CANAL] # NUM_CANAL: rojo = 0, verde = 1, azul = 2

    seq = string_a_seq()

    contador = 0
    for i in range(0,height,2):
        for j in range(0,width,2):
            
            varianzas = []
            sup_izq = array_im[i,j,:]
            sup_der = array_im[i,j+1,:]
            inf_izq = array_im[i+1,j,:]
            inf_der = array_im[i+1,j+1,:]

            for canal in (0,3):
                chek_vari = np.var[sup_der[canal],sup_izq[canal], inf_izq[canal]]
                varianzas.append(chek_vari)

            min_varianzas = min(varianzas)
            modificar_x_canal = varianzas.index(min_varianzas)
            promedio_menor_var = sum([sup_izq[modificar_x_canal], sup_der[modificar_x_canal], inf_izq[modificar_x_canal]]) / 3
            reemplazar_canal = (promedio_menor_var + seq[contador]) % 256
            
            inf_der[modificar_x_canal] = reemplazar_canal
            
            contador += 1
            if contador >= len(seq):
                im = Image.fromarray(array_im)
                im.save("your_file.jpeg")
                return

#padding
def padding(array_im):
    pad = np.pad(array_im,((2,2),(2,2),(0,0)),mode = 'edge')
    return pad

#aplicar filtro
def kuwahara(array_im):
    im_padded = padding(array_im)

#desencript:
def imagen_a_seq():
    im_encript = Image.open("your_file.jpeg")
    width,height = im_encript.size
    array_im = np.array(im_encript)

    seq = string_a_seq()

    for i in range(0,height,2):
        for j in range(0,width,2):
            
            seq = []
        
            varianzas = []
            sup_izq = array_im[i,j,:]
            sup_der = array_im[i,j+1,:]
            inf_izq = array_im[i+1,j,:]
            inf_der = array_im[i+1,j+1,:]

            for canal in (0,3):
                chek_vari = np.var[sup_der[canal],sup_izq[canal], inf_izq[canal]]
                varianzas.append(chek_vari)
                
            min_varianzas = min(varianzas)
            canal_encript = varianzas.index(min_varianzas)

            promedio_menor_var = sum([sup_izq[canal_encript], sup_der[canal_encript], inf_izq[canal_encript]]) / 3
            extraer_valor = (inf_der[canal_encript] - promedio_menor_var) % 256
            seq.append(extraer_valor)

            return seq
            