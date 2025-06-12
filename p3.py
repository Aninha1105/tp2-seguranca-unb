# Parte 3: AES real com biblioteca
import time
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
txt = b"seila"

def run_aes(k, data, mode):

    cipher = AES.new(key, mode)

    if mode in [AES.MODE_ECB, AES.MODE_CBC]:
        to_cipher = pad(data, AES.block_size)
    else:
        to_cipher = data

    ct = cipher.encrypt(to_cipher)

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
    
    print(res)
    res_b64 = base64.b64encode(res).decode('utf-8')

    return {
        "b64": res_b64,
        "iv_ou_nonce_hex": iv_nonce.hex() if iv_nonce else "N/A"
    }

# ainda tem q organizar pra printar isso

print(run_aes(key, txt, AES.MODE_ECB))