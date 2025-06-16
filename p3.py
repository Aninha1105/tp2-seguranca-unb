# Parte 3: AES real com biblioteca
import time     # Importa módulo para medir tempo de execução.
import base64   # Importa módulo para codificação e decodificação em Base64.
import os       # Importa módulo para geração de números aleatórios.
import math     # Importa funções matemáticas para cálculo de entropia.
from collections import Counter     # Importa Counter para cálculo de entropia.
from cryptography.hazmat.primitives import padding      # Importa utilitários de padding.
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes    # Importa classes para criação de cifras AES e modos de operação.
from cryptography.hazmat.backends import default_backend    # Importa backend padrão para operações criptográficas.

# Geração de chave aleatória de 128 bits e mensagem de exemplo
key = os.urandom(16)
txt = b"ok"

def shannon_entropy(data: bytes) -> float:
    # brief Calcula a entropia de Shannon de uma sequência de bytes.
    # param data: bytes de entrada para avaliação de imprevisibilidade.
    # return float representando a entropia média em bits por byte.

    counts = Counter(data)
    lenght = len(data)
    return -sum((cnt/lenght) * math.log2(cnt/lenght) for cnt in counts.values())

def run_aes(k: bytes, data: bytes, mode: str) -> dict:
    # brief Executa a cifragem AES em um determinado modo.
    # param k: bytes de 16 bytes da chave AES.
    # param data: bytes da mensagem clara.
    # param mode: string indicando o modo de operação ("ECB", "CBC", "CFB", "OFB", "CTR").
    # return dicionário com campos:
    #   - "b64": ciphertext codificado em Base64.
    #   - "iv_nonce_hex": hex da IV ou nonce, ou "N/A" se não se aplica.
    #   - "bytes": bytes do IV+ciphertext ou apenas ciphertext.

    #  Aplica padding PKCS7 para modos que exigem múltiplos de 128 bits
    if mode in ["ECB", "CBC"]:
        padder = padding.PKCS7(128).padder()
        pt = padder.update(data) + padder.finalize()
    else:
        pt = data

    iv_nonce = None

    # Seleção do modo de operação e criação do encryptor
    if mode == "ECB":
        cipher = Cipher(algorithms.AES(k), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
    elif mode == "CBC":
        iv_nonce = os.urandom(16)
        cipher = Cipher(algorithms.AES(k), modes.CBC(iv_nonce), backend=default_backend())
        encryptor = cipher.encryptor()
    elif mode == "CFB":
        iv_nonce = os.urandom(16)
        cipher = Cipher(algorithms.AES(k), modes.CFB(iv_nonce), backend=default_backend())
        encryptor = cipher.encryptor()
    elif mode == "OFB":
        iv_nonce = os.urandom(16)
        cipher = Cipher(algorithms.AES(k), modes.OFB(iv_nonce), backend=default_backend())
        encryptor = cipher.encryptor()
    elif mode == "CTR":
        iv_nonce = os.urandom(16)
        cipher = Cipher(algorithms.AES(k), modes.CTR(iv_nonce), backend=default_backend())
        encryptor = cipher.encryptor()
    
    # Realiza a cifragem e concatena IV/nonce se existir
    ct = encryptor.update(pt) + encryptor.finalize()
    res = (iv_nonce + ct) if iv_nonce else ct

    return {
        "b64": base64.b64encode(res).decode('utf-8'),
        "iv_nonce_hex": iv_nonce.hex() if iv_nonce else "N/A",
        "bytes": res
    }


print("=" * 70)
print("SETUP")
print(f"Chave (Hex): {key.hex().upper()}")
print(f"Mensagem Original: {txt.decode('utf-8')}")
print("=" * 70)

time_result = {}    # Armazena tempo de execução por modo
entropies = {}      # Armazena entropia de Shannon por modo

aes_modes = ["ECB", "CBC", "CFB", "OFB", "CTR"]

# Loop pelos modos de operação para cifrar, medir tempo e calcular entropia
for mode in aes_modes:
    print(f"\n--- MODO {mode} ---")

    begin = time.perf_counter()
    res = run_aes(key, txt, mode)
    end = time.perf_counter()

    # Cálculo de tempo em milissegundos
    calc_time = (end-begin)*1000 
    time_result[mode] = calc_time

    # Cálculo de entropia de Shannon
    ent = shannon_entropy(res["bytes"])
    entropies[mode] = ent
    
    print(f"IV/Nonce (Hex): {res['iv_nonce_hex'].upper()}")
    print(f"Texto Cifrado (Base64): {res['b64']}")
    print(f"Tempo de Execução: {calc_time:.6f} ms")
    print(f"Grau de Aleatoriedade (Entropia de Shannon): {ent:.4f} bits/byte")
    print("-" * 70)    

# Impressão de resumo de desempenho e entropia ordenados
print("\n\n--- DESEMPENHO ---")
for mode_name, t in sorted(time_result.items(), key=lambda item:item[1]):
    print(f"Modo {mode_name:<5}: {t:.6f} ms")

print("\n--- ALEATORIEDADE (Entropia de Shannon) ---")
for mode_name, e in sorted(entropies.items(), key=lambda item:item[1]):
    print(f"Modo {mode_name:<5}: {e:.4f} bits/byte")

print("=" * 70)