import math
import sys
import os


# ==============================================================================
# QUESTAO 3.8
# ==============================================================================
"""
PROBLEMA: Comparar dois planos de financiamento e determinar qual tem menor
    taxa de juros mensal J.

Preco a vista: 162.00
Entrada: 22.00
Valor financiado (VF): 140.00

Plano A:
- P = 9 prestacoes de PM = 26.50

Plano B:
- P = 12 prestacoes de PM = 21.50

Equacao base:
(1 - (1 + J)^(-P)) / J = VF / PM

Com x = 1 + J e k = VF / PM, obtem-se:
f(x) = k*x^(P+1) - (k+1)*x^P + 1 = 0

Buscamos a raiz positiva x != 1. Em seguida, J = x - 1.
"""


# Adiciona o diretorio 'src' ao path principal se nao estiver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from metodos import zeros_de_funcao, utils


# ==============================================================================
# SECAO 1: MODELAGEM MATEMATICA
# ==============================================================================
def modelar_funcoes():
    vf = 162.0 - 22.0

    k_a = vf / 26.5
    p_a = 9

    k_b = vf / 21.5
    p_b = 12

    funcoes = {
        # Plano A: f1(x) = k_a*x^(p_a+1) - (k_a+1)*x^p_a + 1
        'f1': lambda x: k_a * (x ** (p_a + 1)) - (k_a + 1) * (x ** p_a) + 1,

        # Plano B: f2(x) = k_b*x^(p_b+1) - (k_b+1)*x^p_b + 1
        'f2': lambda x: k_b * (x ** (p_b + 1)) - (k_b + 1) * (x ** p_b) + 1,

        # Iteracoes de ponto fixo
        'g1': lambda x: x - 0.05 * (k_a * (x ** (p_a + 1)) - (k_a + 1) * (x ** p_a) + 1),
        'g2': lambda x: x - 0.02 * (k_b * (x ** (p_b + 1)) - (k_b + 1) * (x ** p_b) + 1),
    }

    # Mapeamento explicito de quais g's pertencem a cada f
    funcoes['_mapping'] = {
        'f1': ['g1'],
        'f2': ['g2']
    }

    return funcoes


# ==============================================================================
# SECAO 2: MOTOR DOS TESTES
# ==============================================================================



def rodar_algoritmos():
    """Orquestra a execucao dos metodos e salva os resultados em CSV."""

    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    parametros, saidas_dir = utils.configurar_ambiente(nome_script)

    if not parametros:
        print("-> Preencha o arquivo de entrada criado e execute novamente.")
        return

    todas_funcoes = modelar_funcoes()
    mapeamento_g_f = todas_funcoes.pop('_mapping', {})
    funcoes_principais = {nome: func for nome, func in todas_funcoes.items() if nome.startswith('f')}
    funcoes_iteracao = {nome: func for nome, func in todas_funcoes.items() if nome.startswith('g')}

    default_a = parametros.get('a', 1.08)
    default_b = parametros.get('b', 1.20)

    resultados = []
    print(f"\n=== RODANDO EXPERIMENTOS - SCRIPT [{nome_script}.py] ===")

    for id_f, f_loop in funcoes_principais.items():
        print(f"\n[Testando as raizes da Equacao: {id_f}]")

        a = parametros.get(f'{id_f}_a', default_a)
        b = parametros.get(f'{id_f}_b', default_b)
        x0 = parametros.get(f'{id_f}_x0', parametros.get('x0', 1.10))
        tol = parametros.get(f'{id_f}_tol', parametros.get('tol', 1e-6))
        max_iter = int(parametros.get(f'{id_f}_max_iter', parametros.get('max_iter', 100)))

        metodos = {
            f"{id_f} - Bisseccao":      lambda f=f_loop, a=a, b=b: zeros_de_funcao.bisseccao(f, a, b, tol, max_iter),
            f"{id_f} - Posicao Falsa":  lambda f=f_loop, a=a, b=b: zeros_de_funcao.posicaoFalsa(f, a, b, tol, max_iter),
            f"{id_f} - Newton-Raphson": lambda f=f_loop, x0=x0, tol=tol, max_iter=max_iter: zeros_de_funcao.newton_raphson(f, x0, tol, max_iter),
            f"{id_f} - Secante":        lambda f=f_loop, a=a, b=b: zeros_de_funcao.secante(f, a, b, tol, max_iter)
        }

        g_list = mapeamento_g_f.get(id_f, [])
        if not g_list:
            numero_f = id_f.replace('f', '')
            g_list = [g for g in funcoes_iteracao.keys() if g.replace('g', '') == numero_f]

        for id_g in g_list:
            if id_g in funcoes_iteracao:
                g_loop = funcoes_iteracao[id_g]
                metodos[f"{id_f} - Ponto Fixo ({id_g})"] = lambda g=g_loop: zeros_de_funcao.ponto_fixo(g, x0, tol, max_iter)

        for nome_metodo, chamada in metodos.items():
            raiz, iteracoes, historico = chamada()
            erro = historico[-1]['erro'] if historico else 0

            j = raiz - 1 if raiz is not None else None
            resultados.append({
                'Metodo': nome_metodo,
                'Raiz': raiz,
                'Juros': j,
                'Iteracoes': iteracoes,
                'Erro': erro
            })

            nome_arquivo_seguro = (
                nome_metodo.lower()
                .replace(' ', '')
                .replace('-', '_')
                .replace('(', '_')
                .replace(')', '')
            )
            utils.salvar_csv(os.path.join(saidas_dir, f"{nome_script}_hist_{nome_arquivo_seguro}.csv"), historico)

    caminho_comparativo = os.path.join(saidas_dir, f"{nome_script}.csv")
    utils.salvar_csv(caminho_comparativo, resultados)

    print("\n= RESULTADOS FINAIS:")
    for res in resultados:
        juros_pct = res['Juros'] * 100 if res['Juros'] is not None else float('nan')
        print(
            f" -> {res['Metodo']:<30} | x = {res['Raiz']:<12.6f} | "
            f"J = {res['Juros']:<10.6f} ({juros_pct:>7.4f}%) | Iteracoes = {res['Iteracoes']}"
        )

    # Compara os planos com base em raizes nao triviais (x != 1)
    juros_f1 = [r['Juros'] for r in resultados if r['Metodo'].startswith('f1') and abs(r['Raiz'] - 1.0) > 1e-3]
    juros_f2 = [r['Juros'] for r in resultados if r['Metodo'].startswith('f2') and abs(r['Raiz'] - 1.0) > 1e-3]
    if juros_f1 and juros_f2:
        j_a = sum(juros_f1) / len(juros_f1)
        j_b = sum(juros_f2) / len(juros_f2)
        melhor = 'Plano A' if j_a < j_b else 'Plano B'
        print("\n= COMPARACAO DOS PLANOS (raiz positiva x != 1):")
        print(f" -> Plano A: J medio ~= {j_a:.6f} ({j_a * 100:.4f}%)")
        print(f" -> Plano B: J medio ~= {j_b:.6f} ({j_b * 100:.4f}%)")
        print(f" -> Melhor para o consumidor: {melhor} (menor taxa de juros)")

    print(f"\n[SUCESSO] Planilhas renderizadas em '{saidas_dir}'.")


if __name__ == '__main__':
    rodar_algoritmos()
