# Parte 1: Implementação do S-AES
from lib import *

# Tabela fixa de substituição (S-Box) para S-AES
S_BOX = {
    0x0: 0x9,  0x1: 0x4,  0x2: 0xA,  0x3: 0xB,
    0x4: 0xD,  0x5: 0x1,  0x6: 0x8,  0x7: 0x5,
    0x8: 0x6,  0x9: 0x2,  0xA: 0x0,  0xB: 0x3,
    0xC: 0xC,  0xD: 0xE,  0xE: 0xF,  0xF: 0x7
}

RCON1 = 0x80 # 1000 0000
RCON2 = 0x30 # 0011 0000

def AddRoundKey(state, key):
    # Realiza a operação XOR entre o estado e a subchave
    new_state = []
    for i in range(2):
        new_row = []
        for j in range(2):
            xor = state[i][j] ^ key[i][j]
            new_row.append(xor)
        new_state.append(new_row)
    return new_state

def SubNibbles(state):
    # Aplica a substituição de nibble via S-Box em cada elemento do estado
    new_state = []
    for row_idx, row in enumerate(state):
        new_row = []
        for col_idx, nibble in enumerate(row):
            substituted = S_BOX[nibble]
            new_row.append(substituted)
        new_state.append(new_row)  
    return new_state

def ShiftRows(state):
    # Realiza a rotação do 2 e 4 nibble do S-AES.
    a = state[0][1]
    b = state[1][1]
    state[0][1] = b
    state[1][1] = a
    return state

def GFMult(a, b):
    # Multiplica dois polinômios a e b no corpo GF(16), com redução por x^4 + x + 1 (0x13 = 0b10011).
    result = 0
    for i in range(4):      # Até 4 bits, pois estamos em GF(16 = 2^4)
        if b & 1:           # Se o bit menos significativo de 'b' é 1
            result ^= a     # Soma (XOR) o valor atual de 'a' no 'result'
        carry = a & 0x8     # Verifica se o bit mais alto (x^3) vai transbordar
        a <<= 1             # Desloca 'a' para esquerda (multiplica por 2)
        if carry:           # Se passou de grau 4, reduz com o polinômio irreduzível
            a ^= 0b10011
        a &= 0xF            # Garante que a continue com no máximo 4 bits
        b >>= 1             # Desloca 'b' para direita (divide por 2)
    return result & 0xF     # Resultado final limitado a 4 bits

def MixColumns(state):
    # Aplica a transformação MixColumns em uma matriz 2x2 no GF(16)
    s00 = GFMult(0x1, state[0][0]) ^ GFMult(0x4, state[0][1])
    s10 = GFMult(0x4, state[0][0]) ^ GFMult(0x1, state[0][1])
    s01 = GFMult(0x1, state[1][0]) ^ GFMult(0x4, state[1][1])
    s11 = GFMult(0x4, state[1][0]) ^ GFMult(0x1, state[1][1])
    return [[s00, s10], [s01, s11]]

def KeyExpansion(init):

    def SubWord(word):
        n1 = (word>>4) & 0xF
        n2 = word & 0xF
        
        s_n1 = S_BOX[n1]
        s_n2 = S_BOX[n2]

        return (s_n1<<4) | s_n2
    
    def Rotate(word):
        return ((word & 0xF)<<4) | ((word>>4) & 0xF)
    
    w0 = (init[0][0]<<4) | init[0][1]
    w1 = (init[1][0]<<4) | init[1][1]

    # w2 = w0^Rcon1^rotate(w1)
    w2 = w0^RCON1^SubWord(Rotate(w1))
    w3 = w2^w1

    # w4 = w2^Rcon2^rotate(w3)
    w4 = w2^RCON2^SubWord(Rotate(w3))
    w5 = w4^w3

    k1 = [[(w2>>4) & 0xF, w2 & 0xF], [(w3>>4) & 0xF, w3 & 0xF]]
    k2 = [[(w4>>4) & 0xF, w4 & 0xF], [(w5>>4) & 0xF, w5 & 0xF]]

    return init, k1, k2

def Saes(text, key):
    # Estado inicial 
    state = WordToMtx((text & 0xFF00) >> 8, text & 0x00FF)
    MtxOut("Inicial State: ", state)
    key = WordToMtx((key & 0xFF00) >> 8, key & 0x00FF)
    MtxOut("Key: ", key)

    # Key expansion
    k0, k1, k2 = KeyExpansion(key)
    print(f"\n--- After KeyExpansion ---")
    MtxOut("k0: ", k0)
    MtxOut("k1: ", k1)
    MtxOut("k2: ", k2)

    # Pré-rodada
    state = AddRoundKey(state, k0)
    MtxOut("\n--- After AddRoundKey(k0) ---\n", state)

    # Rodada 1
    print("\n--- Round 1 ---")
    state = SubNibbles(state)
    MtxOut("After SubNibbles: ", state)
    state = ShiftRows(state)
    MtxOut("After ShiftRows: ", state)
    state = MixColumns(state)
    MtxOut("After MixColumns: ", state)
    state = AddRoundKey(state, k1)
    MtxOut("After AddRoundKey(k1): ", state)

    # Rodada 2
    print("\n--- Round 2 ---")
    state = SubNibbles(state)
    MtxOut("After SubNibbles: ", state)
    state = ShiftRows(state)
    MtxOut("After ShiftRows: ", state)
    state = AddRoundKey(state, k2)
    MtxOut("After AddRoundKey(k2): ", state)

    ciphertext = state   
    return ciphertext

if __name__ == "__main__":
    text = 0x6F6B   # "ok" -> 0110 1111 0110 1011
    key = 0xA73B    # 1010 0111 0011 1011

    print("=" * 70)
    print("SETUP")
    print(f"Chave (Hex): {key}")
    print(f"Mensagem Original: ok")
    print("=" * 70)

    ciphertext = Saes(text, key)
    print(f"\n--- Saída Final ---")
    MtxOut("Ciphertext: ", ciphertext)
    print("=" * 70)
