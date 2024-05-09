from PIL import Image
import numpy as np

TABLA_CHARS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ".", ",", "?", "!", "¿", "¡", "(", ")", ":", ";", "-", '"', "'", "á", "é", "í", "ó", "ú", "ü", "ñ"]

def char_a_num(c : str) -> int:
    return TABLA_CHARS.index(c) + 1

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

#calcular vari            
def calcular_varianza(array, i,j):
    varianzas = []

    sup_izq = array[i,j,:]
    sup_der = array[i,j+1,:]
    inf_izq = array[i+1,j,:]
    inf_der = array[i+1,j+1,:]
    for canal in range(0,3):
        chek_vari = np.var([sup_izq[canal], sup_der[canal], inf_izq[canal]])
        varianzas.append(chek_vari)
    return varianzas, sup_izq, sup_der, inf_izq, inf_der

#encript:
def valor_a_cuadrante(valor, array, i,j):
    
    varianzas, sup_izq, sup_der, inf_izq, inf_der = valor_a_cuadrante(array, i, j)

    min_varianzas = min(varianzas)
    modificar_x_canal = varianzas.index(min_varianzas)
    promedio_menor_var = sum([sup_izq[modificar_x_canal], sup_der[modificar_x_canal], inf_izq[modificar_x_canal]]) / 3
    reemplazar_canal = (promedio_menor_var + valor) % 256
    
    inf_der[modificar_x_canal] = reemplazar_canal

def seq_a_imagen(seq, im_in):
    width,height = im_in.size
    array_im = np.array(im_in)

    contador = 0
    for i in range(0,height,2):
        for j in range(0,width,2):
            valor_a_cuadrante(seq[contador], array_im, i, j)
            
            contador += 1
            if contador >= len(seq):
                im_out = Image.fromarray(array_im)
                return im_out
            
#padding
def padding(array_im):
    pad = np.pad(array_im,((2,2),(2,2),(0,0)),mode = 'edge')
    return pad

#aplicar filtro
def kuwahara(array_im):
    im_padded = padding(array_im)

def main():
    pass

main()