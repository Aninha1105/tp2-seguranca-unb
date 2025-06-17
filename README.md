# Introdução

Este repositório apresenta uma implementação didática do algoritmo Simplified AES (S-AES) e uma demonstração da criptografia AES real utilizando a biblioteca [cryptography](https://cryptography.io/). O projeto está dividido em três partes:

1. **Parte 1**: Implementação do S-AES puro, incluindo geração de subchaves, substituição de nibbles (S-Box), mistura de colunas e adição de chave.
2. **Parte 2**: Aplicação do modo de operação ECB para o S-AES, cifrando blocos de 16 bits sequenciais e exibindo resultados em HEX e Base64.
3. **Parte 3**: Demonstração do AES real em diversos modos de operação (ECB, CBC, CFB, OFB, CTR) usando a biblioteca `cryptography`, com análise de desempenho e entropia de Shannon.

# Requisitos

- Python 3.7 ou superior
- Biblioteca `cryptography` (instalação via `pip install cryptography`)
- Módulos padrão: `base64`, `timeit`, `os`, `math`, `collections`

# Como executar

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/Aninha1105/tp2-seguranca-unb.git
   cd tp2-seguranca-unb/
   ```

2. **Crie e ative um ambiente virtual** (para isolar dependências):

   - No Unix/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - No Windows (cmd):
     ```bat
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Parte 1 – S-AES**:

   ```bash
   python p1.py
   ```

5. **Parte 2 – Modo ECB com S-AES**:

   ```bash
   python p2.py
   ```

6. **Parte 3 – AES real com biblioteca**:

   ```bash
   python p3.py
   ```

Cada script imprimirá no console o processo de criptografia, resultados intermediários e finais (HEX, Base64), além de métricas de desempenho e entropia (no caso da Parte 3).

# Conclusão

Este repositório serve como material de estudo para compreender o funcionamento interno do algoritmo Simplified AES e experimentar o uso do AES real em diferentes modos de operação. A análise de entropia e desempenho auxilia na comparação prática entre os modos de cifragem e demonstra como a criptografia simétrica é aplicada em cenários do mundo real.