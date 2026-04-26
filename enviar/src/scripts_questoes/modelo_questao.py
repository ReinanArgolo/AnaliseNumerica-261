import math
import sys
import os

# Adiciona o diretório 'src' ao path principal se não estiver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from metodos import zeros_de_funcao, utils

# ==============================================================================
# SEÇÃO 1: MODELAGEM MATEMÁTICA 
# ==============================================================================
def modelar_funcoes():
    """Defina as funções alvo para seu problema matemático aqui."""
    
    funcoes = {
        # Função principal (usada em Bissecção, Posição Falsa, Newton e Secante)
        'f1': lambda x: 1 - (1 + x + (x**2)/2) * math.exp(-x) - 0.1, # f(t) = 1 - (1 + t + t^2/2) * e^(-t) - 0.1
        'f2': lambda x: 1 - (1 + x + (x**2)/2) * math.exp(-x) - 0.9, # f(t) = 1 - (1 + t + t^2/2) * e^(-t) - 0.9

        # Funções de iteração para Ponto Fixo (g(x) = x - f(x) ou outras formas)
        'g1': lambda x: -math.log((1 - 0.1) / (1 + x + (x**2)/2)),
        'g2': lambda x: -math.log((1 - 0.9) / (1 + x + (x**2)/2)),
        'g3': lambda x: math.log((1 + x + (x**2)/2) / (1 - 0.1)),
        'g4': lambda x: math.log((1 + x + (x**2)/2) / (1 - 0.9)),
        'g7': lambda x: x - 0.5*(1 - (1 + x + (x**2)/2)*math.exp(-x) - 0.1),
        'g8': lambda x: x - 0.5*(1 - (1 + x + (x**2)/2)*math.exp(-x) - 0.9),


    }

    return funcoes

# ==============================================================================
# SEÇÃO 2: MOTOR DOS TESTES 
# ==============================================================================


def rodar_algoritmos():
    """Função orquestradora: Recebe as funções matemáticas, alimenta as variáveis 
        através das leituras do .txt, aciona os algoritmos e armazena relatórios."""
    
    # Baseado no nome do arquivo (.py), injeta variáveis estáticas do TXT e retorna a pasta de saída
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    parametros, saidas_dir = utils.configurar_ambiente(nome_script, ["# Preencha os parametros para o script e o rode novamente.\n", "a:0.0\n", "b:1.0\n", "x0:0.5\n", "tol:1e-4\n", "max_iter:100\n"])
    
    if not parametros:
        print(f"-> Por favor, vá na entrada criada, preencha os dados da questão e execute o script novamente!")
        return

    # Recupera todas as funções matemáticas fornecidas no Modelador e separa Fs e Gs
    todas_funcoes = modelar_funcoes()
    funcoes_principais = {nome: func for nome, func in todas_funcoes.items() if nome.startswith('f')}
    funcoes_iteracao = {nome: func for nome, func in todas_funcoes.items() if nome.startswith('g')}

    # Mapeando Chaves com valores padrão caso o TXT esteja incompleto
    a = parametros.get('a', 0.0)
    b = parametros.get('b', 1.0)
    x0 = parametros.get('x0', 0.5)
    tol = parametros.get('tol', 1e-4)
    max_iter = int(parametros.get('max_iter', 100))

    resultados = []
    print(f"\n=== RODANDO EXPERIMENTOS - SCRIPT [{nome_script}.py] ===")

    # Percorre cada Função F(x) definida
    for id_f, f_loop in funcoes_principais.items():
        print(f"\n[Testando as raízes da Equação: {id_f}]")

        metodos = {
            f"{id_f} - Bissecção":      lambda f=f_loop: zeros_de_funcao.bisseccao(f, a, b, tol, max_iter),
            f"{id_f} - Posição Falsa":  lambda f=f_loop: zeros_de_funcao.posicaoFalsa(f, a, b, tol, max_iter),
            f"{id_f} - Newton-Raphson": lambda f=f_loop: zeros_de_funcao.newton_raphson(f, x0, tol, max_iter),
            f"{id_f} - Secante":        lambda f=f_loop: zeros_de_funcao.secante(f, a, b, tol, max_iter)
        }
        
        # Acrescenta dinamicamente as execuções de Ponto Fixo (se houverem G(x)'s propostos)
        for id_g, g_loop in funcoes_iteracao.items():
            # Ex: A g1 pertence à f1, g2 à f2... Logo não cruza funções diferentes
            if id_g.replace('g', '') == id_f.replace('f', ''): 
                metodos[f"{id_f} - Ponto Fixo ({id_g})"] = lambda g=g_loop: zeros_de_funcao.ponto_fixo(g, x0, tol, max_iter)

        for nome_metodo, chamada in metodos.items():
            raiz, iteracoes, historico = chamada()
            erro = historico[-1]["erro"] if historico else 0
            
            # Consolida para o CSV resumo principal
            resultados.append({"Metodo": nome_metodo, "Raiz": raiz, "Iteracoes": iteracoes, "Erro": erro})
            
            # Consolida individual (Ex: arquivo questaoX_f1_hist_secante.csv)
            nome_arquivo_seguro = nome_metodo.lower().replace(" ", "").replace("-", "_").replace("ç", "c").replace("ã", "a").replace("(", "_").replace(")", "")
            utils.salvar_csv(os.path.join(saidas_dir, f"{nome_script}_hist_{nome_arquivo_seguro}.csv"), historico)

    caminho_comparativo = os.path.join(saidas_dir, f"{nome_script}.csv")
    utils.salvar_csv(caminho_comparativo, resultados)

    print("\n= RESULTADOS FINAIS:")
    for res in resultados:
        print(f" -> {res['Metodo']:<30} | Raiz = {res['Raiz']:<12.6f} | Iteraçoes = {res['Iteracoes']}")
    print(f"\n[SUCESSO] Planilhas renderizadas em '{saidas_dir}'.")

if __name__ == '__main__':
    rodar_algoritmos()