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
    Problema 4.3 - Cachorro perdido no labirinto
    """
    
    A = [
        [ 4.0, -1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [-1.0,  4.0, -1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0],
        [ 0.0, -1.0,  4.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0],
        [-1.0,  0.0,  0.0,  4.0, -1.0,  0.0, -1.0,  0.0,  0.0],
        [ 0.0, -1.0,  0.0, -1.0,  4.0, -1.0,  0.0, -1.0,  0.0],
        [ 0.0,  0.0, -1.0,  0.0, -1.0,  4.0,  0.0,  0.0, -1.0],
        [ 0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  4.0, -1.0,  0.0],
        [ 0.0,  0.0,  0.0,  0.0, -1.0,  0.0, -1.0,  4.0, -1.0],
        [ 0.0,  0.0,  0.0,  0.0,  0.0, -1.0,  0.0, -1.0,  4.0]
    ]
    
    b = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
    
    return A, b

# ==============================================================================
# SEÇÃO 2: MOTOR DOS TESTES 
# ==============================================================================



def rodar_algoritmos():
    """Função orquestradora que une modelagem, extração do .txt e executa algoritmos e salva relatórios."""
    
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    parametros, saidas_dir = utils.configurar_ambiente(nome_script, ["# Preencha os parametros para o script e o rode novamente.\n", "tol:1e-12\n"])
    
    if parametros is None:
        print(f"-> Por favor, vá na entrada criada, preencha os dados da questão e execute o script novamente!")
        return

    A, b = modelar_sistema()
    tol = parametros.get('tol', 1e-12)

    resultados = []
    print(f"\n=== RODANDO EXPERIMENTOS - SCRIPT [{nome_script}.py] ===")
    print("SISTEMA DE EQUACOES (Probabilidades do Labirinto):")
    for i in range(len(A)):
        print(f" {A[i]} * [P{i+1}] = {b[i]}")
    
    print("\n[c) RESOLVENDO O SISTEMA: ]")

    metodos = {
        "Eliminação de Gauss": lambda A=A, b=b: sistemas_lineares.eliminacao_gauss(A, b, pivotamento_parcial=True, tol_pivo=tol),
        "Fatoração LU": lambda A=A, b=b: sistemas_lineares.fatoracao_LU(A, b, tol_pivo=tol),
    }

    for nome_metodo, chamada in metodos.items():
        try:
            raiz, etapas, historico = chamada()
            
            res = {
                "Metodo": nome_metodo, 
                "Etapas": etapas
            }
            for i, val in enumerate(raiz):
                res[f"P{i+1}"] = val
                
            resultados.append(res)
            
            nome_arquivo_seguro = nome_metodo.lower().replace(" ", "").replace("-", "_").replace("ç", "c").replace("ã", "a").replace("í", "i").replace("", "")
            utils.salvar_csv(os.path.join(saidas_dir, f"{nome_script}_hist_{nome_arquivo_seguro}.csv"), historico)
            
        except Exception as e:
            print(f"Erro em {nome_metodo}: {e}")

    caminho_comparativo = os.path.join(saidas_dir, f"{nome_script}.csv")
    utils.salvar_csv(caminho_comparativo, resultados)

    print("\n= RESULTADOS FINAIS PROBABILIDADES P = [P1, P2, ... , P9]:")
    for res in resultados:
        p_vals = [res.get(f"P{i+1}", 0.0) for i in range(len(A))]
        p_sol = "[" + ", ".join([f"{v:.4f}" for v in p_vals]) + "]"
        print(f" -> {res['Metodo']:<25} | P = {p_sol} | Etapas = {res['Etapas']}")

    print(f"\n[SUCESSO] Planilhas renderizadas em '{saidas_dir}'.")

if __name__ == '__main__':
    rodar_algoritmos()
