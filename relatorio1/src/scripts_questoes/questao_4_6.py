import math
import sys
import os

# Adiciona o diretório 'src' ao path principal se não estiver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from metodos import sistemas_lineares, utils

# ==============================================================================
# SEÇÃO 1: MODELAGEM DOS SISTEMAS
# ==============================================================================
def modelar_sistema():
    """
    Defina o sistema linear (matriz A e vetor b) alvo do problema.
    Problema 4.6 - Circuito em escada
    Equações simplificadas:
    1: 4(I1 + I2 + Ix) + 10 I1 = 100                   -> 14*I1 + 4*I2 + 4*Ix = 100
    2: 4(I1 + I2 + Ix) + 3(I2 + Ix) + 10 Ix = 100 - 2 Ix -> 4*I1 + 7*I2 + 19*Ix = 100
    3: 4(I1 + I2 + Ix) + 3(I2 + Ix) + 9 Ix = 100 - 2 Ix  -> 4*I1 + 7*I2 + 18*Ix = 100
    """
    A = [
        [14.0,  4.0,  4.0],
        [ 4.0,  7.0, 19.0],
        [ 4.0,  7.0, 18.0]
    ]
    b = [100.0, 100.0, 100.0]
    return A, b

# ==============================================================================
# SEÇÃO 2: MOTOR DOS TESTES 
# ==============================================================================
def inicializar_ambiente(nome_script):
    """Garante a estrutura de pastas e arquivo config estático paramétrico."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    entradas_dir = os.path.join(base_dir, 'dados', 'entradas')
    saidas_dir = os.path.join(base_dir, 'dados', 'saida', nome_script)
    os.makedirs(entradas_dir, exist_ok=True)
    os.makedirs(saidas_dir, exist_ok=True)
    arquivo_entrada = os.path.join(entradas_dir, f"{nome_script}.txt")
    if not os.path.exists(arquivo_entrada):
        with open(arquivo_entrada, 'w') as file:
            file.write("# Preencha os parametros para o script e o rode novamente.\n")
            file.write("tol:1e-12\n")
        return None, saidas_dir
    parametros = {}
    with open(arquivo_entrada, 'r') as file:
        for linha in file:
            linha = linha.strip()
            if linha and not linha.startswith('#') and ':' in linha:
                chave, valor = linha.split(':')
                parametros[chave.strip()] = float(valor.strip())
    return parametros, saidas_dir

def multiplicar_matriz_vetor(A, x):
    n = len(A)
    m = len(A[0])
    resultado = [0.0] * n
    for i in range(n):
        soma = 0.0
        for j in range(m):
            soma += A[i][j] * x[j]
        resultado[i] = soma
    return resultado

def rodar_algoritmos():
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    parametros, saidas_dir = inicializar_ambiente(nome_script)
    if parametros is None:
        print(f"-> Por favor, vá na entrada criada, preencha os dados da questão e execute o script novamente!")
        return

    A, b = modelar_sistema()
    tol = parametros.get('tol', 1e-12)

    resultados = []
    print(f"\n=== RODANDO EXPERIMENTOS - SCRIPT [{nome_script}.py] ===")
    print("a) SISTEMA DE EQUACOES NA FORMA Ax = b:")
    for i in range(len(A)):
        print(f" {A[i]} * [I{i+1}] = {b[i]}")

    print("\nb) DETERMINANDO A^(-1):")
    try:
        invA = sistemas_lineares.inversa_matriz(A, tol_pivo=tol)
        print("A inversa (A^-1) calculada é:")
        for linha in invA:
            print(f" [{', '.join([f'{val:.6f}' for val in linha])}]")
            
        print("\nc) DETERMINANDO O VALOR DE Ix USANDO A^-1:")
        x_inv = multiplicar_matriz_vetor(invA, b)
        print(f"Produto A^-1 * b resulta no vetor x: {x_inv}")
        print(f"O valor de Ix (3ª componente) é: {x_inv[2]:.6f} A")
    except Exception as e:
        print(f"Erro ao calcular inversa e produto: {e}")

    print("\n[d) RESOLVENDO O SISTEMA (OUTROS MÉTODOS DIRETOS): ]")
    metodos = {
        "Eliminação de Gauss": lambda A=A, b=b: sistemas_lineares.eliminacao_gauss(A, b, pivotamento_parcial=True, tol_pivo=tol),
        "Fatoração LU": lambda A=A, b=b: sistemas_lineares.fatoracao_LU(A, b, tol_pivo=tol),
        "Gauss-Jordan": lambda A=A, b=b: sistemas_lineares.gauss_jordan(A, b, pivotamento_parcial=True, tol_pivo=tol)
    }

    for nome_metodo, chamada in metodos.items():
        try:
            raiz, etapas, historico = chamada()
            resultados.append({
                "Metodo": nome_metodo, 
                "I1": raiz[0], 
                "I2": raiz[1], 
                "Ix": raiz[2], 
                "Etapas": etapas
            })
            nome_arquivo_seguro = nome_metodo.lower().replace(" ", "").replace("-", "_").replace("ç", "c").replace("ã", "a").replace("í", "i").replace("", "")
            utils.salvar_csv(os.path.join(saidas_dir, f"{nome_script}_hist_{nome_arquivo_seguro}.csv"), historico)
        except Exception as e:
            print(f"Erro em {nome_metodo}: {e}")

    caminho_comparativo = os.path.join(saidas_dir, f"{nome_script}.csv")
    utils.salvar_csv(caminho_comparativo, resultados)

    print("\n= RESULTADOS FINAIS CORRENTES I = [I1, I2, Ix]:")
    for res in resultados:
        i_sol = f"[{res['I1']:.6f}, {res['I2']:.6f}, {res['Ix']:.6f}]"
        print(f" -> {res['Metodo']:<25} | I = {i_sol:<35} | Etapas = {res['Etapas']}")

    print(f"\n[SUCESSO] Planilhas renderizadas em '{saidas_dir}'.")

if __name__ == '__main__':
    rodar_algoritmos()
