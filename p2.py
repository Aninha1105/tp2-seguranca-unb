# Parte 2: Modo de Operação ECB com S-AES
from p1 import *    # Importa Saes e demais funções do Módulo Parte 1
from lib import *   # Importa utilitários de conversão e saída

def encrypt_saes_ecb(text, key):
    # brief Cifra a mensagem em modo ECB utilizando S-AES por bloco de 2 bytes.
    # param text: string da mensagem (pode conter padding '\0').
    # param key: inteiro 16-bit da chave.
    # return None.

    # Aplica padding nulo se número de caracteres for ímpar
    if len(text) % 2:
        text += '\0'

    ciphertext_list = []
    print("=" * 70)
    print("SETUP")
    print(f"Chave (Hex): {key:04X}")
    print(f"Mensagem Original: {text}")
    print("=" * 70 + "\n")

    b_idx = 1
    # Processa cada bloco de 2 caracteres
    for i in range(0,len(text),2):
        print(f"Bloco {b_idx}")
        b_idx+=1
        block = text[i:i+2]
        # Converte os 2 caracteres em um valor inteiro de 16 bits
        block_bin = (ord(block[0]) << 8 | ord(block[1]))
        # Cifra o bloco usando S-AES
        ciphertext = Saes(block_bin, key)
        ciphertext_list.append(ciphertext)
        print("-" * 70)

    # Concatena todos os blocos cifrados em uma string binária
    bin_str = ''.join(f"{mtxToBin(block)}" for block in ciphertext_list)
    # Converte binário concatenado para hexadecimal e Base64
    hex_out = f"{int(bin_str, 2):04X}"
    b64_out = binToBase64(bin_str)

    print(f"\n--- Saída Final ---")
    print(f"Ciphertext (HEX): {hex_out}")
    print(f"Ciphertext (Base64): {b64_out}")
    print("=" * 70)

if __name__ == "__main__":
    text = "Bom dia!"
    key = 0xA73B

    encrypt_saes_ecb(text, key) # Executa criptografia ECB com S-AES