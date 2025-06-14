# Parte 2: Modo de Operação ECB com S-AES
from p1 import *
from lib import *

def encrypt_saes_ecb(text, key):
    # Padding para manter pares de caracteres
    if len(text) % 2:
        text += '\0'

    ciphertext_list = []
    print(f"Inicial text: {text}")

    for i in range(0,len(text),2):
        block = text[i:i+2]
        block_bin = (ord(block[0]) << 8 | ord(block[1]))
        ciphertext = Saes(block_bin, key)
        ciphertext_list.append(ciphertext)

    
    bin_str = ''.join(f"{mtxToBin(block)}" for block in ciphertext_list)
    hex_out = f"{int(bin_str, 2):04X}"
    b64_out = binToBase64(bin_str)

    print(f"\nCiphertext (HEX): {hex_out}")
    print(f"Ciphertext (Base64): {b64_out}")
    

if __name__ == "__main__":
    text = "Bom dia!"
    key = 0xA73B

    encrypt_saes_ecb(text, key)