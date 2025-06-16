# Parte 3: AES real com biblioteca
import time
import base64
import os
import math
from collections import Counter
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

key = os.urandom(16)
txt = b"ok"

def shannon_entropy(data: bytes) -> float:
    counts = Counter(data)
    lenght = len(data)
    return -sum((cnt/lenght) * math.log2(cnt/lenght) for cnt in counts.values())

def run_aes(k: bytes, data: bytes, mode: str) -> dict:

    # aplica padding (ECB e CBC exigem, CFB, OFB, CTR não exigem). 
    if mode in ["ECB", "CBC"]:
        padder = padding.PKCS7(128).padder()
        pt = padder.update(data) + padder.finalize()
    else:
        pt = data

    iv_nonce = None

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

time_result = {}
entropies = {}

aes_modes = ["ECB", "CBC", "CFB", "OFB", "CTR"]

for mode in aes_modes:
    print(f"\n--- MODO {mode} ---")

    begin = time.perf_counter()
    res = run_aes(key, txt, mode)
    end = time.perf_counter()

    calc_time = (end-begin)*1000 # ms
    time_result[mode] = calc_time

    ent = shannon_entropy(res["bytes"])
    entropies[mode] = ent
    
    print(f"IV/Nonce (Hex): {res['iv_nonce_hex'].upper()}")
    print(f"Texto Cifrado (Base64): {res['b64']}")
    print(f"Tempo de Execução: {calc_time:.6f} ms")
    print("-" * 70)    

print("\n\n--- DESEMPENHO ---")
for mode_name, t in sorted(time_result.items(), key=lambda item:item[1]):
    print(f"Modo {mode_name:<5}: {t:.6f} ms")

print("\n--- ALEATORIEDADE (Entropia) ---")
for mode_name, e in sorted(entropies.items(), key=lambda item:item[1]):
    print(f"Modo {mode_name:<5}: {e:.4f} bits/byte")

print("=" * 70)