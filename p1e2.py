# Parte 1: Implementação do S-AES

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

def ShiftRows():
    pass

def MixColumns():
    pass

def KeyExpansion():
    pass

def Saes():
    # Estado inicial: "Oi" em ascii -> 0x4F 0x69 -> nibbles [[4, 15], [6, 9]]
    initial_state = [[0x4, 0xF], [0x6, 0x9]]
    print(f"Estado inicial: {initial_state}")

    # SubNibbles
    after_sub = SubNibbles(initial_state)
    print(f"Após SubNibbles: {after_sub}")

    return 

# Parte 2: Modo de Operação ECB com S-AES

def EncryptSaesEcb():
    pass


Saes()