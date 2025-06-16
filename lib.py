import base64

def mtxToBin(m):
    # brief Converte uma matriz 2x2 de nibbles em string binária.
    # param m: matriz 2x2 de nibbles (lista de listas) com valores de 0x0 a 0xF.
    # return string contendo 16 bits correspondentes aos quatro nibbles concatenados.

    nbs = [m[0][0],m[0][1],m[1][0],m[1][1]]
    return ''.join(f'{nb:04b}' for nb in nbs)

def binToBase64(b):
    # brief Converte uma string binária em codificação Base64.
    # param b: string de bits.
    # return string em Base64 representando os bytes correspondentes aos bits fornecidos.

    bd = int(b, 2).to_bytes((len(b)+7)//8, byteorder='big')
    b64 = base64.b64encode(bd).decode('ascii')
    return b64

def WordToMtx(high, low):
    # brief Converte dois bytes (alta e baixa ordem) em matriz 2x2 de nibbles.
    # param high: byte de alta ordem (0 a 255).
    # param low: byte de baixa ordem (0 a 255).
    # return Matriz 2x2 de nibbles extraídos de cada byte.

    return [[(high & 0xF0) >> 4, high & 0x0F], [(low & 0xF0) >> 4, low & 0x0F]]

def MtxOut(label, state):
    # brief Exibe um estado (matriz 2x2) em formatos hexadecimal e Base64 com label.
    # param label: string de identificação para o output.
    # param state: matriz 2x2 de nibbles (valores 0x0–0xF).
    # return None.

    bin_str = mtxToBin(state)
    hex_out = f"{int(bin_str, 2):04X}"
    b64_out = binToBase64(bin_str)
    print(f"{label}HEX: {hex_out} | BASE64: {b64_out}")
    return