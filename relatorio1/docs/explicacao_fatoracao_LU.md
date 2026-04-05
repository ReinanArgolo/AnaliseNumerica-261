# Fatoração LU - Explicação Completa

## 📋 O que é Fatoração LU?

A **Fatoração LU** é um método de decomposição de matrizes que decompõe uma matriz quadrada `A` em duas matrizes triangulares:
- **L**: matriz triangular **inferior** (Lower triangular)
- **U**: matriz triangular **superior** (Upper triangular)

A relação fundamental é:
$$A = L \times U$$

## 🔄 Vantagens da Fatoração LU

1. **Eficiência**: Uma vez decomposta, a mesma fatoração LU pode ser usada para resolver múltiplos sistemas com diferentes vetores `b`
2. **Reduz operações**: Decompor uma vez (custoO(n³)) permite resolver vários sistemas em O(n²)
3. **Estabilidade numérica**: Especialmente com pivotamento parcial
4. **Implementação clara**: A decomposição segue a eliminação de Gauss

## 🧮 O Algoritmo - Passo a Passo

### Etapa 1: Decomposição LU (Eliminação de Gauss modificada)

Para cada coluna `k = 0, 1, ..., n-2`:

```
Para cada linha i = k+1, ..., n-1:
    multiplicador = U[i][k] / U[k][k]
    
    L[i][k] = multiplicador  ← Armazenar multiplicador em L
    
    Para cada coluna j = k, ..., n-1:
        U[i][j] -= multiplicador × U[k][j]  ← Anular elemento
```

**Exemplo com matriz 3×3:**

```
Matriz A original:
   4    3   -2
   8    5   -1
  -2    5    7

Passo 1 (k=0): Usar linha 0 como pivô
  L[1][0] = 8/4 = 2
  L[2][0] = -2/4 = -0.5
  
  U[1] = [8,5,-1] - 2×[4,3,-2]    = [0,-1,3]
  U[2] = [-2,5,7] - (-0.5)×[4,3,-2] = [0,6.5,6]

Passo 2 (k=1): Usar linha 1 como pivô
  L[2][1] = 6.5/(-1) = -6.5
  
  U[2] = [0,6.5,6] - (-6.5)×[0,-1,3] = [0,0,25.5]

Resultado:
L = [1,    0,   0  ]    U = [4,   3,    -2]
    [2,    1,   0  ]        [0,  -1,     3]
    [-0.5, -6.5, 1]        [0,   0,  25.5]
```

### Etapa 2: Substituição Progressiva (Resolver Ly = b)

Como L é triangular inferior, resolve-se de cima para baixo:

```
Para i = 0, 1, ..., n-1:
    soma = 0
    Para j = 0, ..., i-1:
        soma += L[i][j] × y[j]
    
    y[i] = (b[i] - soma) / L[i][i]
```

**Exemplo:**
```
L × y = b

[1,    0,   0  ]   [y0]   [11 ]
[2,    1,   0  ] × [y1] = [19 ]
[-0.5, -6.5, 1]   [y2]   [8  ]

y[0] = 11/1 = 11
y[1] = (19 - 2×11)/1 = -3
y[2] = (8 - (-0.5)×11 - (-6.5)×(-3))/1 = (8 + 5.5 - 19.5)/1 = -6
```

### Etapa 3: Substituição Regressiva (Resolver Ux = y)

Como U é triangular superior, resolve-se de baixo para cima:

```
Para i = n-1, n-2, ..., 0:
    soma = 0
    Para j = i+1, ..., n-1:
        soma += U[i][j] × x[j]
    
    x[i] = (y[i] - soma) / U[i][i]
```

**Exemplo:**
```
U × x = y

[4,   3,    -2]   [x0]   [11 ]
[0,  -1,     3] × [x1] = [-3 ]
[0,   0,  25.5]   [x2]   [-6 ]

x[2] = -6/25.5 = -0.2353
x[1] = (-3 - 3×(-0.2353))/(-1) = 2.2941
x[0] = (11 - 3×2.2941 - (-2)×(-0.2353))/4 = 0.9118
```

## 📊 Estrutura do Histórico

A função retorna um histórico detalhado com informações sobre cada operação:

```python
{
    "iter": 0,                          # Número da iteração
    "fase": "fatoracao_LU",             # Fase do algoritmo
    "k": 0,                             # Índice de coluna (para fatoração)
    "linha_pivo": 0,                    # Índice da linha pivô
    "linha_alvo": 1,                    # Índice da linha sendo modificada
    "pivo": 4.0,                        # Valor do pivô
    "multiplicador": 2.0,               # Multiplicador usado
    "acao": "armazenar_multiplicador_L_e_anular_U"  # Descrição da ação
}
```

## 🔢 Complexidade Computacional

- **Decomposição LU**: O(n³) operações
- **Substituição Progressiva**: O(n²) operações
- **Substituição Regressiva**: O(n²) operações
- **Total para um sistema**: O(n³)
- **Para k sistemas (mesmo A)**: O(n³) + k×O(n²) ≈ O(n³)

## ✅ Verificação: A = L × U

Para a matriz do exemplo:

```
L × U = [1,    0,   0  ]   [4,   3,    -2]
        [2,    1,   0  ] × [0,  -1,     3]
        [-0.5, -6.5, 1]   [0,   0,  25.5]

A[0][0] = 1×4 + 0×0 + 0×0 = 4 ✓
A[1][0] = 2×4 + 1×0 + 0×0 = 8 ✓
A[1][1] = 2×3 + 1×(-1) + 0×0 = 5 ✓
...
```

## 💻 Uso Prático

```python
from sistemas_lineares import fatoracao_LU

A = [
    [4.0, 3.0, -2.0],
    [8.0, 5.0, -1.0],
    [-2.0, 5.0, 7.0]
]

b = [11.0, 19.0, 8.0]

# Resolver o sistema
x, etapas, historico = fatoracao_LU(A, b)

# x = [0.9118, 2.2941, -0.2353]
# etapas = 8 (total de operações principais)
# historico = lista de todos os eventos
```

## 🎓 Quando Usar Fatoração LU vs Eliminação de Gauss

| Critério | LU | Gauss |
|----------|----|----|
| **Um sistema** | Similar | Equivalente |
| **Múltiplos b's** | ✓ Melhor (reutilizar L,U) | Refazer tudo |
| **Matrizes muito grandes** | ✓ Melhor (economiza memória) | Mais lento |
| **Precisão** | Com pivotamento parcial | Com pivotamento parcial |

## ⚠️ Considerações Importantes

1. **Pivô nulo/quase nulo**: Se o elemento diagonal for muito pequeno, o sistema é singular ou mal-condicionado
2. **Pivotamento**: A versão atual usa sem pivotamento. Com pivotamento parcial é mais estável
3. **Unicidade**: A fatoração LU não é única sem restrições adicionais (como diagonal de L = 1)

## 🔗 Relação com Outros Métodos

- **Eliminação de Gauss**: LU é uma variação que armazena os multiplicadores
- **Decomposição Cholesky**: Versão especializada para matrizes simétricas positivas definidas
- **QR**: Alternativa para sistemas sobre-determinados
