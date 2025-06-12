import base64

def mtxToBin(m):
    nbs = [m[0][0],m[1][0],m[0][1],m[1][1]]
    return ''.join(f'{nb:04b}' for nb in nbs)

# vou por aqui as coisas que precisar de base64 pq se n o código vai ficar gigamenso

def binToBase64(b):
    bd = int(b, 2).to_bytes((len(b)+7)//8, byteorder='big')
    b64 = base64.b64encode(bd).decode('ascii')
    return b64