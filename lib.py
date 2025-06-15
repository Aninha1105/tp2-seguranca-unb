import base64

def mtxToBin(m):
    nbs = [m[0][0],m[0][1],m[1][0],m[1][1]]
    return ''.join(f'{nb:04b}' for nb in nbs)

def binToBase64(b):
    bd = int(b, 2).to_bytes((len(b)+7)//8, byteorder='big')
    b64 = base64.b64encode(bd).decode('ascii')
    return b64

def WordToMtx(high, low):
    return [[(high & 0xF0) >> 4, high & 0x0F], [(low & 0xF0) >> 4, low & 0x0F]]

def MtxOut(label, state):
    # Função para printar as saídas intermediárias em hexadecimal e base64
    bin_str = mtxToBin(state)
    hex_out = f"{int(bin_str, 2):04X}"
    b64_out = binToBase64(bin_str)
    print(f"{label}HEX: {hex_out} | BASE64: {b64_out}")
    return