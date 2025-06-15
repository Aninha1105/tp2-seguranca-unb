# Parte 2: Modo de Operação ECB com S-AES
from p1 import *
from lib import *

def encrypt_saes_ecb(text, key):
    # Padding para manter pares de caracteres
    if len(text) % 2:
        text += '\0'

    ciphertext_list = []
    print("=" * 70)
    print("SETUP")
    print(f"Chave (Hex): {key:04X}")
    print(f"Mensagem Original: {text}")
    print("=" * 70 + "\n")

    b = 1
    for i in range(0,len(text),2):
        print(f"Bloco {b}")
        b+=1

        block = text[i:i+2]
        block_bin = (ord(block[0]) << 8 | ord(block[1]))
        ciphertext = Saes(block_bin, key)
        ciphertext_list.append(ciphertext)
        print("-" * 70)

    
    bin_str = ''.join(f"{mtxToBin(block)}" for block in ciphertext_list)
    hex_out = f"{int(bin_str, 2):04X}"
    b64_out = binToBase64(bin_str)

    print(f"\n--- Saída Final ---")
    print(f"Ciphertext (HEX): {hex_out}")
    print(f"Ciphertext (Base64): {b64_out}")
    print("=" * 70)

if __name__ == "__main__":
    text = "Bom dia!"
    key = 0xA73B

    encrypt_saes_ecb(text, key)