import math
import sys
import os


# ==============================================================================
# QUESTÃO 3.3
# ==============================================================================
"""
PROBLEMA: Encontrar o tempo t em que a solução da EDO y' = -y, y(0) = 1
atinge 10% e 90% do seu valor assintótico.

A solução exata é: y(t) = e^(-t)
O valor assintótico é: y(∞) = 0

Para y(t) = 0.1: 1 - (1 + t + t²/2) * e^(-t) = 0.1
Para y(t) = 0.9: 1 - (1 + t + t²/2) * e^(-t) = 0.9

Utilize os métodos numéricos (Bissecção, Posição Falsa, Newton-Raphson, 
Secante e Ponto Fixo) para encontrar as raízes com precisão de 1e-4.
"""



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
            file.write("a:0.0\n")
            file.write("b:1.0\n")
            file.write("x0:0.5\n")
            file.write("tol:1e-4\n")
            file.write("max_iter:100\n")
        return None, saidas_dir

    # Parsing simples do aquivo .TXT para dicionários do python
    parametros = {}
    with open(arquivo_entrada, 'r') as file:
        for linha in file:
            linha = linha.strip()
            if linha and not linha.startswith('#'):
                chave, valor = linha.split(':')
                parametros[chave.strip()] = float(valor.strip())
                
    return parametros, saidas_dir

def rodar_algoritmos():
    """Função orquestradora: Recebe as funções matemáticas, alimenta as variáveis 
        através das leituras do .txt, aciona os algoritmos e armazena relatórios."""
    
    # Baseado no nome do arquivo (.py), injeta variáveis estáticas do TXT e retorna a pasta de saída
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    parametros, saidas_dir = inicializar_ambiente(nome_script)
    
    if not parametros:
        print(f"-> Por favor, vá na entrada criada, preencha os dados da questão e execute o script novamente!")
        return

    # Recupera todas as funções matemáticas fornecidas no Modelador e separa Fs e Gs
    todas_funcoes = modelar_funcoes()
    funcoes_principais = {nome: func for nome, func in todas_funcoes.items() if nome.startswith('f')}
    funcoes_iteracao = {nome: func for nome, func in todas_funcoes.items() if nome.startswith('g')}

    # Puxa parâmetros padrões genéricos (caso a função não tenha os seus)
    default_a = parametros.get('a', 0.0)
    default_b = parametros.get('b', 1.0)

    resultados = []
    print(f"\n=== RODANDO EXPERIMENTOS - SCRIPT [{nome_script}.py] ===")

    # Percorre cada Função F(x) definida
    for id_f, f_loop in funcoes_principais.items():
        print(f"\n[Testando as raízes da Equação: {id_f}]")

        # Busca os parâmetros ESPECÍFICOS para a função atual (ex: f1_a, f2_a)
        # Se não encontrar, ele cai pro default
        a = parametros.get(f'{id_f}_a', default_a)
        b = parametros.get(f'{id_f}_b', default_b)
        x0 = parametros.get(f'{id_f}_x0', parametros.get('x0', 0.5))
        tol = parametros.get(f'{id_f}_tol', parametros.get('tol', 1e-4))
        max_iter = int(parametros.get(f'{id_f}_max_iter', parametros.get('max_iter', 100)))

        metodos = {
            f"{id_f} - Bissecção":      lambda f=f_loop, a=a, b=b: zeros_de_funcao.bisseccao(f, a, b, tol, max_iter),
            f"{id_f} - Posição Falsa":  lambda f=f_loop, a=a, b=b: zeros_de_funcao.posicaoFalsa(f, a, b, tol, max_iter),
            f"{id_f} - Newton-Raphson": lambda f=f_loop, x0=x0, tol=tol, max_iter=max_iter: zeros_de_funcao.newton_raphson(f, x0, tol, max_iter),
            f"{id_f} - Secante":        lambda f=f_loop, a=a, b=b: zeros_de_funcao.secante(f, a, b, tol, max_iter)
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

    # Salvando CSV Tabela Geral Consolidadora das Questões
    caminho_comparativo = os.path.join(saidas_dir, f"{nome_script}.csv")
    utils.salvar_csv(caminho_comparativo, resultados)

    # Relatório Final em Console
    print("\n= RESULTADOS FINAIS:")
    for res in resultados:
        print(f" -> {res['Metodo']:<30} | Raiz = {res['Raiz']:<12.6f} | Iteraçoes = {res['Iteracoes']}")
    print(f"\n[SUCESSO] Planilhas renderizadas em '{saidas_dir}'.")

if __name__ == '__main__':
    rodar_algoritmos()