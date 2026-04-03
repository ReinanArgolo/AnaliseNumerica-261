import math
import sys
import os


# ==============================================================================
# QUESTÃO 3.3
# ==============================================================================
"""
PROBLEMA: Calcular a inclinaçào do angulo theta, em que o lançamento do míssil deve ser feito antes de atingir determinado alvo na equação abaixo:

tg(theta/2) = [sen(alfa) cos(alfa)] / [(gR)/v^2 - cos^2(alfa), onde:

alfa - angulo de inclicação com a superfíce da terra com a qual é feita o lancamento do míssil
g - aceleração da gravidade (aprox. 9.81m/s^2)
R - Raio da terra (aprox. 6371000m)
v - velocidade de lançamento do míssil (m/s)
theta - Ângulo (medido do centro da terra) entre o ponto de lançamento e o ponto de impacto desejado

Resolva o problema considerando theta = 80 graus e v tal que v^2/gR = 1.25, ou seja, aproximadadmente 8.840m/s

"""



# Adiciona o diretório 'src' ao path principal se não estiver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from metodos import zeros_de_funcao, utils

# ==============================================================================
# SEÇÃO 1: MODELAGEM MATEMÁTICA 
# ==============================================================================
def modelar_funcoes():
    theta_rad = math.radians(80) / 2  # 40 graus em radianos
    tan_theta_2 = math.tan(theta_rad)
    
    funcoes = {
        # Resolver: sin(α)cos(α) = 0.8 * tan(40°) * [1 - cos²(α)]
        'f1': lambda x: math.sin(x)*math.cos(x) - tan_theta_2*(0.8 - math.cos(x)**2),
        # Ponto fixo: α = arctan(...)
        'g1': lambda x: math.atan((0.8 * tan_theta_2 * (1 - math.pow(math.cos(x), 2))) / math.cos(x)),
        'g2': lambda x: math.atan((math.sin(x) * math.cos(x)) / (0.8 - math.cos(x)**2)),
        'g3': lambda x: math.acos(math.sqrt(0.8 - (math.sin(x)*math.cos(x))/tan_theta_2)
)
    }
    # Mapeamento de quais g's pertencem a cada f
    funcoes['_mapping'] = {'f1': ['g1', 'g2','g3']}
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
    mapeamento_g_f = todas_funcoes.pop('_mapping', {})
    funcoes_principais = {nome: func for nome, func in todas_funcoes.items() if nome.startswith('f')}
    funcoes_iteracao = {nome: func for nome, func in todas_funcoes.items() if nome.startswith('g')}

    # Puxa parâmetros padrões genéricos (caso a função não tenha os seus)
    default_a = parametros.get('a', 0.0)
    default_b = parametros.get('b', 1.0)
    
    # Converte valores de entrada para radianos (ângulos em graus)
    default_a_rad = math.radians(default_a)
    default_b_rad = math.radians(default_b)

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
        
        # Converte ângulos de graus para radianos
        a = math.radians(a)
        b = math.radians(b)
        x0 = math.radians(x0)

        metodos = {
            f"{id_f} - Bissecção":      lambda f=f_loop, a=a, b=b: zeros_de_funcao.bisseccao(f, a, b, tol, max_iter),
            f"{id_f} - Posição Falsa":  lambda f=f_loop, a=a, b=b: zeros_de_funcao.posicaoFalsa(f, a, b, tol, max_iter),
            f"{id_f} - Newton-Raphson": lambda f=f_loop, x0=x0, tol=tol, max_iter=max_iter: zeros_de_funcao.newton_raphson(f, x0, tol, max_iter),
            f"{id_f} - Secante":        lambda f=f_loop, a=a, b=b: zeros_de_funcao.secante(f, a, b, tol, max_iter)
        }
        
        # Acrescenta dinamicamente as execuções de Ponto Fixo (se houverem G(x)'s propostos)
        # Usa mapeamento se disponível, senão tenta correspondência por número
        g_list = mapeamento_g_f.get(id_f, [])
        if not g_list:
            # Fallback: corresponde g1 com f1, g2 com f2, etc
            numero_f = id_f.replace('f', '')
            g_list = [g for g in funcoes_iteracao.keys() if g.replace('g', '') == numero_f]
        
        for id_g in g_list:
            if id_g in funcoes_iteracao:
                g_loop = funcoes_iteracao[id_g]
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