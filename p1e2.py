from lib import *

# Parte 1: Implementação do S-AES

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
    # Realiza a rotação da linha do S-AES.
    # Linha 0: sem alteração
    # Linha 1: rotação circular à esquerda
    a, b = state[1]
    state[1] = [b, a]
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
    s00 = GFMult(0x1, state[0][0]) ^ GFMult(0x4, state[1][0])
    s10 = GFMult(0x4, state[0][0]) ^ GFMult(0x1, state[1][0])
    s01 = GFMult(0x1, state[0][1]) ^ GFMult(0x4, state[1][1])
    s11 = GFMult(0x4, state[0][1]) ^ GFMult(0x1, state[1][1])
    return [[s00, s01], [s10, s11]]

def KeyExpansion(init):

    def SubWord(word):
        n1 = (word>>4) & 0xF
        n2 = word & 0xF
        
        s_n1 = S_BOX[n1]
        s_n2 = S_BOX[n2]

        return (s_n1<<4) | s_n2
    
    def Rotate(word):
        return ((word & 0xF)<<4) | ((word>>4) & 0xF)
    
    w0 = (init[0][0]<<4) | init[1][0]
    w1 = (init[0][1]<<4) | init[1][1]

    # w2 = w0^Rcon1^rotate(w1)
    w2 = w0^RCON1^SubWord(Rotate(w1))
    w3 = w2^w1

    # w4 = w2^Rcon2^rotate(w3)
    w4 = w2^RCON2^SubWord(Rotate(w3))
    w5 = w4^w3

    k1 = [[(w2>>4) & 0xF, (w3>>4) & 0xF], [w2 & 0xF, w3 & 0xF]]
    k2 = [[(w4>>4) & 0xF, (w5>>4) & 0xF], [w4 & 0xF, w5 & 0xF]]

    return init, k1, k2

def Saes():
    # Estado inicial: "ok" em ascii -> 0x6F 0x6B -> nibbles [[6, 15], [6, 11]]
    initial_state = [[0x6, 0xF], [0x6, 0xB]]
    print(f"Estado inicial: {initial_state}")

    # SubNibbles
    after_sub = SubNibbles(initial_state)
    print(f"Após SubNibbles: {after_sub}")

    # ShiftRows
    after_shift = ShiftRows(after_sub)
    print(f"Após ShiftRows: {after_shift}")

    # MixColumns
    test_mix = [[0x2,0xE], [0xE, 0xE]]
    after_mix = MixColumns(test_mix)
    print(f"Após MixColumns: {after_mix}")

    # AddRoundKey
    # key = 1010 0111 0011 1011 -> 0xA 0x7 0x3 0xB -> nibbles [[10, 7], [3, 11]]
    key = [[0xA, 0x7], [0x3, 0xB]]
    after_xor = AddRoundKey(after_mix, key)
    print(f"Após AddRoundKey: {after_xor}")

    #after_expand = KeyExpansion(key)

    # testes 
    init_key = [[0xA, 0x7], [0x3, 0xB]]  #1010 0111 0011 1011
    k0, k1, k2 = KeyExpansion(init_key)
    print("K0:", k0)
    print("K1:", k1)
    print("K2:", k2)
    
    #testes aux
    b = mtxToBin(init_key)
    print(b)
    print(binToBase64(b)) #o3s

    return

# Parte 2: Modo de Operação ECB com S-AES

def EncryptSaesEcb():
    pass


Saes()

