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
    1:  8*i1 - 4*i2 - 2*i3 = 10
    2: -4*i1 + 6*i2 - 2*i3 = 0
    3: -2*i1 - 2*i2 + 10*i3 = 4
    """
    
    A = [
        [8.0, -4.0, -2.0],
        [-4.0, 6.0, -2.0],
        [-2.0, -2.0, 10.0]
    ]
    b = [10.0, 0.0, 4.0]
    
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
    
    # Se input.txt não constar, cria o molde da questão para o usuário preencher
    if not os.path.exists(arquivo_entrada):
        print(f"[{nome_script}] Arquivo de configuração '{nome_script}.txt' não encontrado.")
        print(f"-> Criando template em 'dados/entradas/{nome_script}.txt'...")
        with open(arquivo_entrada, 'w') as file:
            file.write("# Preencha os parametros para o script e o rode novamente.\n")
            file.write("tol:1e-12\n")
        return None, saidas_dir

    # Parsing simples do aquivo .TXT para dicionários do python
    parametros = {}
    with open(arquivo_entrada, 'r') as file:
        for linha in file:
            linha = linha.strip()
            if linha and not linha.startswith('#') and ':' in linha:
                chave, valor = linha.split(':')
                parametros[chave.strip()] = float(valor.strip())
                
    return parametros, saidas_dir

def teste_cholesky(A):
    """Analisa e justifica viabilidade do uso por Cholesky"""
    simetrica = all(A[i][j] == A[j][i] for i in range(len(A)) for j in range(len(A)))
    
    det1 = A[0][0]
    det2 = A[0][0]*A[1][1] - A[0][1]*A[1][0]
    det3 = ( A[0][0]*(A[1][1]*A[2][2] - A[1][2]*A[2][1]) - 
             A[0][1]*(A[1][0]*A[2][2] - A[1][2]*A[2][0]) + 
             A[0][2]*(A[1][0]*A[2][1] - A[1][1]*A[2][0]) )
             
    is_positiva = (det1 > 0) and (det2 > 0) and (det3 > 0)
    
    justificativa = (f"Simetrica: {simetrica}\n"
                     f"Determinantes (Sylvester): Det1={det1}, Det2={det2}, Det3={det3} (Todos > 0: {is_positiva})\n")
    if simetrica and is_positiva:
        justificativa += "O sistema reune os criteios para ser resolvido pelo metodo de Cholesky."
    else:
        justificativa += "Cholesky nao pode ser aplicado (nao é Simetrica e Positivo Definida)."
    return justificativa

def rodar_algoritmos():
    """Função orquestradora que une modelagem, extração do .txt e executa algoritmos e salva relatórios."""
    
    # Baseado no nome do arquivo (.py), injeta variáveis estáticas do TXT e retorna a pasta de saída
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    parametros, saidas_dir = inicializar_ambiente(nome_script)
    
    if parametros is None:
        print(f"-> Por favor, vá na entrada criada, preencha os dados da questão e execute o script novamente!")
        return

    A, b = modelar_sistema()

    # Mapeando Chaves com valores padrão caso o TXT esteja incompleto
    tol = parametros.get('tol', 1e-12)

    resultados = []
    print(f"\n=== RODANDO EXPERIMENTOS - SCRIPT [{nome_script}.py] ===")
    print("SISTEMA DE EQUACOES (Leis de Kirchhoff):")
    for i in range(len(A)):
        print(f" {A[i]} * [i{i+1}] = {b[i]}")

    print("\n[a) É possível resolver por LU?]")
    print("Sim, matriz é densa e regular. A Decomposicao LU classica necessita primordialmente que as submatrizes principais sejam não nulas (invertíveis), e isso é contemplado pela natureza positiva desta matriz principal de resistências da formulação.")
    
    print("\n[b) É possível resolver pelo método de Cholesky?]")
    print(teste_cholesky(A))
    
    print("\n[c) RESOLVENDO O SISTEMA: ]")

    metodos = {
        "Eliminação de Gauss": lambda A=A, b=b: sistemas_lineares.eliminacao_gauss(A, b, pivotamento_parcial=True, tol_pivo=tol),
        "Fatoração LU": lambda A=A, b=b: sistemas_lineares.fatoracao_LU(A, b, tol_pivo=tol)
    }

    for nome_metodo, chamada in metodos.items():
        try:
            raiz, etapas, historico = chamada()
            
            # Consolida para o CSV resumo
            resultados.append({
                "Metodo": nome_metodo, 
                "i1": raiz[0], 
                "i2": raiz[1], 
                "i3": raiz[2], 
                "Etapas": etapas
            })
            
            # Consolida log numérico granular
            nome_arquivo_seguro = nome_metodo.lower().replace(" ", "").replace("-", "_").replace("ç", "c").replace("ã", "a").replace("", "")
            utils.salvar_csv(os.path.join(saidas_dir, f"{nome_script}_hist_{nome_arquivo_seguro}.csv"), historico)
                
        except Exception as e:
            print(f"Erro em {nome_metodo}: {e}")

    # Salvando CSV Tabela Geral
    caminho_comparativo = os.path.join(saidas_dir, f"{nome_script}.csv")
    utils.salvar_csv(caminho_comparativo, resultados)

    # Relatório Final em Console
    print("\n= RESULTADOS FINAIS CORRENTES i = [i1, i2, i3]:")
    for res in resultados:
        i_sol = f"[{res['i1']:.6f}, {res['i2']:.6f}, {res['i3']:.6f}]"
        print(f" -> {res['Metodo']:<25} | i = {i_sol:<35} | Etapas = {res['Etapas']}")
    print(f"\n[SUCESSO] Planilhas renderizadas em '{saidas_dir}'.")

if __name__ == '__main__':
    rodar_algoritmos()