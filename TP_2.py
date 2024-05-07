"""
Bloques esenciales:
-Convertidor Char a Num --> LISTO
-Convertidor Num a Char --> LISTO
-Aplicador Kuwahara
-Encodeador de mensajes ocultos
    - Transformar mensaje a secuencia --> LISTO
    - Poner secuencia en una imagen
-Desencodeador de mensajes ocultos
    - Sacar secuencia de una imagen
    - Transformar secuencia a mensaje

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