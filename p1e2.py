# Parte 1: Implementação do S-AES

# Tabela fixa de substituição (S-Box) para S-AES
S_BOX = {
    0x0: 0x9,  0x1: 0x4,  0x2: 0xA,  0x3: 0xB,
    0x4: 0xD,  0x5: 0x1,  0x6: 0x8,  0x7: 0x5,
    0x8: 0x6,  0x9: 0x2,  0xA: 0x0,  0xB: 0x3,
    0xC: 0xC,  0xD: 0xE,  0xE: 0xF,  0xF: 0x7
}

def AddRoundKey():
    pass

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
    for i in range(4):      # Até 4 bits, pois estamos em GF(2^4)
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
    s11 = GFMult(0x4, state[0][1]) ^ GFMult(0x4, state[1][1])
    return [[s00, s01], [s10, s11]] 

def KeyExpansion():
    pass

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
    after_mix = MixColumns(after_shift)
    print(f"Após MixColumns: {after_mix}")

    return 

# Parte 2: Modo de Operação ECB com S-AES

def EncryptSaesEcb():
    pass


Saes()