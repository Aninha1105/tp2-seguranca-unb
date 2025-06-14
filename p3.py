# Parte 3: AES real com biblioteca
import time
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
txt = b"ok"

def run_aes(k, data, mode):

    # instância da cifra (usa vi e nonce aleatório da biblioteca).
    cipher = AES.new(k, mode)

    # aplica padding (ECB e CBC exigem, CFB, OFB, CTR não exigem). 
    if mode in [AES.MODE_ECB, AES.MODE_CBC]:
        pt = pad(data, AES.block_size)
    else:
        pt = data

    ct = cipher.encrypt(pt)

    iv_nonce = None
    res = None

    if mode == AES.MODE_ECB:
        res = ct
    elif mode == AES.MODE_CTR:
        iv_nonce = cipher.nonce
        res = cipher.nonce + ct
    else:
        iv_nonce = cipher.iv
        res = cipher.iv + ct
    
    res_b64 = base64.b64encode(res).decode('utf-8')

    return {
        "b64": res_b64,
        "iv_nonce_hex": iv_nonce.hex() if iv_nonce else "N/A"
    }


print("=" * 70)
print("SETUP")
print(f"Chave (Hex): {key.hex().upper()}")
print(f"Mensagem Original: {txt.decode('utf-8')}")
print("=" * 70)

time_result = {}

aes_modes = [
    ("ECB", AES.MODE_ECB),
    ("CBC", AES.MODE_CBC),
    ("CFB", AES.MODE_CFB),
    ("OFB", AES.MODE_OFB),
    ("CTR", AES.MODE_CTR)
]

for mode_name, param in aes_modes:
    print(f"\n--- MODO {mode_name} ---")

    begin = time.perf_counter()
    res = run_aes(key, txt, param)
    end = time.perf_counter()

    calc_time = (end-begin)*1000 # ms
    time_result[mode_name] = calc_time
    
    print(f"IV/Nonce (Hex): {res['iv_nonce_hex'].upper()}")
    print(f"Texto Cifrado (Base64): {res['b64']}")
    print(f"Tempo de Execução: {calc_time:.6f} ms")
    print("-" * 70)    

print("\n\n--- DESEMPENHO ---")
for mode_name, t in sorted(time_result.items(), key=lambda item:item[1]):
    print(f"Modo {mode_name:<5}: {t:.6f} ms")
print("=" * 70)