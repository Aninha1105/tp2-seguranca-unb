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


def MixColumns():
    pass

def KeyExpansion():
    pass

def Saes():
    # Estado inicial: "ok" em ascii -> 0x6F 0x6B -> nibbles [[6, 15], [6, 11]]
    initial_state = [[0x6, 0xF], [0x6, 0xB]]
    print(f"Estado inicial: {initial_state}")

    # SubNibbles
    after_sub = SubNibbles(initial_state)
    print(f"Após SubNibbles: {after_sub}")

    #ShiftRows
    after_shift = ShiftRows(after_sub)
    print(f"Após ShiftRows: {after_shift}")

    return 

# Parte 2: Modo de Operação ECB com S-AES

def EncryptSaesEcb():
    pass


Saes()