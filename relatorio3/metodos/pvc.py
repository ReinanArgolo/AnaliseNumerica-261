"""Métodos para problema de valor de contorno sem bibliotecas lineares prontas."""

from metodos.sistemas import rk4_sistema


def thomas(subdiagonal, diagonal, superdiagonal, termos):
    """Resolve sistema tridiagonal pelo algoritmo de Thomas."""
    n = len(diagonal)
    c = [0.0] * n
    d = [0.0] * n
    c[0] = superdiagonal[0] / diagonal[0]
    d[0] = termos[0] / diagonal[0]

    for i in range(1, n):
        denominador = diagonal[i] - subdiagonal[i - 1] * c[i - 1]
        if i < n - 1:
            c[i] = superdiagonal[i] / denominador
        d[i] = (termos[i] - subdiagonal[i - 1] * d[i - 1]) / denominador

    solucao = [0.0] * n
    solucao[-1] = d[-1]

    for i in range(n - 2, -1, -1):
        solucao[i] = d[i] - c[i] * solucao[i + 1]

    return solucao


def shooting_calor(parametros, n_internos):
    """Resolve o problema da haste pelo Método Shooting."""
    h_linha = parametros["h_linha"]
    ta = parametros["ta"]
    t1 = parametros["t1"]
    t2 = parametros["t2"]
    comprimento = parametros["comprimento"]
    dx = comprimento / (n_internos + 1)

    def sistema(x, estado, _):
        temperatura, derivada = estado
        return [derivada, h_linha * (temperatura - ta)]

    def integrar(chute):
        tempos, estados = rk4_sistema(sistema, 0.0, [t1, chute], comprimento, dx, {})
        return tempos, estados

    chute_1 = parametros["chute_1"]
    chute_2 = parametros["chute_2"]
    _, estados_1 = integrar(chute_1)
    _, estados_2 = integrar(chute_2)
    t_l_1 = estados_1[-1][0]
    t_l_2 = estados_2[-1][0]
    chute_corrigido = chute_1 + ((t2 - t_l_1) / (t_l_2 - t_l_1)) * (chute_2 - chute_1)
    pontos, estados = integrar(chute_corrigido)
    temperaturas = [estado[0] for estado in estados]

    return pontos, temperaturas, chute_corrigido


def diferencas_finitas_calor(parametros, n_internos):
    """Resolve o problema da haste por Diferenças Finitas."""
    h_linha = parametros["h_linha"]
    ta = parametros["ta"]
    t1 = parametros["t1"]
    t2 = parametros["t2"]
    comprimento = parametros["comprimento"]
    dx = comprimento / (n_internos + 1)
    coeficiente = h_linha * dx * dx

    subdiagonal = [-1.0] * (n_internos - 1)
    diagonal = [2.0 + coeficiente] * n_internos
    superdiagonal = [-1.0] * (n_internos - 1)
    termos = [coeficiente * ta for _ in range(n_internos)]
    termos[0] += t1
    termos[-1] += t2

    internos = thomas(subdiagonal, diagonal, superdiagonal, termos)
    pontos = [i * dx for i in range(n_internos + 2)]
    temperaturas = [t1] + internos + [t2]

    return pontos, temperaturas
